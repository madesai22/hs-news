import json
import file_handling as fh 



json_file = '/data/madesai/papers.jsonlist'
data = fh.read_jsonlist(json_file)
print(data[0])

    


