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
    
    
@dataclass
class PostProcessOutput:
    """
    후처리의 Output 형태를 고정하기 위함
    """
    trial: bool = None    # True or False
    outputs: str = None    # 지출 기록은 "success", 지출 내역 확인은 text