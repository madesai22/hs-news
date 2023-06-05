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
    all_articles = iter(fh.read_jsonlist(path+"all_articles_no_middle.jsonlist"))
    print('read in articles')
    #gv_articles = path+"/classifier/gunviolence_clf_articles.jsonlist"
    #gv_article_list = []    
    gv_articles = []#pd.DataFrame(columns = ['text','gv_score'])
    other_articles = []
    #all_articles = pd.read_json(path+"all_articles_no_middle.jsonlist", lines=True).drop_duplicates(subset=['text'])
  
    
    clf = fh.unpickle_data(path+"/classifier/clf.pkl")
    vectorizer = fh.unpickle_data(path+"/classifier/vectorizer.pkl")
    print("opened classifier")
    

    limit = 300
    i = 0 
    #while i< limit:
    for article in all_articles:
        sys.stdout.write("Seen %d articles\r" %(i))
        sys.stdout.flush()
        i += 1
        article = next(all_articles)

        headline = article['headline']
        content = article['content']
        text = pp.clean_student_news_article(headline,content) 
        # maybe it doesn't make sense to truncat the guesses?? 

        prediction = score(text,clf,vectorizer)
        #print(type(prediction[0]))
        gv_pred = prediction[0][1]
        other_pred = prediction[0][0]
        
        if gv_pred > other_pred:
            gv_articles.append({'text': headline, 'gv_score': gv_pred})

        else:
            other_articles.append({'text': headline, 'gv_score': other_pred})

    gv_df = pd.DataFrame(gv_articles)
    other_df = pd.DataFrame(other_articles)

    gv_df.to_csv('gv_classify_explore.csv')
    other_df.to_csv('other_classify_explore.csv')

if __name__ == '__main__':
    main()
    


