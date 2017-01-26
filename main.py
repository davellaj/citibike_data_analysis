# make sql calls to google big data api for citibikes
# get top 10 stations for subscribers
# get bottom 10 stations for subscribers
# gather latlong in a dictionary
# find distance to nearest metro stop
# return the distance to metro station for the top 10 stations
# return the distance to metro station for the bottom 10 stations
# print results on scatterplot with circles to reflect distance or a bar chart one mar is metro stop one bar is distance
# print map with worst citibike stations / best citibike locations
# make interface where my friends who aren't tech savy can draw information for the queries
# site where you can view the queries I made, or maybe a blog post that allows users to post suggestions for queries.
# place where people can post their work/queries/projects/ideas about public transportation

# example input
# metro_stations = [
#                     {'lat': 40.730328, 'lon': -73.992629, 'name': '8th St'},
#                     {'lat': 40.741303, 'lon': -73.989344, 'name': '23rd St'},
#                     {'lat': 40.735736, 'lon': -73.990568, 'name': 'Union Square'},
#                 ]
# citibike_stations = [
#                         {'lat': 40.7423543, 'lon': -73.98915076, 'name': 'Broadway & W 24 St' },
#                         {'lat': 40.751551, 'lon': -73.993934, 'name': '8 Ave & W 33 St' },
#                         {'lat': 40.746745, 'lon': -74.007756, 'name': 'W 20 St & 11 Ave' },
#                     ]

# example output
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
# observation - top citibike station all next to the same metro stop


import csv
import requests
# import psycopg2

# manhattan distance is a formula for computing distance in right angles,
# assuming you can only walk north south east west on a street grid like manhattan
def manhattan_distance(start, end):
    s_lat, s_lon = start
    e_lat, e_lon = end
    # print(start, end)
    return abs(e_lat - s_lat) + abs(e_lon - s_lon)


# getting data from metro station csv file: https://docs.python.org/3/library/csv.html
# would like to clean up and remove duplicate station locations to reduce loop runtime
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
#  citibike best station dataset
# only selected usertype to be subscribers as opposed to customers
# would like to clean up and remove the bottom 5
citibike_best_stations_csv = []
with open('citibike_best_desc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row['Station_Name'], row['Station_Latitude'], row['Station_Longitude'],)
        citibike_best_stations_csv.append({
                                            'citibike_station_name' : row['start_station_name'],
                                            'lat' : float(row['start_station_latitude']),
                                            'lon' : float(row['start_station_longitude']),
                                            'num_trips' : int(row['num_trips']),
                                        })
# citibike worst stations data set
# only selected usertype to be subscribers as opposed to customers
# would like to clean up and remove bottom 5
citibike_worst_stations_csv = []
with open('citibike_worst_asc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # print(row['Station_Name'], row['Station_Latitude'], row['Station_Longitude'],)
        citibike_worst_stations_csv.append({
                                            'citibike_station_name' : row['start_station_name'],
                                            'lat' : float(row['start_station_latitude']),
                                            'lon' : float(row['start_station_longitude']),
                                            'num_trips' : int(row['num_trips']),
                                        })
# print(citibike_worst_stations_csv)
# print(citibike_best_stations_csv)

#  computation of distance to metro station using data from csv files
def get_distance_citibike_best():
    citibike_best_distance = []

    for citibike in citibike_best_stations_csv:
        distance_to_metro = 10000
        shortest_metro = {}
        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['lat'], citibike['lon']))
            # temp_distance = haversine(metro['lon'], metro['lat'], citibike['lon'], citibike['lat'])

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        citibike_best_distance.append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
    return citibike_best_distance

def get_distance_citibike_worst():
    citibike_worst_distance = []

    for citibike in citibike_worst_stations_csv:
        distance_to_metro = 10000
        shortest_metro = {}
        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['lat'], citibike['lon']))
            # temp_distance = haversine(metro['lon'], metro['lat'], citibike['lon'], citibike['lat'])

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        citibike_worst_distance.append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
    return citibike_worst_distance

# print(get_distance_citibike_best())
# print(get_distance_citibike_worst())

# look at distance from best stations and look with distance from worst stations
# loop over these objects to print out distance.
# do the distances have a trend, avg distance?
def print_popular_distances():
    best_distances = get_distance_citibike_best()
    worst_distances = get_distance_citibike_worst()
    best_avg = 0
    best_count = 0
    worst_avg = 0
    worst_count = 0

    print("Best station distances")
    for station in best_distances:
        best_avg += station['distance_to_metro']
        best_count += 1
        print("Distance to metro: ", station['distance_to_metro'], "Citibike Station: ", station['citibike_station']['citibike_station_name'] )

    print("Worst station distances")
    for station in worst_distances:
        worst_avg += station['distance_to_metro']
        worst_count += 1
        print("Distance to metro: ", station['distance_to_metro'], "Citibike Station: ", station['citibike_station']['citibike_station_name'] )
    print("Best Citibike station AVG distance to Metro: ", best_avg/best_count)
    print("Worst Citibike station AVG distance to Metro: ", worst_avg/worst_count)

# print_popular_distances()


# compute distance to metro based on data from api of totalDocs at a citibike station
# request object gives us access to json method
# http://www.citibikenyc.com/stations/json
# https://feeds.citibikenyc.com/stations/stations.json
# https://www.citibikenyc.com/system-data

# sort out top 10 highest number of totalDocs
# sort out bottom 10 lowest number of totalDocs
# put into dictionary
# call distance function
# print avg

r = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
data = r.json()

