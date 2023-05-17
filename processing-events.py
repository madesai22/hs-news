import pandas as pd
from geopy.geocoders import Nominatim
import csv


def get_county_fips(latitude, longitude):
    geolocator = Nominatim(user_agent="my-application")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    county_fips = address.get('county_fips')

    return county_fips

def create_party_dictionary(csv_file):
    party_dict = {}
    
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            year = row['year']
            county_fips = row['county_fips']
            party = row['party']
            
            key = (year, county_fips)
            party_dict[key] = party
    
    return party_dict

path_to_events = "/home/madesai/hs-news/external-data/Mother_jones_Mass_Shootings_Database_1982_2023.csv"
path_to_voting_data = "/home/madesai/hs-news/external-data/mit-election-lab/countypres_2000-2020.csv"
# I think I just want to be able to query by FIPS and year and get the party 


events_df = pd.read_csv(path_to_events)

events_df['CountyFIPS'] = events_df.apply(lambda row: get_county_fips(row['latitude'], row['longitude']), axis=1)

