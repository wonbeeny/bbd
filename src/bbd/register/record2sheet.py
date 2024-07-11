# coding : utf-8
# author : WONBEEN

import copy
import datetime
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials

from ..base import (
    BasePreProcessor,
    BasePostProcessor,
    PreProcessOutput,
    PostProcessOutput
)
from ..utils import (
    format_category_match,
    format_amount,
    format_date_str,
    format_date_num,
    find_sheet_columns,
    get_logger
)

logger = get_logger(__name__)

class PreProcessor(BasePreProcessor):
    """
    고객이 입력한 지출 내역 text 를 전처리하여 구글 스프레드 시트에 입력하는 형태로 변환하는 클래스.
    
    만약 고객이 입력한 지출 내역 text 형태가 가이드 문서와 다르다면, False 및 error log return
    """
    def _extract_components(self) -> dict:
        """
        고객이 입력한 지출 내역 text 를 '/' 를 기준으로 분할한 뒤, 4개의 type 으로 분류
        4개의 type: [카테고리, 금액, 날짜, 비고]
        """
        result_dict = {
            "category": None,    # 카테고리
            "amount": None,      # 금액
            "date": None,        # [optional]날짜
            "note": None         # [optional]비고
        }
        
        components = [component.strip() for component in self.user_text.split('/')]
        result_dict["category"] = components[0]
        result_dict["amount"] = components[1]
        if len(components) == 2:
            result_dict["date"] = "오늘"    # 날짜 입력 안 하면 오늘 날짜로 지정
            result_dict["note"] = " "       # 비고 입력 안 하면 빈칸으로 지정
        elif len(components) == 3:    # 3개가 들어올 땐 날짜와 비고에 모두 입력 but 날짜 형식이 아닌 경우, 오늘 날짜로 변환
            result_dict["date"] = components[2]
            result_dict["note"] = components[2]
        elif len(components) == 4:
            result_dict["date"] = components[2]
            result_dict["note"] = components[3]
        else:    # / 가 5개 이상인 경우 에러 발생
            message = f"Please check `{self.user_text}`. user_text must have `/` maximum of three."
            raise NotImplementedError(message)
        
        return result_dict
    
    def run(self) -> PreProcessOutput:
        """
        고객의 지출 내역을 전처리하여 return
        output 의 형태는 PreProcessOutput 로 고정
        """
        result_dict = self._extract_components()
        
        category = result_dict["category"]
        amount = result_dict["amount"]
        date = result_dict["date"]
        note = result_dict["note"]

        # 입력한 카테고리를 변경
        real_category = format_category_match(category)

        # 입력한 금액의 형식을 파악 후 float 형식으로 변경
        real_amount = format_amount(amount)

        # 입력한 날짜가 숫자 형식인지 아닌지 파악 후 YYYY.MM.DD 형식으로 변경
        try:    # 숫자 형식
            check_type = copy.copy(date)
            for separator in [".", ",", "-", " "]:
                check_type = check_type.replace(separator, "")
            int(check_type)
            real_date = format_date_num(date)
        except:    # 문자 형식
            real_date = format_date_str(date)
        # 날짜를 안 적고 비고를 적은 경우(or 날짜를 적었는데 잘못 적은 경우), 날짜는 자동으로 오늘 날짜로 입력
        if real_date is None:
            message = f"The date was `None` followed by default, and today's date was entered. \n user_text: {self.user_text}"
            logger.info(message)
            today = datetime.date.today()
            real_date = today.strftime('%Y.%m.%d')    # YYYY.MM.DD

        # outputs 정의
        outputs = {
            "category": real_category,    # 카테고리
            "amount": real_amount,        # 금액
            "date": real_date,            # [optional]날짜
            "note": note                  # [optional]비고
        }

        return PreProcessOutput(
            trial = True,
            outputs = outputs
        )
        

class PostProcessor(BasePostProcessor):
    """
    PreProcessor 에서 추출한 결과를 활용하여 고객의 구글 스프레드 시트에 저장하는 클래스
    """    
    def append_value_to_column(self, outputs):
        # 스프레드시트 오픈
        try:
            worksheet = self.sheet.worksheet("Spend")  # 워크시트 명은 "Spend" 으로 고정하여 사용
        except Exception as e:
            message = "Invalid open spread sheet."
            logger.error(message)
            raise e
        
        # Column 에 대한 index 찾기
        headers = ["날짜", "세부시간", "금액", "영지사신 구분", "내용", "요일", "날짜 구분"]    # 찾을 헤더 목록 고정하여 사용
        column_indices = find_sheet_columns(worksheet, headers)    # 헤더에 해당하는 열 찾기
        
        # D, E열 데이터 읽고 빈 Row 위치 찾기
        column_amount_data = worksheet.col_values(column_indices["금액"])              # 금액 열
        column_category_data = worksheet.col_values(column_indices["영지사신 구분"])    # 영지사신 구분 열

        # A, B열 둘 다 비어있는 Row 찾기
        last_row = len(column_amount_data) if len(column_amount_data) >= len(column_category_data) else len(column_category_data) 
        row_to_write = last_row + 1  # 둘 다 비어있는 Row

        # 현재 시간
        now = datetime.datetime.now()
        time = now.strftime('%H:%M')
        
        num2alpha = {1:"A", 2:"B", 3:"C", 4:"D", 5:"E", 6:"F", 7:"G", 8:"H", 9:"I"}
        weekdays_korean = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
        
        # 지출 내역 입력
        try:
            worksheet.update_acell(f'{num2alpha[column_indices["날짜"]]}{row_to_write}', outputs["date"])
            worksheet.update_acell(f'{num2alpha[column_indices["세부시간"]]}{row_to_write}', time)
            worksheet.update_acell(f'{num2alpha[column_indices["금액"]]}{row_to_write}', outputs["amount"])
            worksheet.update_acell(f'{num2alpha[column_indices["영지사신 구분"]]}{row_to_write}', outputs["category"])
            worksheet.update_acell(f'{num2alpha[column_indices["내용"]]}{row_to_write}', outputs["note"])
            
            date = datetime.datetime.strptime(outputs["date"], "%Y.%m.%d")
            weekday_index = date.weekday()
            weekday = weekdays_korean[weekday_index]
            worksheet.update_acell(f'{num2alpha[column_indices["요일"]]}{row_to_write}', weekday)
            worksheet.update_acell(f'{num2alpha[column_indices["날짜 구분"]]}{row_to_write}', outputs["date"][:-3])
        except Exception as e:
            message = "Failed to write in worksheet."
            logger.error(message)
            raise e
    
    def run(self, outputs) -> PostProcessOutput:
        """
        Args:
            outputs (:obj:`Dict[str, str]`):
                고객이 저장하고자 하는 지출 내역을 전처리(PreProcessor)한 결과
        """
        try:
            self.append_value_to_column(outputs)
        except Exception as e:
            message = "Sheet registration failed."
            logger.error(message)
            raise e
            
        return PostProcessOutput(
            trial = True,
            outputs = "GOD bless you ~"
        )