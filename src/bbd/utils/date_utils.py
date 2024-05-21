import re
import datetime

text_date = {
    "어제": ["어제", "작일", "ㅇㅈ"],
    "오늘": ["오늘", "금일", "지금", "ㅇㄴ"],
    "내일": ["내일", "명일", "익일", "ㄴㅇ"]
}

def format_date_str(input_date: str) -> str:
    """
    텍스트로 입력한 날짜 형식 매칭
    """
    for key, values in text_date.items():
        if input_date in values:
            today = datetime.date.today()
            if key == "어제":
                date_object = today - datetime.timedelta(days=1)
            elif key == "오늘":
                date_object = today
            elif key == "내일":
                date_object = today + datetime.timedelta(days=1)
            date = date_object.strftime("%y.%m.%d")    # YY.MM.DD
            return date
    return None    # text 입력이 잘못된 경우 None 값 반영
    
            

def format_date_num(input_date: str) -> str:
    """
    정규표현식을 통해 다양한 날짜 형식 매칭
    """
    patterns = [
        (r"(\d{4})[,.-]?(\d{2})[,.-]?(\d{2})", "%Y%m%d"),  # YYYYMMDD or YYYY{.,-}MM{.,-}DD
        (r"(\d{2})[,.-]?(\d{2})[,.-]?(\d{2})", "%y%m%d"),  # YYMMDD or YY{.,-}MM{.,-}DD
        (r"(\d{2})[,.-]?(\d{2})", "%m%d")                  # MMDD or MM{.,-}DD
    ]

    for pattern, date_format in patterns:
        match = re.match(pattern, input_date)
        if match:
            date_str = "".join(match.groups())
            try:
                # 현재 연도를 사용해야 할 경우에만 처리
                if len(date_str) == 4:
                    date_str = str(datetime.date.today().year) + date_str
                    date_format = "%Y%m%d"
                # 날짜 객체 생성 및 포맷
                date_object = datetime.datetime.strptime(date_str, date_format)
                return date_object.strftime("%y.%m.%d")
            except ValueError:
                return None

    return None