from gensim.models.wrappers.ldamallet import LdaMallet
from gensim.matutils import corpus2csc
from gensim.models import CoherenceModel
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import datapath
import numpy
import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import file_handling as fh
import pandas as pd
import numpy as np

def corpus_distribution_of_topics(model,corpus):
    results = model[corpus]
    corpus_topics = [sorted(topics, key=lambda record: -record[1])[0] for topics in results]
    return corpus_topics 

def get_dominant_topic_by_document(model,corpus_topics):
    corpus_topic_df = pd.DataFrame()
    # get the Titles from the original dataframe
    # corpus_topic_df['Title'] = df.Title
    corpus_topic_df['Dominant Topic'] = [item[0]+1 for item in corpus_topics]
    corpus_topic_df['Contribution %'] = [round(item[1]*100, 2) for item in corpus_topics]
    topics_df = make_topic_csv(model)
    corpus_topic_df['Topic Terms'] = [topics_df.iloc[t[0]]['Terms per Topic'] for t in corpus_topics]
    return corpus_topic_df


def dominant_topic_analysis(corpus, corpus_topic_df):
    dominant_topic_df = corpus_topic_df.groupby('Dominant Topic').agg(
                                  Doc_Count = ('Dominant Topic', np.size),
                                  Total_Docs_Perc = ('Dominant Topic', np.size)).reset_index()

    dominant_topic_df['Total_Docs_Perc'] = dominant_topic_df['Total_Docs_Perc'].apply(lambda row: round((row*100) / len(corpus), 2))
    dominant_topic_df = dominant_topic_df.sort_values(by=['Total_Docs_Perc'])
    return dominant_topic_df

def make_topic_csv(ldamallet):
    topic_list = [[(term, round(wt, 3)) for term, wt in ldamallet.show_topic(n, topn=20)] for n in range(0, ldamallet.num_topics)]
    #topic_df = pd.DataFrame([[term for term, wt in topic] for topic in topic_list], columns = ['Term'+str(i) for i in range(1, 21)], index=['Topic '+str(t) for t in range(1, ldamallet.num_topics+1)]).T
    

    pd.set_option('display.max_colwidth', -1)
    topics_df = pd.DataFrame([', '.join([term for term, wt in topic]) for topic in topic_list], columns = ['Terms per Topic'], index=['Topic'+str(t) for t in range(1, ldamallet.num_topics+1)] )
    return topics_df

def topic_model(corpus, dictionary, path_to_file, ntopics,path_to_save_file):

    path_to_mallet_binary = "/home/madesai/Mallet/bin/mallet"

    path_list = path_to_file.split("/")[:-1]
    path = "/".join(path_list)+"/"
    file_name = path_list[-1].split(".")[0]
    out_file_name = path_to_save_file+"lda_"+file_name+"_"+str(ntopics)
    out_file = datapath(out_file_name)

    
    

    ldamallet = LdaMallet(path_to_mallet_binary, corpus=corpus, num_topics=ntopics, id2word=dictionary)
    topic_df = make_topic_csv(ldamallet)
    topic_df.to_csv(path+file_name+"topics_"+str(ntopics)+".csv")
    ldamallet.save(out_file)
    return ldamallet


def make_corpus(filename, truncate = True):
    content = fh.unpickle_data(filename)
    if truncate:
        content = content[:300]
    dictionary = Dictionary(content)
    corpus = [dictionary.doc2bow(text) for text in content]
    return corpus, dictionary


def all_analysis(path,data,ntopics, truncate = True):
    for p in data:
        for nt in ntopics:
            print("Finding {} topics in {} file".format(nt, p))
            corpus, dictionary = make_corpus(path+p, truncate=truncate) 
            lda = topic_model(corpus,dictionary,path+p,nt,path)

            cd = corpus_distribution_of_topics(lda,corpus)
            corpus_topic_df = get_dominant_topic_by_document(lda,cd)
            dominant_topic = dominant_topic_analysis(corpus, corpus_topic_df)
            print(dominant_topic)
            dominant_topic.to_csv(path+"dominant_topic")
            


    

def main():
    path = "/data/madesai/gv-topic-data/"
    data =["all_headlines.pkl"]
    #gv_data = "gv_content_by_headline.pkl"
    ntopics =[10]
    all_analysis(path,data,ntopics,truncate=True)
    

            
            


    

if __name__ == '__main__':
    main()





        