# coding : utf-8
# author : WONBEEN

text_category = {
    "영적": ["영적", "영"],
    "지적": ["지적", "지"],
    "사회적": ["사회적", "사회", "사"],
    "신체적": ["신체적", "신체", "신"],
    "기타": ["기타", "기"],
    "지출": ["지출"],
    "낭비": ["낭비"]
}

def format_category_match(input_category: str) -> str:
    for category, values in text_category.items():
        if input_category in values:
            return category