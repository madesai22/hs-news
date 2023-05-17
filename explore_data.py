import json
import file_handling as fh 



i = 0 
with open('/data/madesai/articles_clean.jsonlist') as f:
    for line in f:
        if i <25:
            print(json.loads(line)['school_type'])
            
        i +=1

    


