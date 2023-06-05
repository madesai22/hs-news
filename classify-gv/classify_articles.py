import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import file_handling as fh
import preprocessing as pp

def load_classifier(path):
    return fh.unpickle_data(path)

def main():
    path = "/data/madesai/student-news-full/"
    gv_articles = path+"/classifier/gunviolence_clf_articles.jsonlist"
    gv_article_list = []
    all_articles = fh.read_jsonlist(path +"articles_clean_ids.jsonlist", ignore_middle = True)
    clf = load_classifier(path+"/classifier/clf.pkl")

    clean_random_sample()


    


