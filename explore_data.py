import json
import file_handling as fh 



nschools = 0
with open('/data/madesai/gv-topic-data/all_headlines') as f:
    for line in f:
        if json.loads(line)['school_name']:
            nschools+=1

print("{} schools".format(nschools))
        
            

    


