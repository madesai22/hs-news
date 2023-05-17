import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
import csv
from datetime import datetime


def lat_long_to_fips(latitude, longitude):
    geolocator = Nominatim(user_agent="my-application")
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    address = location.raw['address']
    county_fips = address.get('county_fips')

    return county_fips

def fips_to_zip_dict(path_to_file):
    ftz_dict = {}
    with open(path_to_file) as f:
        for line in f[1:]: #skip heading
            items = line.split(",")
            zipcode = items[0] # zip is first column 
            fips = items[1] # county is the next one 
            if zipcode in ftz_dict:
                ftz_dict[zipcode].add(fips)
            else:
                ftz_dict[zipcode] = set(fips)
    return fips_to_zip_dict

def year_fips_to_party(csv_file):
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

def zip_to_lat_lon(zip_code):
    geolocator = Nominatim(user_agent="my_app")
    location = geolocator.geocode(zip_code)
    return (location.latitude, location.longitude)


def get_year(date_string):
    if len(date_string.split('/')[-1])==2:
        year = datetime.strptime(date_string, "%d/%m/%y").year
    else:
        year = datetime.strptime(date_string, "%d/%m/%Y").year
    return year

def get_matches(idx, row, boundary, dataframe):
    coords = (row['lat'],row['lon'])
    matches = {}

    for index_other, row_other in dataframe:
        if index_other != idx:
            coords_other = (row_other['lat'], row_other['lon'])
            distance = geopy.distance.geodesic(coords, coords_other)
            if distance >= boundary:
                matches[row['case']]= row_other['case']
    return matches


path_to_events = "/home/madesai/hs-news/external-data/Mother_jones_Mass_Shootings_Database_1982_2023.csv"
path_to_voting_data = "/home/madesai/hs-news/external-data/mit-election-lab/countypres_2000-2020.csv"
path_to_fips_file = "/home/madesai/hs-news/external-data/ZIP_COUNTY_122021.csv"
distance = 200 #km 

party_dictionary = year_fips_to_party(path_to_voting_data)
events_df = pd.read_csv(path_to_events)
ftz_dict = fips_to_zip_dict(path_to_fips_file)

# add fips, zip code, and party to events df 
events_df['countyFIPS'] = events_df.apply(lambda row: lat_long_to_fips(row['latitude'], row['longitude']), axis=1)
events_df['zip'] = events_df.apply(lambda row: ftz_dict(row['countyFIPS']), axis=1)
events_df['year'] = events_df.apply(lambda row: get_year(row['date']), axis=1)
events_df['party'] = events_df.apply(lambda row: party_dictionary[(row['year'],row['party'])], axis=1)

# see if any events are within some distance of one another
matches = []
for row, idx in events_df:
    row_match = get_matches(idx, row, distance, events_df)
    if row_match:
        matches.append(row_match)
if matches:
    print(matches)
else:
    print("no matches")


# collect articles that are within boundary of events? 
# loop through the event list
# find the zip code
# find the schools with that zip code in school_full_info later we can do distance
# from there find the domains?
# then find the articles with those zip codes
# calculate a percent change? in gv coverage over that time? 


    






