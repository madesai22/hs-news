import json
import file_handling as fh 
import preprocess as pp
import sys
import pandas as pd

# write a function that will group by year given a conditional? and then write a gv-articles-by-year 
# type thing 

def group_data_by_year(path_to_data, out_file_path, column = None, condition = None):
    year_dict = {} # year: [nfiles, nother, total, percent]?
    count = 0
    nfile_idx, nother_idx, total_idx = range(0,3)
    with open(path_to_data) as f:
        if count <500:
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
        print(year_dict[y][nfile_idx])
        print(year_dict[y][total_idx])
        pcent = (year_dict[y][nfile_idx])(year_dict[y][total_idx])*100
        year_dict[y].append(pcent)
    df = pd.DataFrame.from_dict(year_dict, orient='index', columns = ['nfiles','nother','total','percent'])
    df.to_csv(out_file_path)

def quick_look(path_to_file, column, condition):
    n_condition = 0 
    with open(path_to_file) as f:
        for line in f:
            if json.loads(line)[column] == condition:
                n_condition+=1

    print("{} {}".format(n_condition, condition))

def main():
    path = '/data/madesai/articles_clean.jsonlist'
    json_column = 'school_type'
    select_for = ['high','middle','college']
    for c in select_for:
        path_to_outfile = '/data/madesai/descriptive-statistics/n_'+c+'l_articles_by_year.csv'
        print(c)
        group_data_by_year(path,path_to_outfile,column=json_column,condition=c)



if __name__ == '__main__':
    main()

        
            

    


