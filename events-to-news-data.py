from dateutil.parser import parse
import pandas as pd
import file_handling as fh 

def domain_to_event(schools_data, zip_codes, zip_to_date): 
    # creates a dictionary of {domain:(zip code, date)} for domains which have the same zip code as an event 
    event_domains = []
    for school in schools_data:
        zipcode = school['zipcode']
        if zipcode in zip_codes:
            print(zipcode, school['type'])
            event = (zipcode, zip_to_date[zipcode])
            event_domains.append({school['domain']: event}) 
    return event_domains

# json style thing of like {(zip code, date): {domain:article list}}

def event_to_domain_to_article_list(event_domains, articles, zip_to_date):
    events_to_hlines_by_domain = {}
    for z in zip_to_date: 
        events_to_hlines_by_domain.update({(z,zip_to_date[z]) : [] } )
    for a in articles:
        article_domain = a['domain']
        article_date = parse(a['date'])
        if article_domain in event_domains.keys():
            headline = a['headline']
            event = event_domains[article_domain] 
            if article_domain in events_to_hlines_by_domain[event].keys():
                events_to_hlines_by_domain[event][article_domain].append((headline, article_date))
            else:
                events_to_hlines_by_domain[event].update({article_domain:(headline, article_date)})
    return events_to_hlines_by_domain
    

def main():
    events_df = pd.read_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv")
    #articles = fh.read_jsonlist_random_sample("/data/madesai/articles_clean.jsonlist",.2)
    #fh.pickle_data(articles,'/data/madesai/twenty_percent_articles.pkl')
    #print("random sample generated")

    articles = fh.unpickle_data('/data/madesai/twenty_percent_articles.pkl')
    print("read random sample")
    schools_data = fh.read_jsonlist("/data/madesai/school_full_info_with_votes.jsonlist")

    zip_codes = events_df['zip'].tolist()
    dates = [parse(d) for d in events_df['date']] # list of datetime objects
    #events = [(z,parse(d)) for z, d in zip(zip_codes,dates)]
    zip_to_date = {zip_codes[i]: dates[i] for i in range(len(zip_codes))}
    print(zip_to_date)

    event_domains = domain_to_event(schools_data,zip_codes,zip_to_date)
    events_to_hlines_by_domain = event_to_domain_to_article_list(event_domains,articles,zip_codes)
    for e in events_to_hlines_by_domain:
        domains = events_to_hlines_by_domain[e]
        print("event: {}, ndomains: {}".format(e, len(domains)))
        for d in domains:
            articles = domains[d]
            print("\t domain: {}, articles: {}".format(d, len(articles)))

if __name__ == '__main__':
    main()
