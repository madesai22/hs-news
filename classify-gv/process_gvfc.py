import pandas as pd


# 1- read in csv data
# 2- select articles that are relevant
# 3- preprocess the data


def main():
    path = "/home/madesai/hs-news/external-data/GVFC/GVFC_headlines_and_annotations.csv"
    df = pd.read_csv(path, usecols = ['news_title','Q1_Relevant'])
    df = df[df.Q1_Relevant == 1]
    
    
