import json
import re
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd 
from gensim.parsing.preprocessing import preprocess_string
from gensim.corpora.dictionary import Dictionary
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
if i < 500: 
    with open('/data/madesai/articles_clean.jsonlist'):
    

        for line in f:

            data = json.loads(line)
            headline = data['headline']
            content = data['content']

            if re.findall(pattern, headline):
                gv_json_file.append(list)
                i += 1

                # remove multiple whitespaces, remove punctuation, tokenize 
                gv_content.append(preprocess_string(content, CUSTOM_FILTERS))

# create corpus
gv_dictionary = Dictionary(gv_content)
gv_corpus = [gv_dictionary.doc2bow(text) for text in gv_content]

# train LDA model
lda = LdaModel(gv_corpus, num_topics = 25) 
topics = lda.get_document_topics(gv_corpus)
topics_numpy = gensim.matutils.corpus2csc(topics).toarray()
all_topics_df = pd.DataFrame(all_topics_numpy)
print(all_topics_df) 
all_topics_df.to_csv("topics.csv")

perplexity = lda.log_perplexity(lda)
coherence_model_lda = CoherenceModel(model=lda, corpus=gv_corpus, coherence = u_mass)
coherence_lda = coherence_model_lda.get_coherence()
print("Perplexity = "+ str(percent))
print("Coherence ="+str(coherence))


# save gun violence articles with all metadata here: 
with open('/data/madesai/gun-violence-articles_clean.jsonlist', 'w') as file:
    json.dump(gv_json_file)


    

        