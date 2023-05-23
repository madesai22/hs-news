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

def km_between_zip(zip1,zip2):
    z1, z2 = zip_to_lat_lon(zip1), zip_to_lat_lon(zip2)
    return geopy.distance.geodesic(z1, z2).km
    


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
        locus_idx, locus_lat, locus_lon =l[0],l[1],l[2]
        locus = [locus_lat,locus_lon]
        cluster = [x for x in coords if geopy.distance.geodesic(locus,[x[1],x[2]]).km <= distance]
        
        C.append(cluster+[(locus_idx,locus_lat, locus_lon)])
        for x in cluster:
            coords.remove(x)
    return C

def make_cluster_csv(clusters, cases, years):
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
    return match_df