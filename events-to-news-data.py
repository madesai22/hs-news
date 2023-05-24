from dateutil.parser import parse
import pandas as pd
import file_handling as fh 
import preprocess as pp
import geography_functions as gf
import os
import re

def domain_to_event(schools_data, event_states, zip_codes, zip_to_date, max_distance = 0): 
    # creates a dictionary of {domain:(zip code, date)} for domains which have the same zip code as an event 
    event_domains = {}
    state_domains = {}
    for school in schools_data: 
        if school['school_type'] == 'middle':
            pass
        else:
            school_state = school['state']
        
            school_zipcode = int(school['zipcode'])
            if max_distance == 0:
                if school_zipcode in zip_codes:
                    event_zip = school_zipcode
                    event = (event_zip, zip_to_date[event_zip])
                    event_domains.update({school['domain']: event})
            else:
                for i, e_state in enumerate(event_states):
                    if school_state == e_state.strip():
                        event_zip = zip_codes[i]
                        event = (event_zip, zip_to_date[event_zip])
                        distance = gf.km_between_zip(school_zipcode, event_zip)
                        state_domains.update({school['domain']: event})
                        if distance < max_distance and distance > 0:
                            print(event_zip, school_zipcode, school['school_type'], school['domain'])
                            
                            event_domains.update({school['domain']: event})
            fh.pickle_data(state_domains,'/data/madesai/schools_to_events/state_domains.pkl')
    return event_domains



def event_to_domain_to_article_list(event_domains, articles, zip_to_date, max_distance=0):
    # creates dictionary of {(zip code, date): {domain: [headlines]}}
    events_to_hlines_by_domain = {}
    for z in zip_to_date.keys(): 
        events_to_hlines_by_domain.update({(z,zip_to_date[z]) : [] } )
    for a in articles:
        article_domain = a['domain']
        article_date = pp.get_date(a['date'])

        if article_domain in event_domains.keys():
            headline = a['headline']
            event = event_domains[article_domain] 
            if article_domain in events_to_hlines_by_domain[event].keys():
                events_to_hlines_by_domain[event][article_domain].append((headline, article_date))
            else:
                events_to_hlines_by_domain[event].update({article_domain:(headline, article_date)})

    
    return events_to_hlines_by_domain
    

def main():

    out_path = '/data/madesai/schools_to_events/'
    if os.path.exists('/data/madesai/twenty_percent_articles.pkl'):
        articles = fh.unpickle_data('/data/madesai/twenty_percent_articles.pkl')
        print("read random sample")
    else:
        #articles = fh.read_jsonlist_random_sample("/data/madesai/articles_clean.jsonlist",.2)
        articles = fh.read_jsonlist_random_sample("/data/madesai/articles_clean.jsonlist")
        fh.pickle_data(articles,'/data/madesai/twenty_percent_articles.pkl')
        print("random sample generated")

    events_df = pd.read_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv",usecols=['zip','date','location'])
    schools_data = fh.read_jsonlist("/data/madesai/school_full_info_with_votes.jsonlist")
    print("read school data")

    zip_codes = events_df['zip'].tolist()
    states = [l.strip().split(',')[1] for l in events_df['location']]

    dates = [parse(d).strftime("%m/%d/%Y") for d in events_df['date']] # list of datetime objects
    zip_to_date = {zip_codes[i]: dates[i] for i in range(len(zip_codes))}

    max_distance = 24 
    if 1>2:#os.path.exists(out_path+'rs_domain_to_event_distance_'+str(max_distance)+".pkl"):
        event_domains = fh.unpickle_data(out_path+'/rs_domain_to_event_distance_'+str(max_distance)+".pkl")
    else:
        event_domains = domain_to_event(schools_data,states,zip_codes,zip_to_date, max_distance=32)
        fh.pickle_data(event_domains,out_path+"/rs_domain_to_event_distance_"+str(max_distance)+".pkl")
    print("calculated distances")
    
    if 1>2:#os.path.exists("/data/madesai/schools_to_events/rs_events_to_hlines_distance_"+str(max_distance)+".pkl"):
        events_to_hlines_by_domain = fh.unpickle_data(out_path+ "rs_events_to_hlines_distance_"+str(max_distance)+".pkl")
    else:
        events_to_hlines_by_domain = event_to_domain_to_article_list(event_domains,articles,zip_to_date,max_distance)
        fh.pickle_data(events_to_hlines_by_domain,out_path+"/rs_events_to_hlines_distance_"+str(max_distance)+".pkl")
    print("found headlines")
    
    # print data
    for e in events_to_hlines_by_domain:
        domains = events_to_hlines_by_domain[e]
        print("event: {}, ndomains: {}".format(e, len(domains)))
        for d in domains:
            articles = domains[d]
            print("\t domain: {}, articles: {}".format(d, len(articles)))

if __name__ == '__main__':
    main()
