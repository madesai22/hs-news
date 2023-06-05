import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import file_handling as fh
import preprocess as pp

def load_classifier(path):
    return fh.unpickle_data(path)

def main():
    path = "/data/madesai/student-news-full/"
    gv_articles = path+"/classifier/gunviolence_clf_articles.jsonlist"
    gv_article_list = []
    all_articles = iter(fh.read_jsonlist(path +"articles_clean_ids.jsonlist", ignore_middle = True))
    clf = load_classifier(path+"/classifier/clf.pkl")

    limit = 30
    i = 0 
    while i < limit:
   # for article in all_articles:
        article = next(all_articles)

        headline = article['headline']
        content = article['content']
        text = pp.clean_student_news_article(headline,content) 
        # maybe it doesn't make sense to truncat the guesses?? 

        prediction = clf.predict(text)
        print("headline: {}\n prediction: {}\n".format(headline,prediction))
        i += 1

if __name__ == '__main__':
    main()
    


