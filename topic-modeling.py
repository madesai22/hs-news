import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 
from gensim.parsing.preprocessing import preprocess_string, strip_punctuation, strip_multiple_whitespaces
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from gensim.matutils import corpus2csc
from gensim.models import CoherenceModel
import numpy


i = 0
year_counts = {} # key: year (int) --> value: [n gv headlines, n other] (list)
#df = pd.DataFrame(columns = ['year', 'n gv headlines','n other','total','percent gv'])
pattern = re.compile(r"\b(gun|shooting)\b", re.IGNORECASE)

gv_json_file = []
gv_content = []

#preprocessing filters:
CUSTOM_FILTERS = [lambda x: x.lower(), strip_punctuation, strip_multiple_whitespaces]

#open file and add in gun violence content

with open('/data/madesai/articles_clean.jsonlist') as f:

    for line in f:
        if i <500: 
        

            data = json.loads(line)
            headline = data['headline']
            content = data['content']

            if re.findall(pattern, headline):
                gv_json_file.append(list)
                i += 1
                

                # remove multiple whitespaces, remove punctuation, tokenize 
                preprocessed_content = preprocess_string(content, CUSTOM_FILTERS)
                if i % 100 == 0:
                    print(preprocessed_content[:10])
                gv_content.append(preprocessed_content)

# create corpus
gv_dictionary = Dictionary(gv_content)
gv_corpus = [gv_dictionary.doc2bow(text) for text in gv_content]

# train LDA model
ntopics = 25
lda = LdaModel(gv_corpus, num_topics = ntopics) 
topics = lda.get_document_topics(gv_corpus)

all_topics = []
for j in range(0,ntopics):
    topic_list = lda.get_topic_terms(j, topn=10)
    string_topics = [gv_dictionary[item[0]]for item in topic_list]
    print(string_topics)
    all_topics.append(string_topics)

all_topics_df = pd.DataFrame(all_topics) 
all_topics_df.to_csv("topics.csv")

#perplexity = lda.log_perplexity(lda)
coherence_model_lda = CoherenceModel(model=lda, corpus=gv_corpus, coherence = u_mass)
coherence_lda = coherence_model_lda.get_coherence()
#print("Perplexity = "+ str(perplexity))
print("Coherence ="+str(coherence))


# save gun violence articles with all metadata here: 
with open('/data/madesai/gun-violence-articles_clean.jsonlist', 'w') as file:
    json.dump(gv_json_file)


    

        