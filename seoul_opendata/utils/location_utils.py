import re
from typing import Final
from seoul_opendata.models.location import Location

LocationRegex: Final[re.Pattern] = re.compile(r"서울특별시 ([ㄱ-ㅎ|ㅏ-ㅣ|가-힣]+구) [ㄱ-ㅎ|ㅏ-ㅣ|가-힣\d\w ]+")

def parse_location(addr: str) -> Location | None:
    addrMatch: re.Match | None = LocationRegex.match(addr)
    
    if addrMatch is None:
        return None
    
    return Location(addrMatch.group(1))
    