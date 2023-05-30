import json
import file_handling as fh 
import preprocess as pp
import sys
import pandas as pd
import os 
import make_plot as mp
import matplotlib.pyplot as plt


def domain_to_year(path_to_article_data, path_to_school_data,path_to_states = "/home/madesai/hs-news/external-data/states.txt",year_start=1999, year_end=2019):
    # read in states
    states_list = fh.read_text_to_list(path_to_states)
    states_dict = {s.strip().lower():0 for s in states_list}
    states_dict.update({'district of columbia':0})
    states_dict.update({-1:0})
    domain_to_states = {}

    year_range = year_end-year_start
    year_to_idx = {y:i for i, y in enumerate(range(year_start,year_end+1))}
    year_to_idx = {y:i for i, y in enumerate(range(year_start,year_end+1))}
    year_to_idx.update({pp.get_invalid_year_value():len(year_to_idx.keys())})
    year_to_idx.update({'total':len(year_to_idx.keys())})
    #year_to_idx.update({'state':len(year_to_idx.keys())})
    year_to_idx.update({'dem_share':len(year_to_idx.keys())})
    print(year_to_idx)
    ncolumns = len(year_to_idx.keys())

    paper_dict = {} # dictionary of domain: list of numbers of articles
    school_data = fh.read_jsonlist(path_to_school_data)
    article_data = fh.read_jsonlist(path_to_article_data)
    for school in school_data: 
        if school['school_type'] == 'middle' or school['is_foreign']== 'true':
            pass
        else:
            domain = school['domain'].lower().strip()
            
            if domain not in paper_dict:
                paper_dict[domain] = [0]*(ncolumns) # plus one for -3000 plus one other for total 
                try:
                    dem_share = school['dem_share']
                    paper_dict[domain][year_to_idx['dem_share']] = dem_share
                except:
                    paper_dict[domain][year_to_idx['dem_share']] = -1
                
                try:
                    state = school['state'].lower()
                except:
                    state = -1
                domain_to_states[domain] = state

    for a in article_data:
        if a['school_type'] != 'middle':

            article_domain = a['domain'].lower().strip()
            article_year = pp.get_year(a['date'])
            if article_year in year_to_idx:
                idx = year_to_idx[article_year]
                if article_domain in paper_dict:
                    paper_dict[article_domain][idx] += 1
                    state = domain_to_states[article_domain]
                    if state in states_dict:
                            states_dict[state] +=1
                else:
                    paper_dict[article_domain] = [0]*(ncolumns)
                    paper_dict[article_domain][idx] += 1
                    paper_dict[article_domain][year_to_idx['dem_share']] = -1

                    if a['geographic'].lower() in states_dict.keys(): 
                        state = a['geographic'].lower()
                        if state in states_dict:
                            states_dict[state] +=1

                    else:
                        state = -1
                    domain_to_states[article_domain] = state


                        #paper_dict[domain][year_to_idx['state']] = states_dict[state]
                    #else:
                    #    paper_dict[domain][year_to_idx['state']] = -1
        
                paper_dict[article_domain][year_to_idx['total']] += 1 # total
    
   #averages_by_year = [0]*(year_range+1) # plus one for -3000
    
    # for y in year_to_idx: # calculate averages; maybe move this to a different function 
    #     year_sum, year_domains = 0, 0 
    #     idx = year_to_idx[y]
    #     for p in paper_dict:
    #         domain_articles_in_year = paper_dict[p]
    #         if domain_articles_in_year != 0:
    #             year_sum += sum(domain_articles_in_year)
    #             year_domains += 1
    #     averages_by_year[idx] = year_sum/year_domains
    return paper_dict, list(year_to_idx.keys()), states_dict#, averages_by_year


def main():
    if not os.path.exists("domains_to_years.pkl"):
        path = "/data/madesai/student-news-full//articles_clean_ids.jsonlist"
        path_to_school = "/data/madesai/student-news-full/school_full_info_with_votes.jsonlist"
        paper_dict, columns, states_dict = domain_to_year(path, path_to_school)
        df = pd.DataFrame.from_dict(paper_dict, orient= 'index', columns=columns)
        df.to_csv('domains_to_years.csv')
        fh.pickle_data(states_dict,'states_dict.pkl')
        fh.pickle_data(df,"domains_to_years.pkl")
        fh.pickle_data(columns,'columns.pkl')

        print("saving df")
    else:
        df = fh.unpickle_data('domains_to_years.pkl')
        columns = fh.unpickle_data('columns.pkl')
        states = fh.unpickle_data('states_dict.pkl')

    data_w_domain = df['total']

    data = data_w_domain.values.tolist() # this is a list where each item is the total n of domains 
    data.sort()
    data_exclude_zeros = [d for d in data if d!=0]

    mp.multiple_box_plot({'all data':data,'excluded zeros':data_exclude_zeros},'Article distribution over schools','/home/madesai/hs-news/plots/data-familiarity/schools-distribution.png')

    n_schools = len(data)
    print(sum(data))
    mean_articles = sum(data)/len(data)

    n_zeros = sum(1 for d in data if d ==0)
    non_zero_sum = sum(data_exclude_zeros)
    non_zero_n = len(data_exclude_zeros)
    non_zero_mean = non_zero_sum/non_zero_n

    dem_share = [i for i in df['dem_share'].values.tolist() if i >0]
    mp.box_plot(dem_share,"dem share",'/home/madesai/hs-news/plots/data-familiarity/voting-distribution.png')

    mp.make_hist(states.values(),states.keys(),'/home/madesai/hs-news/plots/data-familiarity/states.png')
    print(len(states.values()))



    
    print("{} schools, {} average articles per school, {} publish 0 articles, {} average among other schools".format(n_schools,mean_articles,n_zeros, non_zero_mean))
    
    plt.hist(data, bins=40)
    plt.savefig('dom-to-years.png')




if __name__ == '__main__':
    main()

        