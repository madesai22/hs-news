import file_handling as fh

def select_relevant_articles(data, label): # works for the mfc data
    clean = {}
    for a in data: # use a as key?
        article = data[a]
        if article['irrelevant'] == 0: # releavant article
            text = article['text']
            clean.update({'key':a, 'text': text, 'label': label})
    return clean

def clean_random_sample(data, label): # works for student news articles
    for line in data:
        headline = line['headline']
        content = line['content']
        paragraphs = content.split('\n\n')


def main():
    gv_file = fh.read_json("/data/madesai/mfc_v4.0/guncontrol/guncontrol_labeled.json")
    gv_articles = select_relevant_articles(gv_file, label=1)

    random_student_sample = fh.read_jsonlist_random_sample("/data/madesai/student-news-full/gun-violence-articles_clean.jsonlist",size = 9018)

if __name__ == '__main__':
    main()
