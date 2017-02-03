import csv
import requests

# manhattan distance is a formula for computing distance in right angles,
# assuming you can only walk north south east west on a street grid like manhattan
def manhattan_distance(start, end):
    s_lat, s_lon = start
    e_lat, e_lon = end
    # print(start, end)
    return abs(e_lat - s_lat) + abs(e_lon - s_lon)

# getting data from metro station csv file: https://docs.python.org/3/library/csv.html
metro_stations_csv = []
with open('metro_station_entrances_nyc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        metro_stations_csv.append({
                                    'metro_station_name' : row['Station_Name'],
                                    'lat' : float(row['Station_Latitude']),
                                    'lon' : float(row['Station_Longitude']),
                                })
#  citibike best station dataset
# only selected usertype to be subscribers as opposed to customers
citibike_best_stations_csv = []
with open('citibike_best_desc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        citibike_best_stations_csv.append({
                                            'citibike_station_name' : row['start_station_name'],
                                            'lat' : float(row['start_station_latitude']),
                                            'lon' : float(row['start_station_longitude']),
                                            'num_trips' : int(row['num_trips']),
                                        })
# citibike worst stations data set
# only selected usertype to be subscribers as opposed to customers
citibike_worst_stations_csv = []
with open('citibike_worst_asc.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
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
    citibike_best_distance = {'stations' : [], 'distance_list': []}

    for citibike in citibike_best_stations_csv:
        distance_to_metro = 10000
        shortest_metro = {}

        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['lat'], citibike['lon']))

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        citibike_best_distance['stations'].append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
        citibike_best_distance['distance_list'].append(distance_to_metro)
    return citibike_best_distance

def get_distance_citibike_worst():
    citibike_worst_distance = {'stations' : [], 'distance_list': []}

    for citibike in citibike_worst_stations_csv:
        distance_to_metro = 10000
        shortest_metro = {}

        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['lat'], citibike['lon']))

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        citibike_worst_distance['stations'].append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
        citibike_worst_distance['distance_list'].append(distance_to_metro)
    return citibike_worst_distance

# print(get_distance_citibike_best())
# print(get_distance_citibike_worst())

def print_popular_distances():
    best_distances = get_distance_citibike_best()
    worst_distances = get_distance_citibike_worst()
    best_avg = 0
    best_count = 0
    worst_avg = 0
    worst_count = 0
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Best station distances")
    for station in best_distances['stations']:
        best_avg += station['distance_to_metro']
        best_count += 1
        print("Distance to metro: ", station['distance_to_metro'] * 1000, "Citibike Station: ", station['citibike_station']['citibike_station_name'] )
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Worst station distances")
    for station in worst_distances['stations']:
        worst_avg += station['distance_to_metro']
        worst_count += 1
        print("Distance to metro: ", station['distance_to_metro'] * 1000, "Citibike Station: ", station['citibike_station']['citibike_station_name'] )
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Best Citibike station-Metro AVG Distance: %6.2f" % (best_avg/best_count * 1000))
    print("Best Citibike station-Metro, MAX/MIN Distance: Max distance: %6.2f, Min distance: %6.2f" % (max(best_distances['distance_list']) * 1000, min(best_distances['distance_list']) * 1000))
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Worst Citibike station-Metro, AVG Distance: %6.2f" % (worst_avg/worst_count * 1000))
    print("Worst Citibike station-Metro, MAX/MIN Distance: Max distance: %6.2f, Min distance: %6.2f" % (max(worst_distances['distance_list']) * 1000, min(worst_distances['distance_list']) * 1000))
    print("-------------------------------------------------------------------------------------------------------------------------------")

# compute distance to metro based on data from api of totalDocs at a citibike station
# http://www.citibikenyc.com/stations/json
# https://feeds.citibikenyc.com/stations/stations.json
# https://www.citibikenyc.com/system-data

r = requests.get("https://feeds.citibikenyc.com/stations/stations.json")
data = r.json()

citibike_stations_list = data['stationBeanList']
# sort citibike_stations_list by total docks in ascending order.
citibike_stations_list.sort(key=lambda sta: sta['totalDocks'])
# start the least totalDocks station at 13 because the bottom 13 had 0 docks.
least_totalDocks_stations = citibike_stations_list[13:33]
most_totalDocks_stations = citibike_stations_list[-20:]

# Repeat similar analysis as above but this time with totalDocks data.
def get_distance_most_totalDocks():
    most_totalDocks_distance = {'stations' : [], 'distance_list': []}

    for citibike in most_totalDocks_stations:
        distance_to_metro = 10000
        shortest_metro = {}

        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['latitude'], citibike['longitude']))

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        most_totalDocks_distance['stations'].append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
        most_totalDocks_distance['distance_list'].append(distance_to_metro)
    return most_totalDocks_distance

def get_distance_least_totalDocks():
    least_totalDocks_distance = {'stations' : [], 'distance_list': []}

    for citibike in least_totalDocks_stations:
        distance_to_metro = 10000
        shortest_metro = {}

        for metro in metro_stations_csv:
            temp_distance = manhattan_distance((metro['lat'], metro['lon']), (citibike['latitude'], citibike['longitude']))

            if temp_distance < distance_to_metro:
                distance_to_metro = temp_distance
                shortest_metro = metro
        least_totalDocks_distance['stations'].append({'citibike_station': citibike, 'metro_station': shortest_metro, 'distance_to_metro': distance_to_metro})
        least_totalDocks_distance['distance_list'].append(distance_to_metro)
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
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Most total docks citibike station distances")
    for station in most_docks_distances['stations']:
        most_avg += station['distance_to_metro']
        most_count += 1
        print("Distance to metro: ", station['distance_to_metro'] * 1000, "Citibike Station: ", station['citibike_station']['stationName'] )
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Least total docks citibike station distances")
    for station in least_docks_distances['stations']:
        least_avg += station['distance_to_metro']
        least_count += 1
        print("Distance to metro: ", station['distance_to_metro'] * 1000, "Citibike Station: ", station['citibike_station']['stationName'] )
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Most total docks Citibike station-Metro, AVG Distance: %6.2f" % (most_avg/most_count * 1000))
    print("Most total docks Citibike station-Metro, MAX/MIN Distance: Max distance: %6.2f, Min distance: %6.2f" % (max(most_docks_distances['distance_list']) * 1000, min(most_docks_distances['distance_list']) * 1000))
    print("-------------------------------------------------------------------------------------------------------------------------------")
    print("Least total docks Citibike station-Metro, AVG Distance: %6.2f" % (least_avg/least_count * 1000))
    print("Least total docks Citibike station-Metro, MAX/MIN Distance: Max distance: %6.2f, Min distance: %6.2f" % (max(least_docks_distances['distance_list']) * 1000, min(least_docks_distances['distance_list']) * 1000))
    print("-------------------------------------------------------------------------------------------------------------------------------")

# Get results for the analysis
print_docks_distances()
print_popular_distances()
