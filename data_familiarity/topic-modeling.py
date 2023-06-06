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

def corpus_distribution_of_topics(model,corpus):
    results = model[corpus]
    corpus_topics = [sorted(topics, key=lambda record: -record[1])[0] for topics in results]
    return corpus_topics 

def get_dominant_topic_by_document(model,corpus_distribution):
    corpus_topic_df = pd.DataFrame()
    # get the Titles from the original dataframe
    corpus_topic_df['Title'] = df.Title
    corpus_topic_df['Dominant Topic'] = [item[0]+1 for item in corpus_topics]
    corpus_topic_df['Contribution %'] = [round(item[1]*100, 2) for item in corpus_topics]
    corpus_topic_df['Topic Terms'] = [topics_df.iloc[t[0]]['Terms per Topic'] for t in corpus_topics]


def document_topic_analysis():
    dominant_topic_df = corpus_topic_df.groupby('Dominant Topic').agg(
                                  Doc_Count = ('Dominant Topic', np.size),
                                  Total_Docs_Perc = ('Dominant Topic', np.size)).reset_index()

    dominant_topic_df['Total_Docs_Perc'] = dominant_topic_df['Total_Docs_Perc'].apply(lambda row: round((row*100) / len(corpus), 2))

    dominant_topic_df

def topic_model(path_to_file, ntopics,path_to_save_file):

    path_to_mallet_binary = "/home/madesai/Mallet/bin/mallet"

    path_list = path_to_file.split("/")[:-1]
    path = "/".join(path_list)+"/"
    file_name = path_list[-1].split(".")[0]
    out_file_name = path_to_save_file+"lda_"+file_name+"_"+str(ntopics)
    out_file = datapath(out_file_name)

    content = fh.unpickle_data(path_to_file)
    content = content[:300]
    dictionary = Dictionary(content)
    corpus = [dictionary.doc2bow(text) for text in content]

    ldamallet = LdaMallet(path_to_mallet_binary, corpus=corpus, num_topics=ntopics, id2word=dictionary)
    ldamallet.save(out_file)

   # topic_list  = ldamallet.show_topics(formatted=False, num_topics=ntopics)
    topic_list = [[(term, round(wt, 3)) for term, wt in ldamallet.show_topic(n, topn=20)] for n in range(0, ldamallet.num_topics)]
    topic_df = pd.DataFrame([[term for term, wt in topic] for topic in topic_list], columns = ['Term'+str(i) for i in range(1, 21)], index=['Topic '+str(t) for t in range(1, ldamallet.num_topics+1)]).T
    print(topic_df)
    # print(topic_list)
    # topic_dict = {}
    # for t in topic_list:
    #     word_list = []
    #     for t2 in t[1]:
    #         word_list.append(t2[0])

    #     topic_dict[t[0]]=word_list
    #     print(t[0], word_list)

    topic_df= pd.DataFrame.from_dict(topic_dict,orient='index')
    topic_df.to_csv(path+file_name+"topics_"+str(ntopics)+".csv")

def main():
    path = "/data/madesai/gv-topic-data/"
    data =["all_headlines.pkl"]
    gv_data = "gv_content_by_headline.pkl"
    ntopics =[10]
    #ntopics = [25,40,55]
    gv_topics = [5,10,15]

    for p in data:
        for nt in ntopics:
            print("Finding {} topics in {} file".format(nt, p))
            topic_model(path+p,nt,path)
    #for g in gv_topics:
    #    topic_model(path+gv_data, g)


if __name__ == '__main__':
    main()





        