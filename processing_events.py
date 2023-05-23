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
            
                if key in max_votes_per_year:
                    if party_votes > max_votes_per_year[key][0]:
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


def lat_long_to_zip(latitude, longitude):
    geolocator = Nominatim(user_agent="madesasi@umich.edu")
    p = geopy.point.Point(latitude,longitude)
    location = geolocator.reverse(p, exactly_one=True)
    zip = location.raw['address']['postcode']
    return zip


def get_date(date_string):
    if len(date_string.split('/')[-1])==2:
        d = datetime.strptime(date_string, "%m/%d/%y").year
    else:
        d = datetime.strptime(date_string, "%m/%d/%Y").year
    return d


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

def find_clusters(lat_list, lon_list,distance): # takes in a set of tuples with idx, lat, lon
    points = zip(lat_list,lon_list)
    coords = set()
    for i, p in enumerate(points):
      coords.add((i, p[0],p[1]))
    C=[] #list of clusters
    while len(coords):
        l = coords.pop()
        print(l)
        locus_idx, locus_lat, locus_lon =l[0],l[1],l[2]
        locus = [locus_lat,locus_lon]
        cluster = [x for x in coords if geopy.distance.geodesic(locus,[x[1],x[2]]).km <= distance]
        
        C.append(cluster+[(locus_idx,locus_lat, locus_lon)])
        for x in cluster:
            coords.remove(x)
    return C


path_to_events = "/home/madesai/hs-news/external-data/Mother_jones_Mass_Shootings_Database_1982_2023.csv"
path_to_voting_data = "/home/madesai/hs-news/external-data/mit-election-lab/countypres_2000-2020.csv"
path_to_fips_file = "/home/madesai/hs-news/external-data/ZIP_COUNTY_122021.csv"
distance = 50 #km 

def make_edited_csv(path_to_events,path_to_voting_data, path_to_fips_file):

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

    countyFIPS = [lat_long_to_fips(lat, lon) for lat, lon in zip(latitude,longitude)]
    zip_code = [lat_long_to_zip(lat,lon) for lat, lon in zip(latitude,longitude)]
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


events_df = pd.read_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv")
events_df.drop(['zip'])
events_df = events_df.astype({'year': 'int'})
cases = events_df['case'].tolist()
latitude = events_df['latitude'].tolist()
longitude = events_df['longitude'].tolist()
zip_code = [lat_long_to_zip(lat,lon) for lat, lon in zip(latitude,longitude)]
events_df['zip'] = zip_code
events_df.to_csv("/home/madesai/hs-news/external-data/mother-jones-edited.csv")



years = events_df['year'].tolist()

clusters = find_clusters(latitude,longitude,distance)
all_cluster_data, longest_cluster, columns = [], 0, []
 
for c in clusters:
    if len(c) > longest_cluster:
        longest_cluster = len(c)
    single_cluster_data = []
    for event in c:
        idx, latlon = event[0], [event[1],event[2]]
        name = cases[idx]
        date = years[idx]
        single_cluster_data.extend([name, date, latlon])
    all_cluster_data.append(single_cluster_data)

for i in range(longest_cluster): columns.extend(["name_"+str(i),"date_"+str(i),"location_"+str(i)]) 
match_df = pd.DataFrame(columns=columns, data = all_cluster_data)
match_df.to_csv("/home/madesai/hs-news/external-data/"+str(distance)+"km_event_matches.csv")