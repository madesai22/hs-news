import json
import file_handling as fh 



high = 0 
college = 0 
middle = 0 
with open('/data/madesai/articles_clean.jsonlist') as f:
    for line in f:
        school_type = json.loads(line)['school_type']
        if school_type == 'high':
            high +=1
        elif school_type == 'college':
            college +=1
        elif school_type == 'middle':
            middle +=1
        else:
            print(school_type)

print("{} middle, {} high, {} college".format(middle,high,college))
            

    


