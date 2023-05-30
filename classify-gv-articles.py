import time
import file_handling as fh
import preprocess as pp
import pandas as pd
from tqdm import tqdm
import random
import os
import re
from hyperparameters import (SEARCH_SPACE,BEST_HPS, HyperparameterSearch,
                             RandomSearch)
from sklearn.feature_extraction.text import (CountVectorizer, TfidfVectorizer, HashingVectorizer)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score


def select_relevant_articles(data, label): # works for the mfc data
    clean = []
    for a in data: # use a as key?
        article = data[a]
        if article['irrelevant'] == 0: # releavant article
            text = article['text']
            pattern = r"gun[0-9]+"
            
            text = pp.remove_whitespaces(text)
            text = pp.strip_punctuation(text).lower().strip()
            text = re.sub(pattern, "",text)
            clean.append({'key':a, 'text': text, 'label': label})
    return clean

def clean_random_sample(data, label): # works for student news articles
    word_lengths = []
    clean = []
    for line in data:
        headline = line['headline']
        headline = pp.remove_whitespaces(headline)
        headline = pp.strip_punctuation(headline).lower().strip()
        text = headline.split()
        #paragraphs = pp.pre_process_paragraph(line['content'])
        paragraphs = pp.pre_process_sentence(line['content']) # really this is sentences 
        n_paragraphs = len(paragraphs)
        key = line['article_id']
  
        paragraph_count = 0 
        while len(text) < 225 and paragraph_count < n_paragraphs:
            next_paragraph = paragraphs[paragraph_count]
            paragraph_count += 1 
            text.extend(next_paragraph.split())
        text = " ".join(text)
        clean.append({'key':key, 'text': text, 'label': label}) 
        word_lengths.append(len(text))
    print("average words = {}".format(sum(word_lengths)/len(word_lengths)))
    return clean   


def train_lr(train,
             test,
             search_space): # from https://github.com/kernelmachine/quality-filter/blob/main/lr/train.py
    master = train
    space = HyperparameterSearch(**search_space)
    sample = space.sample()
    if sample.pop('stopwords') == 1:
        stop_words = 'english'
    else:
        stop_words = None
    weight = sample.pop('weight')
    if weight == 'binary':
        binary = True
    else:
        binary = False
    ngram_range = sample.pop('ngram_range')
    ngram_range = sorted((int(x) for x in ngram_range.split()))
    ngram_range = tuple(ngram_range)
    if weight == 'tf-idf':
        vect = TfidfVectorizer(stop_words=stop_words,
                               lowercase=True,
                               ngram_range=ngram_range)
    elif weight == 'hash':
        vect = HashingVectorizer(stop_words=stop_words, lowercase=True, ngram_range=ngram_range)
    else:
        vect = CountVectorizer(binary=binary,
                               stop_words=stop_words,
                               lowercase=True,
                               ngram_range=ngram_range)
    start = time.time()
    vect.fit(tqdm(master.text, desc="fitting data", leave=False))
    X_train = vect.transform(tqdm(train.text, desc="transforming training data",  leave=False))

    if test is not None:
        X_test = vect.transform(tqdm(test.text, desc="transforming test data",  leave=False))

    sample['C'] = float(sample['C'])
    sample['tol'] = float(sample['tol'])
    classifier = LogisticRegression(**sample)
    classifier.fit(X_train, train.label)
    end = time.time()
    for k, v in sample.items():
        if not v:
            v = str(v)
        sample[k] = [v]
    res = pd.DataFrame(sample)
    preds = classifier.predict(X_train)
    if test is not None:
        test_preds = classifier.predict(X_test)
    res['dev_f1'] = f1_score(train.label, preds, average='macro')
    if test is not None:
        res['test_f1'] = f1_score(test.label, test_preds, average='macro')
    if test is not None:
        res['test_accuracy'] = classifier.score(X_test, test.label)
    res['dev_accuracy'] = classifier.score(X_train, train.label)
    res['training_duration'] = end - start
    res['ngram_range'] = str(ngram_range)
    res['weight'] = weight
    res['stopwords'] = stop_words
    return classifier, vect, res

        



def main():
    TOTAL_GV_IN_MFC = 9018
    TEST_SPLIT = 0.2
    N_TEST = int(TOTAL_GV_IN_MFC*TEST_SPLIT)
    path = "/data/madesai/student-news-full/classifier/"
    test_file = path+"test.jsonlist"
    train_file = path+"/train.jsonlist"
    b = True


    if b: #not os.path.exists(test_file) or not os.path.exists(train_file):
        gv_file = fh.read_json("/data/madesai/mfc_v4.0/guncontrol/guncontrol_labeled.json")
        gv_articles = select_relevant_articles(gv_file, label=1)
        random.shuffle(gv_articles)
        print("read in gun control articles")

        
        if not os.path.exists(path+"random_sample.pkl"):
            random_student_sample = fh.read_jsonlist_random_sample("/data/madesai/student-news-full//articles_clean_ids.jsonlist",size = TOTAL_GV_IN_MFC)
            fh.pickle_data(random_student_sample,path+"random_sample.pkl")
            print("saving random sample")
        else:
            random_student_sample = fh.unpickle_data(path+"random_sample.pkl")
            print("read in random sample")
            

        non_gv_articles = clean_random_sample(random_student_sample, label=0)
        random.shuffle(non_gv_articles)
        print("read in random sample")

        test = gv_articles[:N_TEST] +  non_gv_articles[:N_TEST]
        test = pd.DataFrame(test)
        for i in range(10):
            print(random.choice(gv_articles))
            print(random.choice(non_gv_articles))

        train = gv_articles[N_TEST:] + non_gv_articles[N_TEST:]
        train = pd.DataFrame(train)



        fh.pickle_data(test, test_file)
        fh.pickle_data(train, train_file)
        
    else:
        train = fh.unpickle_data(train_file)
        test = fh.unpickle_data(test_file)
    
    print("training model ...")
    clf, vectorizer, results = train_lr(test,train,SEARCH_SPACE)
    fh.pickle_data(clf,path+"/clf.pkl")
    fh.pickle_data(vectorizer, path+"/vectorizer.pkl")
    fh.pickle_data(results,path+"/results.pkl")

    for (columnName, columnData) in results.iteritems():
        print('{} : {}'.format(columnName,columnData))
    


    

if __name__ == '__main__':
    main()
