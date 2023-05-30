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
    states_dict = {s:i for i,s in enumerate(states_list)}

    year_range = year_end-year_start
    year_to_idx = {y:i for i, y in enumerate(range(year_start,year_end+1))}
    year_to_idx.update({pp.get_invalid_year_value():year_range+1})
    year_to_idx.update({'state':year_range+2})
    year_to_idx.update({'dem_share':year_range+3})

    paper_dict = {} # dictionary of domain: list of numbers of articles
    school_data = fh.read_jsonlist(path_to_school_data)
    article_data = fh.read_jsonlist(path_to_article_data)
    for school in school_data: 
        if school['school_type'] == 'middle' or school['is_foreign']== 'true':
            pass
        else:
            domain = school['domain'].lower().strip()
            
            if domain not in paper_dict:
                paper_dict[domain] = [0]*(year_range+3) # plus one for -3000 plus one other for total 
                try:
                    dem_share = school['dem_share']
                    paper_dict[domain][year_to_idx['dem_share']] = dem_share
                except:
                    paper_dict[domain][year_to_idx['dem_share']] = -1

                state = school['state']
                if state in states_dict.keys():
                    paper_dict[domain][year_to_idx['state']] = states_dict[state]
                else:
                    paper_dict[domain][year_to_idx['state']] = -1
                

    for a in article_data:
        article_domain = a['domain'].lower().strip()
        article_year = pp.get_year(a['date'])
        if article_year in year_to_idx:
            idx = year_to_idx[article_year]
            if article_domain in paper_dict:
                paper_dict[article_domain][idx] += 1
            else:
                print("SLFJSLDFJSDLKFJSL")
                paper_dict[article_domain] = [0]*(year_range+3)
                paper_dict[article_domain][idx] += 1
                
            paper_dict[article_domain][-1] += 1 # total
    
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
    return paper_dict#, averages_by_year


def main():
    if True:#not os.path.exists("domains_to_years.pkl"):
        path = "/data/madesai/student-news-full//articles_clean_ids.jsonlist"
        path_to_school = "/data/madesai/student-news-full/school_full_info_with_votes.jsonlist"
        paper_dict = domain_to_year(path, path_to_school)
        years = [str(i) for i in range(1999,2020)]
        years.insert(0, str(-3000))
        years.append("total")
        df = pd.DataFrame.from_dict(paper_dict, orient= 'index', columns=[years])
        df.to_csv('domains_to_years.csv')
        fh.pickle_data(df,"domains_to_years.pkl")

        print("saving df")
    else:
        df = fh.unpickle_data('domains_to_years.pkl')

    data_w_domain = df['total']
    #print(data_w_domain)
    
    data = [i[0] for i in  data_w_domain.values.tolist()] # this is a list where each item is the total n of domains 
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


    
    print("{} schools, {} average articles per school, {} publish 0 articles, {} average among other schools".format(n_schools,mean_articles,n_zeros, non_zero_mean))
    
    plt.hist(data, bins=40)
    plt.savefig('domain-to-years.png')




if __name__ == '__main__':
    main()

        