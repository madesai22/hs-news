import time
import file_handling as fh
import preprocess as pp
import pandas as pd
from tqdm import tqdm
import random
import os

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
            clean.append({'key':a, 'text': text, 'label': label})
    return clean

def clean_random_sample(data, label): # works for student news articles
    clean = []
    for line in data:
        text = line['headline'].split()
        paragraphs = pp.pre_process_paragraph(line['content'])
        print(paragraphs)
        n_paragraphs = len(paragraphs)
        key = line['article_id']
  
        paragraph_count = 0 
        while len(text) < 225 and paragraph_count < n_paragraphs:
            next_paragraph = paragraphs[paragraph_count]
            paragraph_count += 1 
            text.append(next_paragraph.split())
        print(text) 
        print("\n\n\n")
        clean.append({'key':key, 'text': text, 'label': label}) 
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
    ngram_range = sorted([int(x) for x in ngram_range.split()])
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
    if test is not None:
        test_preds = classifier.predict(X_test)
    if test is not None:
        res['test_f1'] = f1_score(test.label, test_preds, average='macro')
    if test is not None:
        res['test_accuracy'] = classifier.score(X_test, test.label)
    res['training_duration'] = end - start
    res['ngram_range'] = str(ngram_range)
    res['weight'] = weight
    res['stopwords'] = stop_words
    return classifier, vect, res

        



def main():
    TOTAL_GV_IN_MFC = 9018
    TEST_SPLIT = 0.2
    N_TEST = int(TOTAL_GV_IN_MFC*TEST_SPLIT)
    test_file = "/data/madesai/student-news-full/classifier/test.jsonlist"
    train_file = "/data/madesai/student-news-full/classifier/train.jsonlist"

    if not os.path.exists(test_file) or not os.path.exists(train_file):
        gv_file = fh.read_json("/data/madesai/mfc_v4.0/guncontrol/guncontrol_labeled.json")
        gv_articles = random.shuffle(select_relevant_articles(gv_file, label=1))
        print("read in gun control articles")

        random_student_sample = fh.read_jsonlist_random_sample("/data/madesai/student-news-full/articles_clean_ids.jsonlist",size = TOTAL_GV_IN_MFC)
        non_gv_articles = random.shuffle(clean_random_sample(random_student_sample, label=0))
        print("read in random sample")

        test = gv_articles[:N_TEST] +  non_gv_articles[:N_TEST]
        train = gv_articles[N_TEST:] + non_gv_articles[N_TEST:]
        fh.pickle_data(test, test_file)
        fh.pickle_data(train, train_file)
        
    else:
        train = fh.unpickle_data(train_file)
        test = fh.unpickle_data(test_file)
    
    print("training model ...")
    clf, vectorizer, results = train_lr(test,train,SEARCH_SPACE)
    fh.pickle_data(clf,"/data/madesai/student-news-full/classifier/clf.pkl")
    fh.pickle_data(vectorizer, "/data/madesai/student-news-full/classifier/vectorizer.pkl")
    fh.pickle_data(results,"/data/madesai/student-news-full/classifier/results.pkl")
    print(results)


    

if __name__ == '__main__':
    main()
