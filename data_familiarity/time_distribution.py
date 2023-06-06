import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import make_plot as mp
import pandas as pd



def main():
    path = "/data/madesai/descriptive-statistics/n_high_articles_by_year.csv"
    #college = pd.read_csv("/data/madesai/descriptive-statistics/n_college_articles_by_year.csv")






    mp.plot_articles_by_year(path)

if __name__ == '__main__':
    main()



    