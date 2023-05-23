import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
import csv
from datetime import datetime
import requests
import json
import preprocess as pp
import geography_functions as gf
import os 




def make_edited_csv(path_to_events,path_to_voting_data, path_to_fips_file):

    party_dictionary = gf.year_fips_to_party(path_to_voting_data)
    events_df = pd.read_csv(path_to_events)
    events_df = events_df.astype({'year': 'int'})
    events_df = pp.df_slice(events_df,2000,2019,'year')

    #ftz_dict = gf.fips_to_zip_dict(path_to_fips_file)
    years = events_df['year'].tolist()
    election_years = [pp.year_to_election_year(y) for y in years]

    # add fips, zip code, and party to events df 
    latitude = events_df['latitude'].tolist()
    longitude = events_df['longitude'].tolist()

    countyFIPS = [gf.lat_long_to_fips(lat, lon) for lat, lon in zip(latitude,longitude)]
    zip_code = [gf.lat_long_to_zip(lat,lon) for lat, lon in zip(latitude,longitude)]
    #zip_code = [ftz_dict[fips] for fips in countyFIPS]
    party = [party_dictionary[(y,f)][1] for y, f in zip(election_years,countyFIPS)]
    last_party = [party_dictionary[(y-4,f)][1] if y-4>=2000 else "n/a" for y, f in zip(election_years,countyFIPS)]
    next_party = [party_dictionary[(y+4,f)][1] if y+4>=2000 else "n/a" for y, f in zip(election_years,countyFIPS)]

    events_df['countyFIPS'] = countyFIPS
    events_df['zip'] = zip_code
    events_df['party'] = party
    events_df['previous election'] = last_party
    events_df['next election'] = next_party


    events_df.to_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv")
    print("wrote csv")
    return events_df

def main():
    path = "/home/madesai/hs-news/external-data/"
    path_to_events = path+"/Mother_jones_Mass_Shootings_Database_1982_2023.csv"
    path_to_voting_data = path+"mit-election-lab/countypres_2000-2020.csv"
    path_to_fips_file = path+"/ZIP_COUNTY_122021.csv"
    distance = 50 #km 

    if os.path.exists(path+"/mother-jones-edited.csv"):
        events_df = pd.read_csv(path+"/mother-jones-edited.csv")
    else: 
        events_df = make_edited_csv(path_to_events,path_to_voting_data,path_to_fips_file)

    events_df = events_df.astype({'year': 'int'})
    cases = events_df['case'].tolist()
    latitude = events_df['latitude'].tolist()
    longitude = events_df['longitude'].tolist()
    years = events_df['year'].tolist()

    clusters = gf.find_clusters(latitude,longitude,distance)
    match_df = gf.make_cluster_csv(clusters,cases,years)
    match_df.to_csv("/home/madesai/hs-news/external-data/"+str(distance)+"km_event_matches.csv")