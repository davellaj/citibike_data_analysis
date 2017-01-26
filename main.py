# make sql calls to google big data api for citibikes
# get top 10 stations for subscribers
# get bottom 10 stations for subscribers
# gather latlong in a dictionary
# find distance to nearest metro stop
# return the distance to metro station for the top 10 stations
# return the distance to metro station for the bottom 10 stations
# print results on scatterplot with circles to reflect distance or a bar chart one mar is metro stop one bar is distance
# make interface where my friends who aren't tech savy can draw information for the queries
# site where you can view the queries I made, or maybe a blog post that allows users to post suggestions for queries.

from math import radians, cos, sin, asin, sqrt
import csv
# import requests

# request object gives us access to json method
# r = requests.get("URL")
# data = r.json()

# import urllib2
# import json

# citibikesAPI = 'AIzaSyAVSDb3H4ZXQ7i8fWhDO9AOPBNmNLhL6x4'
#
# def locu_search(query):
#     api_key = citibikesAPI
#     url = 'https://api.locu.com/v1_0/venue/search/?api_key' + api_key
#     locality = query.replace(' ', '%20')
#     final_url = url + '&locality=' + locality + '&category=restaurant'
#     json_obj = urllib2.urlopen(final_url)
#     data = json.load(json_obj)
#
#     for item in data['objects']:
#         print item['name']
#         print item['phone']
#
# locu_search('new york')


# haversine is spherical string pull tight from one point to another. appropriate for drone delivery :)
# triangular equation - pythagoros point to point on 2D field
#  Manhattan Distance -- diff in one coordinate and diff in another coordinate and adding them
#  you only walk along the grid == assumes you was walking across the grid

# links from chris
# r = requests.get(".........")
# data = r.json()
# pip install requests
# import requests
# import psycopg2
# http://www.citibikenyc.com/stations/json
# https://www.citibikenyc.com/system-data
# Manhattan Distance
# import csv
# https://docs.python.org/3/library/csv.html


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    km = 6367 * c
    return km

def manhattan_distance(start, end):
    s_lat, s_lon = start
    e_lat, e_lon = end
    # print(start, end)
    return abs(e_lat - s_lat) + abs(e_lon - s_lon)

# search through data set and look for closest latlong
# calculate latlong distance:

# example input
# metro_stations = [
#                     {'lat': 40.730328, 'lon': -73.992629, 'name': '8th St'},
#                     {'lat': 40.741303, 'lon': -73.989344, 'name': '23rd St'},
#                     {'lat': 40.735736, 'lon': -73.990568, 'name': 'Union Square'},
#                 ]
citibike_stations = [
                        {'lat': 40.7423543, 'lon': -73.98915076, 'name': 'Broadway & W 24 St' },
                        {'lat': 40.751551, 'lon': -73.993934, 'name': '8 Ave & W 33 St' },
                        {'lat': 40.746745, 'lon': -74.007756, 'name': 'W 20 St & 11 Ave' },
                    ]

# example output
# observation - top citibike station all next to the same metro stop
# [
#     {
#         citibike station:  {'lat': 40.7423543, 'lon': -73.98915076, 'name': 'Broadway & W 24 St'},
#         metro station:  {'lat': 40.741303, 'lon': -73.989344, 'name': 'Broadway,23rd St'},
#         temp_distance 0.11795330311417092,
#     }
#
#     {
#         citibike station:  {'lat': 40.751551, 'lon': -73.993934, 'name': '8 Ave & W 33 St'},
#         metro station:  {'lat': 40.741303, 'lon': -73.989344, 'name': 'Broadway,23rd St'},
#         temp_distance 1.2025867415022102,
#     }
#
#     {
#         citibike station:  {'lat': 40.746745, 'lon': -74.007756, 'name': 'W 20 St & 11 Ave'},
#         metro station:  {'lat': 40.741303, 'lon': -73.989344, 'name': 'Broadway,23rd St'},
#         temp_distance 1.6639293851898207,
#     }
# ]

# getting data from metro station csv file
# Division,Line,Station_Name,Station_Latitude,Station_Longitude,Route_1,Route_2,Route_3,Route_4,Route_5,Route_6,Route_7,Route_8,Route_9,Route_10,Route_11,Entrance_Type,Entry,Exit_Only,Vending,Staffing,Staff_Hours,ADA,ADA_Notes,Free_Crossover,North_South_Street,East_West_Street,Corner,Latitude,Longitude
metro_stations_csv = []
with open('metro_station_entrances_nyc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row['Station_Name'], row['Station_Latitude'], row['Station_Longitude'],)
        metro_stations_csv.append({
                                    'metro_station_name' : row['Station_Name'],
                                    'lat' : float(row['Station_Latitude']),
                                    'lon' : float(row['Station_Longitude']),
                                })

mode_distance = []
def get_distance():
    for citibike in citibike_stations:
        distance_to_metro = 1000
        shortest_metro = {}
        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['lat'], citibike['lon']))
            # temp_distance = haversine(metro['lon'], metro['lat'], citibike['lon'], citibike['lat'])

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        mode_distance.append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
    return mode_distance

get_distance()
# print(get_distance())
