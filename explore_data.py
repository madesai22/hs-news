import json
import file_handling as fh 



json_file = '/data/madesai/school_full_info_with_votes.jsonlist'
data = fh.read_jsonlist(json_file)
print(data)


