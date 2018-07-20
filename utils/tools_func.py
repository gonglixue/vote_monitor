import json

def get_json_data_from_file(file_path):
    with open(file_path, "r") as f:
        json_txt = f.read()
        json_obj = json.loads(json_txt)
        print(json_obj["ok"])

        return json_obj