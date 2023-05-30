from datetime import date


def str2date(datestr: str) -> date:
    """
    YYYYMMDD 형식의 날짜 표현을 datetime.date 객체로 변환합니다.
    
    Args:
        datestr (str):YYYYMMDD 형태의 문자열

    Returns:
        datetime.date: 변환된 날짜 객체
    """
    return date(int(datestr[:4]), int(datestr[4:6]), int(datestr[6:]))

def date2str(d: date) -> str:
    """
    datetime.date 객체를 YYYYMMDD 형식의 날짜 표현으로 변환합니다.

    Args:
        d (datetime.date): 변환할 날짜 객체

    Returns:
        str: YYYYMMDD 형태의 문자열
    """
    return f"{d.year}{d.month:02d}{d.day:02d}"

def yyyy_mm_dd2date(datestr: str) -> date:
    y, m, d = datestr[:10].split("-")
    return date(int(y), int(m), int(d))

def date2yyyy_mm_dd(d: date) -> str:
    return f"{d.year:04d}-{d.month:02d}-{d.day:02d}"
