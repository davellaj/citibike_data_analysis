# make sql calls to google big data api for citibikes
# get top 10 stations for subscribers
# get bottom 10 stations for subscribers
# gather latlong in a dictionary
# find distance to nearest metro stop
# return the distance to metro station for the top 10 stations
# return the distance to metro station for the bottom 10 stations
# print results on scatterplot with circles to reflect distance or a bar chart one mar is metro stop one bar is distance
from math import radians, cos, sin, asin, sqrt
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

# calculate latlong distance:
citibike_station = {'lat': 40.7423543, 'lon': -73.98915076, 'name': 'Broadway & W 24 St' }
metro_station = {'lat': 40.730328, 'lon': -73.992629, 'name': 'Broadway, 8th St'}
metro_stations = [
                    {'lat': 40.730328, 'lon': -73.992629, 'name': 'Broadway, 8th St'},
                    {'lat': 40.741303, 'lon': -73.989344, 'name': 'Broadway,23rd St'},
                    {'lat': 40.735736, 'lon': -73.990568, 'name': 'Broadway,Union Square'},
                ]
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

# search through data set and look for closest latlong
distance = 1000
for item in metro_stations:
    # print(item['lat'])
    temp_distance = haversine(item['lon'], item['lat'], citibike_station['lon'], citibike_station['lat'])
    if temp_distance < distance:
        distance = temp_distance
print(distance)

# print("the answer in km should be 1.369: ", haversine(citibike_station['lon'], citibike_station['lat'], metro_station['lon'], metro_station['lat']))
