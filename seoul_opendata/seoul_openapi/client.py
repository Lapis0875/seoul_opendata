from contextlib import suppress
from functools import wraps
import json
import os
import re
from typing import Any, Callable, ClassVar, Final, Optional, TypedDict

import requests

from seoul_opendata.firebase.controller import DB, EntryAlreadyExist
from seoul_opendata.models.article import Article
from seoul_opendata.models.child_school import EstablishType
from seoul_opendata.models.location import Location
from seoul_opendata.models.payloads import ArticleCreate, ChildSchoolCreate
from seoul_opendata.utils.location_utils import parse_location
from setup import set_keys

ChildSchoolUniqueKey: Final[str] = "KINDERCODE"
OpenDataAPICallers: Final[list[str]] = []
set_keys()

class OpenApiOptionExtras(TypedDict):
    startIndex: int
    endIndex: int


def build_event(event_resp: dict[str, Any]) -> ArticleCreate:
    """
    행사 정보 데이터로부터 Article 객체를 생성합니다.
    
    Args:
        event_resp (dict[str, Any]): api 응답에서 얻은 행사 정보의 json 객체.
        
    Example data:
        {
            "CLTUR_EVENT_ETC_NM": "금천 하모니 축제",
            "SVC_CL_CODE": "2001",
            "SVC_CL_NM": "문화행사(보육반장)",
            "ATDRC_CODE": "11545",
            "ATDRC_NM": "금천구",
            "AGE_SE_CODE": "",
            "AGE_SE_NM": "",
            "X_CRDNT_VALUE": "126.89604",
            "Y_CRDNT_VALUE": "37.45707",
            "ZIP": "08611",
            "BASS_ADRES": "서울특별시 금천구 시흥대로73길 70",
            "DETAIL_ADRES": "금천구청 앞 중앙무대 (시흥동)",
            "RNTFEE_FREE_AT": "Y",
            "RNTFEE": "",
            "EVENT_PD_BGNDE": "2023-05-13",
            "EVENT_PD_ENDDE": "2023-05-14",
            "GUIDANCE_URL": "",
            "EVENT_FCLTY_NM": "금천문화재단",
            "REGIST_DT": "2023-04-29 02:37:02.0",
            "UPDT_DT": ""
        },
    """
    location: Location = Location(event_resp["ATDRC_NM"])
    
    content: str = f"{event_resp['CLTUR_EVENT_ETC_NM']}\n" + \
                f"행사 장소: {event_resp['BASS_ADRES']} {event_resp['DETAIL_ADRES']}\n" + \
                f"행사 기간: {event_resp['EVENT_PD_BGNDE']} {event_resp['EVENT_PD_ENDDE']}\n" + \
                f"행사 주최: {event_resp['EVENT_FCLTY_NM']}\n" + \
                f"행사 종류: {event_resp['SVC_CL_NM']}"
    
    return ArticleCreate(
        title=event_resp["CLTUR_EVENT_ETC_NM"],
        content=content,
        attachments=[],
        location=location,
        childSchoolId=None,
        uploadAt=event_resp["REGIST_DT"]
    )
        

def opendata(collect: bool = True, startIndex: int = 1, endIndex: int = 1000):
    """공공데이터 api를 호출하는 메소드를 자동 구현하는 데코레이터입니다.
    API의 서비스 명칭이 모두 childSchool~로 시작한다는 점에서 착안했습니다.

    Args:
        collect: (bool) fetchall()의 대상으로 이 메소드를 등록할지의 여부를 결정합니다. 기본 값은 True입니다.
        options (Optional[OpenApiOptionExtras], optional): 가져올 데이터의 시작 인덱스와 끝 인덱스를 설정합니다. 기본 값은 1부터 1000입니다.
    """
    def openDataDeco(meth: Callable[["SeoulOpenAPI"], Any]) -> Callable[["SeoulOpenAPI"], dict[str, Any]]:
        """실제 사용될 데코레이터입니다.

        Args:
            meth (Callable[[SeoulOpenAPI], Any]): 데코레이팅 된 메소드.

        Returns:
            Callable[["SeoulOpenAPI"], dict[str, Any]]: 구현부가 채워진 api 호출 메소드.
        """
        @wraps(meth)
        def wrapper(self: "SeoulOpenAPI") -> dict[str, Any]:
            """서울 공공데이터 api를 호출하는 메소드를 자동 구현합니다.
            데코레이팅 된 메소드 이름이 서비스 명칭에 해당합니다.

            Returns:
                dict[str, Any]: api의 응답 데이터.
            """
            url=f"{self.base}/json/{meth.__name__}/{startIndex}/{endIndex}"
                
            resp: requests.Response = self.session.get(url)
            # print(resp.content)
            
            if (resp.status_code != 200):
                # handle exceptions
                return {}
            
            data: dict[str, Any] = resp.json()
            self.saveData(data, meth.__name__)
            return data
        
        if collect:
            OpenDataAPICallers.append(wrapper.__name__)
        return wrapper
    return openDataDeco


