# coding : utf-8
# author : WONBEEN

import re

def format_amount(input_amount: str) -> str:
    """ 
    숫자와 [`.`, `,`]을 제외한 모든 문자를 공백으로 치환
    """
    amount = re.sub(r"[^0-9\.,]", "", input_amount)
    return amount