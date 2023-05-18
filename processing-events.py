import pandas as pd
from geopy.geocoders import Nominatim
import geopy.distance
import csv
from datetime import datetime
import requests
import json
import preprocess as pp


def lat_long_to_fips(latitude, longitude):
    request_str = "https://geo.fcc.gov/api/census/block/find?lat={}&lon={}&format=json".format(latitude,longitude)
    response = requests.get(request_str)
    try: 
        fips = response.json()['results'][0]['county_fips']
        return int(fips)
    except:
        return -1

def fips_to_zip_dict(path_to_file):
    ftz_dict = {}
    with open(path_to_file) as f:
        lines = f.readlines()
        for line in lines[1:]: #skip heading
            items = line.split(",")
            zipcode = items[0] # zip is first column 
            fips = int(items[1]) # county is the next one 
            ftz_dict[fips] = int(zipcode)
    return ftz_dict

def year_fips_to_party(csv_file):
    max_votes_per_year = {} # (year, fips) --> [nvotes, party]
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try: 
                county_fips = int(row['county_fips'])
                party = row['party']
                party_votes = float(row['candidatevotes'])
                year = int(row['year'])
                key = (year, county_fips)
                if county_fips == 21101:
                    print(key, party, party_votes)
                if key in max_votes_per_year:
                    if party_votes > max_votes_per_year[year][0]:
                        if county_fips == 21101:
                            print("update! {} {} {}".format(year, party, party_votes))
                        max_votes_per_year[key] = [party_votes,party]
                else:
                    max_votes_per_year[key] = [party_votes,party]    
            except:
                pass

    return max_votes_per_year

def zip_to_lat_lon(zip_code):
    geolocator = Nominatim(user_agent="madesasi@umich.edu")
    location = geolocator.geocode(zip_code)
    return (location.latitude, location.longitude)


def get_year(date_string):
    if len(date_string.split('/')[-1])==2:
        year = datetime.strptime(date_string, "%m/%d/%y").year
    else:
        year = datetime.strptime(date_string, "%m/%d/%Y").year
    return year

def get_matches(idx, row, boundary, dataframe):
    coords = (row['lat'],row['lon'])
    matches = {}

    for index_other, row_other in dataframe:
        if index_other != idx:
            coords_other = (row_other['lat'], row_other['lon'])
            distance = geopy.distance.geodesic(coords, coords_other).km
            if distance >= boundary:
                matches[row['case']]= row_other['case']
    return matches


path_to_events = "/home/madesai/hs-news/external-data/Mother_jones_Mass_Shootings_Database_1982_2023.csv"
path_to_voting_data = "/home/madesai/hs-news/external-data/mit-election-lab/countypres_2000-2020.csv"
path_to_fips_file = "/home/madesai/hs-news/external-data/ZIP_COUNTY_122021.csv"
distance = 200 #km 

party_dictionary = year_fips_to_party(path_to_voting_data)
events_df = pd.read_csv(path_to_events)
events_df = events_df.astype({'year': 'int'})
events_df = pp.df_slice(events_df,2000,2019,'year')

ftz_dict = fips_to_zip_dict(path_to_fips_file)
years = events_df['year'].tolist()
election_years = [pp.year_to_election_year(y) for y in years]

# add fips, zip code, and party to events df 
latitude = events_df['latitude'].tolist()
longitude = events_df['longitude'].tolist()
cases = events_df['case'].tolist()

countyFIPS = [lat_long_to_fips(lat, lon) for lat, lon in zip(latitude,longitude)]
zip_code = [ftz_dict[fips] for fips in countyFIPS]
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
# see if any events are within some distance of one another
matches = set()
for i, latlon in enumerate(zip(latitude,longitude)):
    for j, latlon_other in enumerate(zip(latitude,longitude)):
        if i != j:
            d = geopy.distance.geodesic(latlon, latlon_other).km
            if d < distance and d > 0:
                matches.add(frozenset((cases[i], cases[j])))
print(matches)
print("**")

if matches:
    for m in matches:
        m = list(m)
        print("{} within 200km of  {}".format(m[0],m[1]))
else:
    print("no matches")






# collect articles that are within boundary of events? 
# loop through the event list
# find the zip code
# find the schools with that zip code in school_full_info later we can do distance
# from there find the domains?
# then find the articles with those zip codes
# calculate a percent change? in gv coverage over that time? 
# probably good to make a json file, or add to it? maybe do with a random sample 


    






