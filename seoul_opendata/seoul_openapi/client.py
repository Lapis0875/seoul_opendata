from functools import wraps
import json
import os
from typing import Any, Callable, ClassVar, Final, Optional, TypedDict

import requests

class OpenApiOptionExtras(TypedDict):
    startIndex: int
    endIndex: int

def opendata(options: Optional[OpenApiOptionExtras] = None):
    """공공데이터 api를 호출하는 메소드를 자동 구현하는 데코레이터입니다.
    API의 서비스 명칭이 모두 childSchool~로 시작한다는 점에서 착안했습니다.

    Args:
        options (Optional[OpenApiOptionExtras], optional): 가져올 데이터의 시작 인덱스와 끝 인덱스를 설정합니다. 기본 값은 None입니다.
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
            url=f"{self.base}/json/{meth.__name__}"
            if options is not None:
                url += f"/{options['startIndex']}/{options['endIndex']}"
                
            resp: requests.Response = self.session.get(url)
            data: dict[str, Any] = resp.json()
            
            self.saveData(data, meth.__name__)
            return data
        return wrapper
    
        SeoulOpenAPI.__api_calls__.append(wrapper.__name__)

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
    
    def fetchall(self):
        """등록된 모든 공공데이터 api를 호출합니다."""
        for api_call in self.__api_calls__:
            getattr(self, api_call)()

class SeoulOpenData:
    """서울 공공데이터 이용 클라이언트."""
    def __init__(self):
        self.api: SeoulOpenAPI = SeoulOpenAPI()
    
    def prefetch(self):
        self.api.fetchall()
