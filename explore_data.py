import json
import file_handling as fh 



i = 0 
with open('/data/madesai/articles_clean.jsonlist') as f:
    for line in f:
        if i <1:
            print(line.keys)
        i +=2

    


