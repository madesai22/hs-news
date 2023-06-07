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


def get_meta_data(domain, meta_data_json):
    for school in meta_data_json:
        if pp.clean(school['domain']) == pp.clean(domain):
            return school

# date, school_type, category, (metadata zipcode, is_foreign, dem_share, state)
def make_corpus(data,path_to_metadata, columns = [], conditions = []): 
    # read in file
    #data = fh.read_json(path)
    n_total = len(data)
    metadata = fh.read_jsonlist(path_to_metadata)
    seen = set()
    corpus = []

    columns = {'date':[], 'school_type':[], 'zip_code':[], 'is_foreign':[], 'dem_share':[], 'state':[]}
    total = 0 
    for article in data:
        sys.stdout.write("Seen %d articles\r" %(total))
        sys.stdout.flush()
        total +=1
        take_article = True
        for column, condition in zip(columns, conditions): # select for conditions
            if article[column] != condition:
                take_article = False
        if take_article:
            text = article['content']
            if text not in seen: # remove duplicates 
                seen.add(text)

                # get metadata
                domain = article['domain']
                meta_data = get_meta_data(domain,metadata)
                columns['date'].append(pp.get_date(article['date']))
                columns['school_type'].append(article['school_type'])
                columns['zip_code'].append(meta_data['zipcode'])
                columns['is_foreign'].append(meta_data['is_foreign'])
                columns['dem_share'].append(meta_data['dem_share'])
                columns['state'].append(meta_data['state'])
                corpus.append(pp.pre_process(text,stopwords=None))
    return corpus, columns

def main():
    random_sample = '/data/madesai/student-news-full/articles_no_middle_10p_rs.jsonlist'
    if os.path.exists(random_sample):
        data = fh.read_jsonlist(random_sample)
    else:
        data = fh.read_jsonlist_random_sample('/data/madesai/student-news-full/all_articles_no_middle.jsonlist', 10, percent =True)
        fh.write_to_jsonlist(data, random_sample)

    print('read random sample')
    path_to_md = '/data/madesai/student-news-full/school_full_info_with_votes.jsonlist'
    corpus, columns = make_corpus(data,path_to_md, columns = ['school_type'], conditions = ['high'])
    print(corpus[:10])

    for c in columns:
        print(columns[c][:10])

if __name__ == '__main__':
    main()







    




