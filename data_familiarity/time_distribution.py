import sys
sys.path.insert(1, '/home/madesai/hs-news/processing')
import make_plot as mp


def main():

    path = "/data/madesai/descriptive-statistics/n_college_hs_by_year.csv"
    mp.plot_articles_by_year(path)

if __name__ == '__main__':
    main()



    