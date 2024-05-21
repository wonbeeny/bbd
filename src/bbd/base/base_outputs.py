# coding : utf-8
# author : WONBEEN

from typing import Dict, List
from datetime import datetime
from dataclasses import dataclass

@dataclass
class PreProcessOutput:
    """
    전처리의 Output 형태를 고정하기 위함
    """
    trial: bool = None    # True or False
    outputs: Dict[str, str] = None    # 지출 기록은 components_dict, 통계치는 json 형태
    errors: List[str] = None    # error 발생 안 하면 [], 하면 error message
    
    
@dataclass
class PostProcessOutput:
    """
    후처리의 Output 형태를 고정하기 위함
    """
    trial: bool = None    # True or False
    outputs: str = None    # 지출 기록은 "success", 통계치는 image path
    errors: List[str] = None    # error 발생 안 하면 [], 하면 error message
    
    
def mk_Output(user_id, trial, logType=None, errors=[]):
    now = datetime.now()
    date_now = now.strftime('%Y-%m-%d %H:%M:%S')
    
    _logs = '\n'.join([error[0] for error in errors])
    logs = _logs if _logs != "" else None
    
    Output_final = {
        "user_id": user_id,     # [str] 고객의 id
        "trial": trial,         # [bool] 실행 성공 여부
        "datetime": date_now,   # [str] Log 발생 시간
        "logType": logType,     # [optional: str] 로그 대분류 (에러가 발생한 스크립트 명)
        "logs": logs            # [optional: str] 에러 메세지
    }
    return Output_final