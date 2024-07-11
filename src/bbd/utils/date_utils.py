# coding : utf-8
# author : WONBEEN

import re
import datetime

text_date = {
    "어제": ["어제", "작일", "ㅇㅈ"],
    "오늘": ["오늘", "금일", "지금", "ㅇㄴ"],
    "내일": ["내일", "명일", "익일", "ㄴㅇ"],
    "월요일": ["월", "월요일"],
    "화요일": ["화", "화요일"],
    "수요일": ["수", "수요일"],
    "목요일": ["목", "목요일"],
    "금요일": ["금", "금요일"],
    "토요일": ["토", "토요일"],
    "일요일": ["일", "일요일"]
}
def get_previous_weekday_date(today, target_weekday):
    # 요일을 한국어로 정의
    weekdays_korean = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]

    # 현재 요일 계산
    current_weekday_index = today.weekday()

    # 타겟 요일의 인덱스 계산
    target_weekday_index = weekdays_korean.index(target_weekday)

    # 오늘 날짜가 입력된 요일과 일치하는 경우
    if current_weekday_index == target_weekday_index:
        target_date = today
    else:
        # 일주일 전까지의 날짜를 기준으로 타겟 요일 계산
        days_difference = (current_weekday_index - target_weekday_index) % 7
        if days_difference == 0:
            days_difference = 7
        target_date = today - datetime.timedelta(days=days_difference)

    return target_date

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
            elif key in ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]:
                date_object = get_previous_weekday_date(today, key)
            date = date_object.strftime("%Y.%m.%d")    # YYYY.MM.DD
            
            return date
    return None    # text 입력이 잘못된 경우 None 값 반영
    
            

def format_date_num(input_date: str) -> str:
    """
    정규표현식을 통해 다양한 날짜 형식 매칭
    """
    patterns = [
        (r"(\d{4})[ ,.-]?(\d{2})[ ,.-]?(\d{2})", "%Y%m%d"),  # YYYYMMDD or YYYY{.,-}MM{.,-}DD
        (r"(\d{2})[ ,.-]?(\d{2})[ ,.-]?(\d{2})", "%y%m%d"),  # YYMMDD or YY{.,-}MM{.,-}DD
        (r"(\d{2})[ ,.-]?(\d{2})", "%m%d"),                 # MMDD or MM{.,-}DD
        (r'(\d{1})[ ,.-]?(\d{2})', '%m%d'),                  # MDD or M{.,-}DD
        (r'(\d{2})[ ,.-]?(\d{1})', '%m%d'),                  # MMD or MM{.,-}D
        (r'(\d{1})[ ,.-]?(\d{1})', '%m%d')                   # MD or M{.,-}D
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
                return date_object.strftime("%Y.%m.%d")
            except Exception as e:
                message = f"{input_date} is wrong."
                logger.error(message)
                raise e

    return None