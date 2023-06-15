import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import preprocess as pp
import file_handling as fh
import sys
import json
import os

def unpack_labels(labels_dict):
    date = labels_dict['date']
    school_type = labels_dict['school_type']
    zip_code = labels_dict['zip_code']
    is_foreign = labels_dict['is_foreign']
    state = labels_dict['state']
    return date, school_type, zip_code, is_foreign, state


def get_meta_data(domain, meta_data_json):
    for school in meta_data_json:
        if pp.clean(school['domain']) == pp.clean(domain):
            return school

# date, school_type, category, (metadata zipcode, is_foreign, dem_share, state)
def make_corpus(data, path_to_metadata, columns = [], conditions = []): 
    # read in file
    #data = fh.read_json(path)
    n_total = len(data)
    metadata = fh.read_jsonlist(path_to_metadata)
    seen = set()
    corpus = []

    labels = {'date':[], 'school_type':[], 'zip_code':[], 'is_foreign':[], 'dem_share':[], 'state':[]}
    total = 0 
    duplicates = 0 
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
                labels['date'].append(pp.get_date(article['date']))
                labels['school_type'].append(article['school_type'])
                labels['zip_code'].append(meta_data['zipcode'])
                labels['is_foreign'].append(meta_data['is_foreign'])
                labels['dem_share'].append(meta_data['dem_share'])
                labels['state'].append(meta_data['state'])
                corpus.append(pp.pre_process(text,stopwords=None))
        else:
            duplicates += 1
    print("found {} duplicates".format(duplicates))

    return corpus, labels

def main():
    # random_sample = '/data/madesai/student-news-full/articles_no_middle_10p_rs.jsonlist'
    # if os.path.exists(random_sample):
    #     data = fh.read_jsonlist(random_sample)
    # else:
    #     data = fh.read_jsonlist_random_sample('/data/madesai/student-news-full/all_articles_no_middle.jsonlist', .1, percent =True)
    #     fh.write_to_jsonlist(data, random_sample) 
    data = fh.read_jsonlist('/data/madesai/student-news-full/all_articles_no_middle.jsonlist')
    print('read data sample')
    path_to_md = '/data/madesai/student-news-full/school_full_info_with_votes.jsonlist'
    corpus, columns = make_corpus(data,path_to_md)# columns = ['school_type'], conditions = ['high'])
    print(corpus[:10])

    for c in columns:
        print(columns[c][:10])

if __name__ == '__main__':
    main()







    




