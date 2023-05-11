import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_multiple_whitespaces, remove_stopwords
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.models.wrappers.ldamallet import LdaMallet
from gensim.matutils import corpus2csc
from gensim.models import CoherenceModel
import numpy
import pickle

path_to_mallet_binary = "/home/madesai/Mallet/bin/mallet/"

i = 0
year_counts = {} # key: year (int) --> value: [n gv headlines, n other] (list)
#df = pd.DataFrame(columns = ['year', 'n gv headlines','n other','total','percent gv'])



gv_json_file = []
gv_content = []
all_content = []

#preprocessing filters:
CUSTOM_FILTERS = [lambda x: x.lower(), strip_punctuation, strip_multiple_whitespaces, remove_stopwords]

#open file and add in gun violence content

with open('/data/madesai/articles_clean.jsonlist') as f:

    for line in f:
       # if i <500: 
        

        data = json.loads(line)
        headline = data['headline']
        content = data['content']

        preprocessed_all_content = preprocess_string(content, CUSTOM_FILTERS)
        all_content.append(preprocessed_all_content)
        march_match = re.findall(r"\bMarch for Our Lives\b|\bStudents Demand Action\b|\bNational School Walkout\b|\bsecond amendment\b|\bNRA\b|\bNever Again MSD\b|\b2nd amendment\b|\bstand for the second\b",headline, re.IGNORECASE)
        gun_match = re.findall(r"\b(gun)\b|\b(firearm)\b", headline, re.IGNORECASE)
        sports_pattern = r"ball|lacrosse|score|point|film|movie|hoop|win|soccer|court|hockey|polo|champ|game|varsity|lax|trophy|sweep|flu|vaccin|photo|star|playoff|competition|finals"
        sports_match = re.findall(sports_pattern, headline, re.IGNORECASE)
        shooting_match = re.findall(r"\b(?!(?:shot[\s-]?put(?:t|s)?(?:ter)?\b))(?:shoot|shot)\w*\b", headline, re.IGNORECASE)
        long_shot_match = re.findall(r"(\blong\s+shot\w*)|(call\s+the\s+shot\w*)", headline, re.IGNORECASE)
        shooter_likely = re.findall(r"\b(?:active|mass|school)\s+(?:shoot|shot)\w*\b", headline, re.IGNORECASE)


        if gun_match or shooter_likely or march_match or (shooting_match and not sports_match and not long_shot_match):
            if i%100 == 0:
                print(headline)
            gv_json_file.append(line)
            i += 1
            

            # remove multiple whitespaces, remove punctuation, tokenize 
            preprocessed_content = preprocess_string(content, CUSTOM_FILTERS)
            if i % 300 == 0:
                print(preprocessed_content[:10])
            gv_content.append(preprocessed_content)

print("***")
# create corpus
gv_dictionary = Dictionary(gv_content)
gv_corpus = [gv_dictionary.doc2bow(text) for text in gv_content]

# create whole corpus 
all_dictionary = Dictionary(all_content)
all_corpus = [all_dictionary.doc2bow(text) for text in all_content]

# train LDA model
ntopics = 10
ldamallet = LdaMallet(path_to_mallet_binary, corpus=gv_corpus, num_topics=ntopics, id2word=gv_dictionary)
pprint(ldamallet.show_topics(formatted=False))

#lda = LdaModel(gv_corpus, num_topics = ntopics) 
topics = lda.get_document_topics(gv_corpus)

# # train whole LDA
# ntopics_all = 45
# lda_all = LdaModel(all_corpus, num_topics = ntopics_all) 
# topics = lda.get_document_topics(all_corpus)


# all_topics = []
# for j in range(0,ntopics):
#     topic_list = lda.get_topic_terms(j, topn=10)
#    #string_topics = [(gv_dictionary[item[0]], item[1]) for item in topic_list]
#     string_topics = [gv_dictionary[item[0]] for item in topic_list]
#     print(string_topics)
#     all_topics.append(string_topics)

# all_topics_df = pd.DataFrame(all_topics) 
# all_topics_df.to_csv("topics_"+str(ntopics)+".csv")

# # total topics 
# all_data_topics = []
# for j in range(0,ntopics):
#     topic_list_all = lda_all.get_topic_terms(j, topn=10)
#     string_topics = [all_dictionary[item[0]] for item in topic_list_all]
#     all_data_topics.append(string_topics)
# all_data_topics_df = pd.DataFrame(all_data_topics) 
# all_data_topics_df.to_csv("all_data_topics_"+str(ntopics_all)+".csv")

# #perplexity = lda.log_perplexity(lda)
# coherence_model_lda = CoherenceModel(model=lda, dictionary = gv_dictionary, corpus=gv_corpus, coherence="u_mass")
# coherence_lda = coherence_model_lda.get_coherence()
# #print("Perplexity = "+ str(perplexity))
# print("Coherence ="+str(coherence_lda))


# # save gun violence articles with all metadata here: 
# with open('/data/madesai/gun-violence-articles_clean.jsonlist', 'w') as file:
#     json.dumps(gv_json_file)


    

        