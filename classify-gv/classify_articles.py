import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import file_handling as fh
import preprocess as pp
import pandas as pd



def score_text(df, clf, clf_vectorizer, field='text'): # from https://github.com/kernelmachine/quality-filter/blob/main/data/score.py
    ## score text using quality filter
    df['filter_output']  = clf.predict_proba(clf_vectorizer.transform(tqdm(df[field]))).tolist()
    df['prob_low_quality'] = df.filter_output.apply(lambda x: x[0])
    df['prob_high_quality'] = df.filter_output.apply(lambda x: x[1])
    df = df.drop(['filter_output'], axis=1)
    df['GPT3_included'] = df.prob_high_quality.apply(lambda x: np.random.pareto(9) > (1 - x))

    return df

def score(x, clf, vectorizer): # also from kernelmachine
    # score a single document
    return clf.predict_proba(vectorizer.transform([x]))

def main():
    path = "/data/madesai/student-news-full/"
    all_articles = fh.read_jsonlist(path+"all_articles_no_middle.jsonlist")
    gv_articles = path+"/classifier/gunviolence_clf_articles.jsonlist"
    gv_article_list = []
    #all_articles = pd.read_json(path+"all_articles_no_middle.jsonlist", lines=True).drop_duplicates(subset=['text'])
  
    
    clf = fh.unpickle(path+"/classifier/clf.pkl")
    vectorizer = fh.unpickle(path+"/vectorizer.pkl")
    

    limit = 30
    i = 0 
    while i < limit:
   # for article in all_articles:
        article = next(all_articles)

        headline = article['headline']
        content = article['content']
        text = pp.clean_student_news_article(headline,content) 
        # maybe it doesn't make sense to truncat the guesses?? 

        prediction = score(text,clf,vectorizer)
        print("headline: {}\n prediction: {}\n".format(headline,prediction))
        i += 1

if __name__ == '__main__':
    main()
    


