# coding : utf-8
# author : WONBEEN

import copy
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

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
    format_date_num
)

class PreProcessor(BasePreProcessor):
    """
    고객이 입력한 지출 내역 text 를 전처리하여 구글 스프레드 시트에 입력하는 형태로 변환하는 클래스.
    
    만약 고객이 입력한 지출 내역 text 형태가 가이드 문서와 다르다면, False 및 error message 를 return
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
            self.errors.append([f"Please check `{self.user_text}`. user_text must have `/` maximum of four."])
            return None
        
        return result_dict
    
    def run(self) -> PreProcessOutput:
        """
        고객의 지출 내역을 전처리하여 return
        output 의 형태는 PreProcessOutput 로 고정
        """
        if self.errors != list():    # input 이 잘못 입력된 경우, 모든 연산을 거치지 않기 위함
            return PreProcessOutput(
                trial = False,
                outputs = None,
                errors = self.errors
            )
        else:
            result_dict = self._extract_components()
            if result_dict is None:    # input 이 잘못 입력된 경우, 모든 연산을 거치지 않기 위함
                return PreProcessOutput(
                    trial = False,
                    outputs = None,
                    errors = self.errors
                )
            else:    # input 이 올바른 형태로 입력된 경우, run
                category = result_dict["category"]
                amount = result_dict["amount"]
                date = result_dict["date"]
                note = result_dict["note"]

                # 입력한 카테고리를 변경
                real_category = format_category_match(category)

                # 입력한 금액의 형식을 파악 후 int 형식으로 변경
                real_amount = format_amount(amount)

                # 입력한 날짜가 숫자 형식인지 아닌지 파악 후 YY.MM.DD 형식으로 변경
                try:    # 숫자 형식
                    check_type = copy.copy(date)
                    for separator in [".", ",", "-"]:
                        check_type = check_type.replace(separator, "")
                    int(check_type)
                    real_date = format_date_num(date)
                except:    # 문자 형식
                    real_date = format_date_str(date)
                # 날짜를 안 적고 비고를 적은 경우(or 날짜를 적었는데 잘못 적은 경우), 날짜는 자동으로 오늘 날짜로 입력
                if real_date is None:
                    today = datetime.date.today()
                    real_date = today.strftime('%y.%m.%d')


                outputs = {
                    "category": real_category,    # 카테고리
                    "amount": real_amount,        # 금액
                    "date": real_date,            # [optional]날짜
                    "note": note                  # [optional]비고
                }

                return PreProcessOutput(
                    trial = True,
                    outputs = outputs,
                    errors = self.errors
                )

        

class PostProcessor(BasePostProcessor):
    """
    PreProcessor 에서 추출한 결과를 활용하여 고객의 구글 스프레드 시트에 저장하는 클래스
    """
    def append_value_to_column(self, json_key_path, sheet_url, outputs):
        # 구글 인증
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(json_key_path, scope)
        client = gspread.authorize(creds)

        # 스프레드시트 오픈
        sheet = client.open_by_url(sheet_url)
        worksheet = sheet.get_worksheet(0)  # 첫 번째 워크시트 사용

        # D, E열 데이터 읽고 빈 Row 위치 찾기
        column_D_data = worksheet.col_values(4)  # 'D'열은 4번째 열
        column_E_data = worksheet.col_values(5)  # 'E'열은 5번째 열

        # A, B열 둘 다 비어있는 Row 찾기
        last_row = len(column_D_data) if len(column_D_data) >= len(column_E_data) else len(column_E_data) 
        row_to_write = last_row + 1  # 둘 다 비어있는 Row

        # 현재 시간
        now = datetime.datetime.now()
        time = now.strftime('%H:%M')
        
        # 지출 내역 입력
        worksheet.update_acell(f'{"A"}{row_to_write}', outputs["date"])
        worksheet.update_acell(f'{"C"}{row_to_write}', time)
        worksheet.update_acell(f'{"D"}{row_to_write}', outputs["amount"])
        worksheet.update_acell(f'{"E"}{row_to_write}', outputs["category"])
        worksheet.update_acell(f'{"G"}{row_to_write}', outputs["note"])
    
    def run(self, user_json, user_id, outputs) -> PostProcessOutput:
        """
        Args:
            user_json (:obj: `Dict[str, List]`):
                고객의 정보 (API Key & Sheet URL)
            user_id (:obj:`str`):
                고객의 고유 번호
            outputs (:obj:`Dict[str, str]`):
                고객이 저장하고자 하는 지출 내역을 전처리(PreProcessor)한 결과
        """
        if not self.trial:
            return PostProcessOutput(
                trial = False,
                outputs = None,
                errors = self.errors
            )
        else:
            # try:
            json_key_path, sheet_url = user_json[user_id]
            self.append_value_to_column(json_key_path, sheet_url, outputs)
            return PostProcessOutput(
                trial = True,
                outputs = "Yes~~~",
                errors = self.errors
            )
            # except:
            #     self.errors.append(["Wow~~~"])
            #     return PostProcessOutput(
            #         trial = False,
            #         outputs = None,
            #         errors = self.errors
            #     )