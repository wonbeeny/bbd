import json

def read_json(filepath):
    with open(filepath, 'r', encoding = 'utf-8') as f:
        return json.load(f)
    
def save_json(save_path, data):
    with open(save_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2, ensure_ascii=False)
        
def create_directory_if_not_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        pass