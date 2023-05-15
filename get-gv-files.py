# first command line argument: path to directory for storing below files
# if not supplied will write to /data/madesai/gv-topic-data
# second command line argument: path to stopword text file
# if not supplied will write to ./snowball.txt
# creates a jsonlist file with the articles + all meta data that match for gun violence-related headlines
# creates a pickeled corpus of gun violence news articles (list of articles that have been preprocessed)
# creates a pickeled corpus of all news articles (list of articles that have been preprocessed) 
# creates a pickeled corpus of all headlines (list of headlines that have been preprocessed)
# preprocessing = removing snowball stopwords, replacing all punctuation with blank, removing multiple white spaces, and tokenizing 

import preprocess as pp
import file_handling as fh
import sys
import json
import os


def main():
    if sys.argv[1]:
        path = sys.argv[1]
        fh.makedirs(path)
    else:
        path = "/data/madesai/gv-topic-data/"
    print("Writing to "+path)
    
    if sys.argv[2] and os.path.exists(os.path.dirname(sys.argv[2])):
        stopword_file = sys.argv[2]
    else:
        stopword_file = "/home/madesai/snowball.txt"
        
    print("Reading stopwords from "+stopword_file)
    stopwords = fh.read_text_to_list(stopword_file)
    stopwords = set([word.strip() for word in stopwords])

    gv_json_file = []
    gv_content = []
    all_content = []
    all_headlines = []
    
    with open('/data/madesai/articles_clean.jsonlist') as f, open(path+'/gv-headlines.csv','w') as f2:
        for line in f:
            data = json.loads(line)
            headline = pp.pre_process(data['headline'])
            content = pp.pre_process(data['content'])

            if data['date']:
                year = pp.get_year(data['date'])
            else:
                year =  3000

            
            if pp.match_gun_violence(headline):
                gv_json_file.append(line)
                gv_content.append(content,stopwords)
                f2.write(headline+','+str(year)+'\n')
            else: 
                all_headlines.append(headline)
                all_content.append(content)
    
    
    
    fh.pickle_data(gv_content, path+'/gv_content.pkl')
    fh.pickle_data(all_headlines,path +'/all_headlines.pkl')
    fh.pickle_data(all_content, path+'/all_content.pkl')
    fh.write_to_jsonlist(gv_json_file,path+'/gun-violence-articles_clean.jsonlist')
    
    documentation = """file\tdescription\n
    gv-headlines.csv\t preproccessed headlines that match gun violence terms\n
    gv_content.pkl\tlist of full content of articles that match gun violence terms, where each article is preprocessed (list of list of strings)\n
    all_headlines.pkl\tlist of headlines of all articles, where each headline is preprocessed (list of list of strings)\n
    all_content.pkl\tlist of full content of articles, where each article is preprocessed (list of list of strings)\n
    gun-violence-articles_clean.jsonlist\t jsonlist file with all articles that match gun violence terms, no preprocessing\n\n
    preprocessing: """+ stopword_file+""" stopwords, punctuation, extra white spaces, removed, words lowercased, tokenized\n"""

    fh.write_documentation(documentation,path+"/README.txt")


if __name__ == '__main__':
    main()







    




