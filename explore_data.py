import json
import file_handling as fh 



high = 0 
other = 0 
with open('/data/madesai/articles_clean.jsonlist') as f:
    for line in f:
        
        if json.loads(line)['school_type'] == 'high':
            high +=1
        else:
            print(json.loads(line)['school_type'])
            

    


