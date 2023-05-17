import json

def get_all_keys(json_file):
    with open(json_file, 'r') as file:
        json_data = json.load(file)
        
    all_keys = set()
    for json_object in json_data:
        keys = json_object.keys()
        all_keys.update(keys)
    
    return all_keys


json_file = '/data/madesai/school_full_info_with_votes.jsonlist'
keys = get_all_keys(json_file)


for key in keys:
    print(key)