citibike_stations_list = data['stationBeanList']
# print(citibike_stations_list[0]['totalDocks']

# example output:
most_totalDocks_stations = [
                {
                    'id': 3438, 'stationName': 'E 76 St & 3 Ave', 'availableDocks': 23, 'totalDocks': 31, 'latitude': 40.772248537721744, 'longitude': -73.95842134952545,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 7, 'stAddress1': 'E 76 St & 3 Ave', 'stAddress2': '', 'city': '', 'postalCode': '',
                      'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 01:29:34 AM', 'landMark': ''
                },
                {
                    'id': 79, 'stationName': 'Franklin St & W Broadway', 'availableDocks': 6, 'totalDocks': 33, 'latitude': 40.71911552, 'longitude': -74.00666661,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 27, 'stAddress1': 'Franklin St & W Broadway', 'stAddress2': '', 'city': '', 'postalCode': '',
                      'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 12:55:07 AM', 'landMark': ''
                },
                {
                    'id': 82, 'stationName': 'St James Pl & Pearl St', 'availableDocks': 16, 'totalDocks': 27, 'latitude': 40.71117416, 'longitude': -74.00016545,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 11, 'stAddress1': 'St James Pl & Pearl St', 'stAddress2': '', 'city': '', 'postalCode': '',
                     'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 12:54:58 AM', 'landMark': ''
                }
            ]
least_totalDocks_stations = [
                {
                    'id': 3443, 'stationName': 'W 52 St & 6 Ave', 'availableDocks': 39, 'totalDocks': 41, 'latitude': 40.76132983124814, 'longitude': -73.97982001304626,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 1, 'stAddress1': 'W 52 St & 6 Ave', 'stAddress2': '', 'city': '', 'postalCode': '',
                      'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 01:31:19 AM', 'landMark': ''
                },
                {
                    'id': 3440, 'stationName': 'Fulton St & Adams St', 'availableDocks': 39, 'totalDocks': 43, 'latitude': 40.692418292578466, 'longitude': -73.98949474096298,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 4, 'stAddress1': 'Fulton St & Adams St', 'stAddress2': '', 'city': '', 'postalCode': '',
                      'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 01:30:54 AM', 'landMark': ''
                },
                {
                    'id': 72, 'stationName': 'W 52 St & 11 Ave', 'availableDocks': 36, 'totalDocks': 39, 'latitude': 40.76727216, 'longitude': -73.99392888,
                     'statusValue': 'In Service', 'statusKey': 1, 'availableBikes': 2, 'stAddress1': 'W 52 St & 11 Ave', 'stAddress2': '', 'city': '', 'postalCode': '',
                      'location': '', 'altitude': '', 'testStation': False, 'lastCommunicationTime': '2017-01-26 12:22:17 AM', 'landMark': ''
                }
            ]

def get_distance_most_totalDocks():
    most_totalDocks_distance = []

    for citibike in most_totalDocks_stations:
        distance_to_metro = 10000
        shortest_metro = {}
        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['latitude'], citibike['longitude']))
            # temp_distance = haversine(metro['lon'], metro['lat'], citibike['lon'], citibike['lat'])

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        most_totalDocks_distance.append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
    return most_totalDocks_distance

def get_distance_least_totalDocks():
    least_totalDocks_distance = []

    for citibike in least_totalDocks_stations:
        distance_to_metro = 10000
        shortest_metro = {}
        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['latitude'], citibike['longitude']))
            # temp_distance = haversine(metro['lon'], metro['lat'], citibike['lon'], citibike['lat'])

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        least_totalDocks_distance.append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
    return least_totalDocks_distance

# print(get_distance_most_totalDocks())
# print(get_distance_least_totalDocks())

def print_docks_distances():
    most_docks_distances = get_distance_most_totalDocks()
    least_docks_distances = get_distance_least_totalDocks()
    most_avg = 0
    most_count = 0
    least_avg = 0
    least_count = 0

    print("Most total docks citibike station distances")
    for station in most_docks_distances:
        most_avg += station['distance_to_metro']
        most_count += 1
        print("Distance to metro: ", station['distance_to_metro'], "Citibike Station: ", station['citibike_station']['stationName'] )

    print("Least total docks citibike station distances")
    for station in least_docks_distances:
        least_avg += station['distance_to_metro']
        least_count += 1
        print("Distance to metro: ", station['distance_to_metro'], "Citibike Station: ", station['citibike_station']['stationName'] )
    print("Most total docks Citibike station AVG distance to Metro: ", most_avg/most_count)
    print("Least total docks Citibike station AVG distance to Metro: ", least_avg/least_count)


print_docks_distances()
print_popular_distances()





# Notes----------------------------------------------------------------------------------------
# from math import radians, cos, sin, asin, sqrt
# haversine is spherical string pull tight from one point to another. appropriate for drone delivery :)
# triangular equation - pythagoros point to point on 2D field
#  Manhattan Distance -- diff in one coordinate and diff in another coordinate and adding them
#  you only walk along the grid == assumes you was walking across the grid

# def haversine(lon1, lat1, lon2, lat2):
#     """
#     Calculate the great circle distance between two points
#     on the earth (specified in decimal degrees)
#     """
#     # convert decimal degrees to radians
#     lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
#     # haversine formula
#     dlon = lon2 - lon1
#     dlat = lat2 - lat1
#     a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
#     c = 2 * asin(sqrt(a))
#     km = 6367 * c
#     return km
#  ------------------------
# youtube tutorial on using an api with python - in python2
# import urllib2
# import json
#
# def locu_search(query):
#     api_key = ''
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
