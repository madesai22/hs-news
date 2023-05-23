import processing_events as pe 
import pandas as pd
import file_handling as fh 


events_df = pd.read_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv")
articles = fh.read_jsonlist_random_sample("/data/madesai/articles_clean.jsonlist")
schools_data = fh.read_jsonlist("/data/madesai/school_full_info_with_votes.jsonlist")

zip_codes = events_df['zip']
dates = [pe.get_date(d) for d in events_df['date']] # list of datetime objects
zip_to_date = {zip_codes[i]: dates[i] for i in range(len(zip_codes))}

event_domains = []
papers_jsonlist = []
articles_json = {}


for school in schools_data:
    zipcode = school['zipcode']
    if zipcode in zip_codes:
        print(zipcode, school['type'])
        event_domains.append({school['domain']:zip_to_date[zip_codes]}) # dict of domain to date
        articles_json[zipcode] = []

# json style thing of like [zip code: domain:article list]

for a in articles:
    if a['domain'] in event_domains.keys():
        zipcode = event_domains
        papers_jsonlist.append(a)

# I want them grouped by zip code though, is that possible? 
# like, [event date(s), zip code, domain name, article_list] 
# i think this will require going through the article list as many times as there are 

fh.write_to_jsonlist(papers_jsonlist,"/data/madesai/gv_event_articles.jsonlist")

# the other thing that's important is the date?? of the event 



