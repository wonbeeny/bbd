# coding : utf-8
# author : WONBEEN

text_category = {
    "영적": ["영적", "영"],
    "지적": ["지적", "지"],
    "사회적": ["사회적", "사회", "사"],
    "신체적": ["신체적", "신체", "신"],
    "기여": ["기여"],
    "낭비": ["낭비", "낭"],
    "기타": ["기타", "기"],
    "고정 지출": ["고정 지출", "고정지출", "고정", "지출", "고"]
}

def format_category_match(input_category: str) -> str:
    for category, values in text_category.items():
        if input_category in values:
            return category
        
    message = f"Please check `{input_category}`. Not exist category in text."
    raise NotImplementedError(message)
