import json
import file_handling as fh 



json_file = '/data/madesai/school_locations_full.jsonlist'
data = fh.read_jsonlist(json_file)
print(data[0])

    


