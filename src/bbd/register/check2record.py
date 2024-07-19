# coding : utf-8
# author : WONBEEN

from ..base import (
    BasePreProcessor,
    BasePostProcessor,
    PreProcessOutput,
    PostProcessOutput
)
from ..utils import (
    get_logger
)

logger = get_logger(__name__)

text_type = [
    "지출내역확인", "내역확인", "지출내역", "지출확인", "확인", "내역",
    "ㅈㅊㄴㅇㅎㅇ", "ㄴㅇㅎㅇ", "ㅈㅊㄴㅇ", "ㅈㅊㅎㅇ", "ㅎㅇ", "ㄴㅇ"
]

class PreProcessor(BasePreProcessor):
    """
    고객이 입력한 지출 내역 확인 text 를 확인하는 클래스.
    """
    
    def run(self) -> PreProcessOutput:
        """
        output 의 형태는 PreProcessOutput 로 고정
        """
        user_text = self.user_text.replace(" ", "")
        
        if user_text not in text_type:
            message = f"Please check your text."
            raise NotImplementedError(message)

        return PreProcessOutput(
            trial = True,
            outputs = user_text
        )
        

class PostProcessor(BasePostProcessor):
    """
    스프레드 시트에 입력된 지출 내역을 가져와 처리하여 string 형태로 변환하는 클래스
    """    
    def _get_record_list(self):
        # 스프레드시트 오픈
        try:
            worksheet = self.sheet.worksheet("Spend")  # 워크시트 명은 "Spend" 으로 고정하여 사용
        except Exception as e:
            message = "Invalid open spread sheet."
            logger.error(message)
            raise e
            
        all_rows = worksheet.get_all_values()
        spend_rows = list() if len(all_rows) == 1 else all_rows[1:]
        check_rows = spend_rows[-min(len(spend_rows), 7):]
        
        # view_headers와 동일한 원소의 인덱스를 추출
        header_row = all_rows[0]
        view_headers = ["날짜", "요일", "영지사신 구분", "금액", "내용"]
        indices = [header_row.index(header) for header in view_headers if header in header_row]
        
        formatted_str = str()
        for idx, data in enumerate(check_rows):
            # 특정 인덱스에 해당하는 원소 추출
            selected_data = [idx+1]
            selected_data += [data[i] for i in indices]
            formatted_str += ' | '.join(str(item) for item in selected_data)
            if len(check_rows) != idx+1:
                 formatted_str += "\n\n"

        return formatted_str
        
    
    def run(self, outputs) -> PostProcessOutput:
        """
        output 의 형태는 PostProcessOutput 로 고정
        
        Args:
            outputs (:obj:`Dict[str, str]`):
                사용하지 않음.
        """
        try:
            formatted_str = self._get_record_list()
        except Exception as e:
            message = "Sheet checking failed."
            logger.error(message)
            raise e
            
        return PostProcessOutput(
            trial = True,
            outputs = formatted_str
        )