class SeoulOpenAPI:
    """서울 공공데이터 API 클라이언트"""
    base: Final[str]
    __api_calls__: ClassVar[list[str]] = []
    
    def __init__(self):
        self.base = f"http://openapi.seoul.go.kr:8088/{os.environ['SEOUL_OPENDATA_KEY']}"
        self.session = requests.Session()
    
    def saveData(self, data: dict[str, Any], filename: str):
        with open(f"./seoul_opendata/seoul_openapi/data/{filename}.json", mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    @opendata()
    def childSchoolInfo(self):
        """
        서울시 유치원 일반현황
        서울특별시 소재 유치원 기본정보 유지원명, 소재지, 주소, 전화번호, 홈페이지주소 등 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20566/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolHygiene(self):
        """
        서울시 유치원 환경위생관리 현황
        서울특별시 소재 유치원의 실내공기질, 미세먼지 등 환경 위생 점검 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20574/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolInsurance(self):
        """
        서울시 유치원 보험별 가입 현황
        서울특별시 소재 유치원의 각종 보험 가입 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20577/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolBus(self):
        """
        서울시 유치원 통학차량 현황
        서울특별시 소재 유치원의 차량운행여부, 운행차량 수, 신고차량 수 등 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20572/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolMeal(self):
        """
        서울시 유치원 급식운영 현황
        서울특별시 소재 유치원 급식정보 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20571/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolYearWork(self):
        """
        서울시 유치원 직원 근속연수 현황
        서울특별시 소재 유치원 교사의 근속 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20573/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolLesson(self):
        """
        서울시 유치원 수업일수 현황
        서울특별시 소재 유치원의 수업일수 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20570/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolSafetyEdu(self):
        """
        서울시 유치원 안전점검 교육 실시 현황
        서울특별시 소재 유치원의 안전점검ㆍ교육 실시 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20575/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolTeacher(self):
        """
        서울시 유치원 직위 자격별 교직원 현황
        서울특별시 소재 유치원의 직위별 교사수, 보건교사, 영양교사 등 인력구성 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20569/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolClassArea(self):
        """
        서울시 유치원 교실면적 현황
        서울특별시 소재 유치원 기본정보 교실수, 면적, 체육장등 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20568/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolSociety(self):
        """
        서울시 유치원 공제회 가입 현황
        서울특별시 소재 유치원의 각종 공제회 가입 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20576/S/1/datasetView.do
        """
    
    @opendata()
    def childSchoolBuilding(self):
        """
        서울시 유치원 건물현황
        서울특별시 소재 유치원 건물의 건축년도, 건물층수, 전용면적 등 현황입니다.
        유치원알리미(https://e-childschoolinfo.moe.go.kr) 에서 제공되는 자료입니다.
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20567/S/1/datasetView.do
        """
    
    def fetchall(self) -> dict[str, list[dict[str, Any]]]:
        """등록된 모든 공공데이터 api를 호출합니다."""
        data: dict[str, list[dict[str, Any]]] = {}
        
        for api_call in OpenDataAPICallers:
            print(f"Fetching api `{api_call}`")
            data[api_call] = getattr(self, api_call)()[api_call]["row"]
        
        # print(data)
        return data
    
    @opendata(collect=False)
    def TnFcltySttusInfo2001(self):
        """
        서울시 지역보육 문화행사 정보
        지역보육정보 중 문화행사 정보(최근1년자료)
        
        Reference:
            http://data.seoul.go.kr/dataList/OA-20975/S/1/datasetView.do
        """

class SeoulOpenData:
    """서울 공공데이터 이용 클라이언트."""
    def __init__(self):
        self.api: SeoulOpenAPI = SeoulOpenAPI()
        self.data: dict[str, dict[str, Any]] = {}
        self.events: list[Article] = []
    
    def prefetch(self):
        data: dict[str, list[dict[str, Any]]] = self.api.fetchall()
        for childSchoolData in data.values():
            for e in childSchoolData:
                uniqueKey: str = e[ChildSchoolUniqueKey]
                if uniqueKey not in self.data:
                    self.data[uniqueKey] = e
                self.data[uniqueKey].update(e)
        
        eventData: dict[str, Any] = self.api.TnFcltySttusInfo2001()
        for event in eventData["TnFcltySttusInfo2001"]["row"]:
            self.events.append(DB.article.create(build_event(event)))
    
    def create(self):
        """Create ChildSchool entries on firebase."""
        print(f"Creating ChildSchool {len(self.data)} entries on firebase...")
        
        for data in self.data.values():
            # print(f"SeoulOpenData.create() : code = {data['KINDERCODE']}")
            addr: str = data["ADDR"]
            
            location: Location | None = parse_location(addr)
            if location is None:
                continue
            with suppress(EntryAlreadyExist):
                DB.childSchool.create(ChildSchoolCreate(
                    code=data["KINDERCODE"],
                    name=data["KINDERNAME"],
                    representerName=data["RPPNNAME"],
                    location=location,
                    address=addr,
                    establishType=EstablishType(data["ESTABLISH"][:2]),
                    establishAt=data["EDATE"],
                    openingTime=data["OPERTIME"],
                    tel=data["TELNO"],
                    children=[]
                ))
        print("Done!")
        
    def test(self):
        self.api.childSchoolInfo()
        self.api.childSchoolClassArea()
        

if __name__ == "__main__":
    os.environ["SEOUL_OPENDATA_KEY"] = "6c514452756c61703839496c494c72"
    client = SeoulOpenData()
    client.prefetch()
    client.api.saveData(client.data, "formatted")
