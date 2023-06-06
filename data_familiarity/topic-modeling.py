from gensim.models.wrappers.ldamallet import LdaMallet
from gensim.matutils import corpus2csc
from gensim.models import CoherenceModel
from gensim.corpora.dictionary import Dictionary
from gensim.test.utils import datapath
import numpy
sys.path.insert(1, '/home/madesai/hs-news/processing')
import file_handling as fh
import pandas as pd


def topic_model(path_to_file, ntopics,path_to_save_file):

    path_to_mallet_binary = "/home/madesai/Mallet/bin/mallet"

    path_list = path_to_file.split("/")[:-1]
    path = "/".join(path_list)+"/"
    file_name = path_list[-1].split(".")[0]
    out_file_name = path_to_save_file+"lda_"+file_name+"_"+str(ntopics)
    out_file = datapath(out_file_name)

    content = fh.unpickle_data(path_to_file)
    dictionary = Dictionary(content)
    corpus = [dictionary.doc2bow(text) for text in content]

    ldamallet = LdaMallet(path_to_mallet_binary, corpus=corpus, num_topics=ntopics, id2word=dictionary)
    ldamallet.save(out_file)

    topic_list  = ldamallet.show_topics(formatted=False, topn=ntopics)
    topic_dict = {}
    for t in topic_list:
        word_list = []
        for t2 in t[1]:
            word_list.append(t2[0])

        topic_dict[t[0]]=word_list
        print(t[0], word_list)

    topic_df= pd.DataFrame.from_dict(topic_dict,orient='index')
    topic_df.to_csv(path+file_name+"topics_"+str(ntopics)+".csv")

def main():
    path = "/data/madesai/gv-topic-data/"
    data =["all_headlines.pkl"]
    gv_data = "gv_content_by_headline.pkl"
    ntopics = [25,40,55]
    gv_topics = [5,10,15]

    for p in data:
        for nt in ntopics:
            print("Finding {} topics in {} file".format(nt, p))
            topic_model(path+p,nt,path)
    #for g in gv_topics:
    #    topic_model(path+gv_data, g)


if __name__ == '__main__':
    main()





        