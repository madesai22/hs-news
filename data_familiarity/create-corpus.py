# first command line argument: path to directory for storing below files
# if not supplied will write to /data/madesai/gv-topic-data
# second command line argument: path to stopword text file
# if not supplied will read from to ./snowball.txt
# creates a jsonlist file with the articles + all meta data that match for gun violence-related headlines
# creates a pickeled corpus of gun violence news articles (list of articles that have been preprocessed)
# creates a pickeled corpus of all news articles (list of articles that have been preprocessed) 
# creates a pickeled corpus of all headlines (list of headlines that have been preprocessed)
# preprocessing = removing snowball stopwords, replacing all punctuation with blank, removing multiple white spaces, and tokenizing 
import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import preprocess as pp
import file_handling as fh
import sys
import json
import os


def main():
    try:
        path = sys.argv[1]
        fh.makedirs(path)
    except:
        path = "/data/madesai/gv-topic-data/"
    print("Writing to "+path)
    
    try:
        if os.path.exists(os.path.dirname(sys.argv[2])):
            stopword_file = sys.argv[2]
    except:
        stopword_file = "/home/madesai/hs-news/snowball.txt"
        
    print("Reading stopwords from "+stopword_file)
    stopwords = fh.read_text_to_list(stopword_file)
    stopwords = set([word.strip() for word in stopwords])

    gv_by_headline_json_file = []
    gv_by_headline_content = []
    gv_by_content_content = []
    all_content = []
    all_headlines = []
    n_gv = 0 
    total = 0
    with open('/data/madesai/articles_clean.jsonlist') as f, open(path+'/gv-headlines.csv','w') as f2, open(path+'/shooting-headlines.csv','w') as f3:
        for line in f:
            sys.stdout.write("Seen %.2f percent of articles\r" %(total/1951843*100))
            sys.stdout.flush()
            total +=1
            
            data = json.loads(line)
            headline = data['headline']
            content = data['content']
            pp_content = pp.pre_process(content,stopwords=None)

            if data['date']:
                year = pp.get_year(data['date'])
            else:
                year =  3000
            
            all_headlines.append(headline)
            all_content.append(pp_content)

            # if pp.match_gun_violence(headline):
            #     gv_by_headline_json_file.append(line)
            #     gv_by_headline_content.append(pp_content)
            #     f2.write(headline.replace(",", "")+','+str(year)+'\n')
            #     n_gv +=1
            # if pp.match_gun_violence_simple(content):
            #     gv_by_content_content.append(pp_content)
            #     f3.write(headline.replace(",", "")+','+str(year)+'\n')      
    
    sys.stdout.write("Writing files...")
    #fh.pickle_data(gv_by_content_content, path+'/gv_content_by_content.pkl')
    #fh.pickle_data(gv_by_headline_content, path+'/gv_content_by_headline.pkl')
    fh.pickle_data(all_headlines,path +'/all_headlines.pkl')
    fh.pickle_data(all_content, path+'/all_content.pkl')
    #fh.write_to_jsonlist(gv_by_headline_json_file,path+'/gun-violence-articles-by-headline_clean.jsonlist')


    documentation = """file,description
    gv-headlines.csv,headlines that match gun violence terms - not preprocessed
    gv_content.pkl,list of full content of articles that match gun violence terms, where each article is preprocessed (list of list of strings)
    all_headlines.pkl,list of headlines of all articles, where each headline is preprocessed (list of list of strings) - stopwords not removed
    all_content.pkl,list of full content of articles, where each article is preprocessed (list of list of strings) - stopwords not removed
    all_headlines_stopwords_removed.pkl,list of headlines of all articles, where each headline is preprocessed (list of list of strings) - stopwords removed
    all_content_stopwords_removed.pkl,list of full content of articles, where each article is preprocessed (list of list of strings) - stopwords removed
    gun-violence-articles_clean.jsonlist,jsonlist file with all articles that match gun violence terms, no preprocessing
    stopwords, """+ stopword_file+""" 
    other preprocessing, remove punctuation remove extra white spaces words lowercased tokenized"""

    fh.write_documentation(documentation,path+"/README.txt")
    sys.stdout.write("Done!")


if __name__ == '__main__':
    main()







    




