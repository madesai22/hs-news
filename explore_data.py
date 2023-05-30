import json
import file_handling as fh 
import preprocess as pp
import sys
import pandas as pd
from tqdm.auto import tqdm
import matplotlib.pyplot as plt

# write a function that will group by year given a conditional? and then write a gv-articles-by-year 
# type thing 
def domain_to_year(path_to_article_data, path_to_school_data,year_start=1999, year_end=2019):
    year_range = year_end-year_start
    year_to_idx = {y:i for i, y in enumerate(range(year_start,year_end+1))}
    year_to_idx.update({pp.get_invalid_year_value():year_range+1})

    paper_dict = {} # dictionary of domain: list of numbers of articles
    school_data = fh.read_jsonlist(path_to_school_data)
    article_data = fh.read_jsonlist(path_to_article_data)
    for school in school_data: 
        if school['school_type'] == 'middle':
            pass
        else:
            domain = school['domain']
            if domain not in paper_dict:
                paper_dict[domain] = [0]*(year_range+2) # plus one for -3000 plus one other for total 
    for a in article_data:
        article_domain = a['domain']
        article_year = pp.get_year(a['date'])
        if article_year in year_to_idx:
            idx = year_to_idx[article_year]
            if article_domain in paper_dict:
                paper_dict[article_domain][idx] += 1
            else:
                paper_dict[article_domain] = [0]*(year_range+2)
                paper_dict[article_domain][idx] += 1
            paper_dict[article_domain][-1] += 1 # total
    
    averages_by_year = [0]*(year_range+1) # plus one for -3000
    
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




def group_data_by_year(path_to_data, out_file_path, column = None, condition = None):
    year_dict = {} # year: [nfiles, nother, total, percent]?
    count = 0
    nfile_idx, nother_idx, total_idx = range(0,3)
    with open(path_to_data) as f:
        
        for line in f: 
            sys.stdout.write("Seen {} articles\r".format(count))
            #sys.stdout.write("Seen %.2f percent of articles\r" %(count/nfiles*100))
            sys.stdout.flush()
            count +=1
            
            data = json.loads(line)
            if condition and column:
                take_file = data[column] == condition
            else:
                take_file == True

            if data['date']:
                year = pp.get_year(data['date'])
            else:
                year =  3000
            
            if year in year_dict:
                year_dict[year][total_idx] += 1
                if take_file:
                    year_dict[year][nfile_idx] += 1
                else:
                    year_dict[year][nother_idx] += 1
            else:
                if take_file:
                    year_dict[year] = [1,0,1]
                else:
                    year_dict[year] = [0,1,1]
    for y in year_dict:
        num, denom  = year_dict[y][nfile_idx], year_dict[y][total_idx]
        pcent = num/denom*100
        year_dict[y].append(pcent)
    df = pd.DataFrame.from_dict(year_dict, orient='index', columns = ['nfiles','nother','total','percent'])
    df.to_csv(out_file_path)

def quick_look_column_jsonlist(path_to_file, column, condition=None, printn=True, printexamples = False, nexamples = 1000):
    n_condition = 0 
    count = 0 
    with open(path_to_file) as f:
        for line in f:
            data = json.loads(line)[column]
            if condition:
                if  data == condition:
                    if printn: 
                        n_condition+=1
                    if printexamples and n_condition < nexamples:
                        print(data)
            else:
                if printn: 
                    n_condition+=1
                if printexamples and count < nexamples:
                    print(data)
            count +=1
    if printn:
        print("{} {}".format(n_condition, condition))

def quick_look_json(path_to_file, column, condition=None, printn=True, printexamples = False, nexamples = 1000):
    d = fh.read_json(path_to_file)
    good_articles = 0 
    bad_articles = 0
    for item in d:
        article = d[item]
        if article[column] == condition:
            good_articles += 1
        else:
            bad_articles += 1
            print(article)
    print("{} good and {} bad articles".format(good_articles,bad_articles))
        #if i <nexamples:
        #    print(d[item])

def add_id(path_to_file, path_to_out_file):
    new_json = []
    article_id = 0
    with open(path_to_file) as f:
        for line in f:
            data = json.loads(line)
            article_id += 1 
            data.update({'article_id':article_id})
            new_json.append(data)
    fh.write_to_jsonlist(new_json,path_to_out_file)



            

def main():
    path = "/data/madesai/student-news-full//articles_clean_ids.jsonlist"
    path_to_school = "/data/madesai/student-news-full/school_full_info_with_votes.jsonlist"
    paper_dict = domain_to_year(path, path_to_school)
    years = [str(i) for i in range(1999,2020)]
    years.insert(0, str(-3000))
    years.append("total")
    df = pd.DataFrame.from_dict(paper_dict, orient= 'index', columns=[years])
    fh.pickle_data(df,"domains_to_years.pkl")
    print("saving df")
    data = df['total']
    plt.hist(data)
    plt.savefig('domain-to-years.png')
    
    




    # path = "/data/madesai/mfc_v4.0/guncontrol/guncontrol_all_with_duplicates.json"
    # data = fh.read_json(path)
    # i = 0 
    # for d in data:
    #     if i < 10:
    #         print(data[d])
    #     i +=1
    #path = '/data/madesai/student-news-full/articles_clean.jsonlist'
    #out_path = '/data/madesai/student-news-full/articles_clean_ids.jsonlist'
    #add_id(path, out_path)

    #quick_look_column_jsonlist(out_path,column = 'article_id',printexamples=True)
    # path = "/data/madesai/student-news-full/classifier/results.pkl"
    # results = fh.unpickle_data(path)
    # test_acc = results['test_accuracy']
    # test_f1 = results['test_f1']
    # print(test_acc, test_f1)
    # path = "/data/madesai/mfc_v4.0/guncontrol/guncontrol_labeled.json"
    # path = "/data/madesai/filter_data/test.jsonl"
    # dev = pd.read_json(path, lines=True)
    # tqdm.pandas()
    # a = dev.loc[dev.label == 0].text.progress_apply(lambda x: len(x.split())).sum()
    # print(a)
    # print(dev.head(10))

    # json_column = 'school_type'
    # select_for = ['high','middle','college']
    # for c in select_for:
    #     path_to_outfile = '/data/madesai/descriptive-statistics/n_'+c+'l_articles_by_year.csv'
    #     print(c)
    #     group_data_by_year(path,path_to_outfile,column=json_column,condition=c)

    #quick_look_json(path,column = 'irrelevant', condition = 0, printexamples=False,printn=False,nexamples=5)



if __name__ == '__main__':
    main()

        
            

    


