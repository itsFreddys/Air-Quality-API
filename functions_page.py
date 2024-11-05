import math


def c_to_aqi(pm_concent) -> int:
    """collects a concentrated pm2.5 value and converts to aqi
        return aqi"""
    aqi_value = 0
    if 0 <= pm_concent < 12.1:
        aqi_value = (50 / 12) * pm_concent
    elif 12.1 <= pm_concent < 35.5:
        aqi_value = (49 / 23.3) * (pm_concent - 12.1) + 51
    elif 35.5 <= pm_concent < 55.5:
        aqi_value = (49 / 19.9) * (pm_concent - 35.5) + 101
    elif 55.5 <= pm_concent < 150.5:
        aqi_value = (49 / 94.9) * (pm_concent - 55.5) + 151
    elif 150.5 <= pm_concent < 250.5:
        aqi_value = (99 / 99.9) * (pm_concent - 150.5) + 201
    elif 250.5 <= pm_concent < 350.5:
        aqi_value = (99 / 99.9) * (pm_concent - 250.5) + 301
    elif 350.5 <= pm_concent < 500.5:
        aqi_value = (99 / 149.9) * (pm_concent - 350.5) + 401
    elif 500.5 <= pm_concent:
        aqi_value = 500
    return round(aqi_value)


def degree_to_float(num: float or str) -> float:
    """turns coordinate into a float
        returns float"""
    if num == None:
        return 1111.0
    if type(num) == str:
        if num.startswith('-'):
            temp_num = num[1:]
            return float(temp_num)
    elif num < 0:
        num = num * -1
    return float(num)

def round_float(num: 'float or str') -> float:
    """turns string into float and rounds
        returns rounded float"""
    if type(num) == str:
        if num.startswith('-'):
            temp_num = num[1:]
            return round(float(temp_num) * -1, 2)
        else:
            return round(float(num),2)
    elif num > 0 or num < 0:
        return round(num,2)


def degree_dist(lat_point, lon_point, center_obj: 'NomCenter') -> float:
    """finds the distance of two coordinates, returns distance as float"""
    center_lat = degree_to_float(center_obj.get_lat())
    center_lon = degree_to_float(center_obj.get_lon())
    R = 3958.8
    dlat = abs(math.radians(lat_point - center_lat))
    dlon = abs(math.radians(lon_point - center_lon))
    alat = abs(math.radians((lat_point + center_lat) / 2))
    x = dlon * math.cos(alat)
    distance = math.sqrt(x ** 2 + dlat ** 2) * R
    return round(distance, 2)


def sort_data(filtered_list: list, max_res: int) -> list:
    """sorts a list according to aqi value,
        returns a sorted list of max size of requested search size"""
    def sort_key(aqi):
        return aqi[4]

    filtered_list.sort(key=sort_key, reverse=True)
    temp_list = filtered_list[0: max_res]

    return temp_list


def list_to_dict(f_list: list) -> list[dict]:
    """Creates a list of dictionaries
        returns a list of dictionaries"""
    newlist = []
    for i in range(len(f_list)):
        count = 0
        for j in range(len(f_list[i])):
            count = count+1
            if count == 2:
                temp_dict = {
                    'lat': f_list[i][2],
                    'lon': f_list[i][3],
                    'aqi': c_to_aqi(f_list[i][4])
                }
                newlist.append(temp_dict)
    return newlist


def print_coordinate(data_dict) -> None:
    """prints coordinates in the format being asked for the project"""
    lon = str(data_dict['lon'])
    lat = str(data_dict['lat'])
    if lon.startswith('-'):
        lon = lon[1:] + '/W'
    else: lon = lon + '/E'

    if lat.startswith('-'):
        lat = lat[1:] + '/S'
    else: lat = lat + '/N'

    print(lat, lon)


def print_results(list_dict: list[dict]) -> None:
    """prints all results of a list of dictionaries,
        prints in the format of the project"""
    for i in range(len(list_dict)):
        print('AQI',list_dict[i]['aqi'])
        print_coordinate(list_dict[i])
        print(list_dict[i]['name'])


def print_dict(my_dict: dict) -> None:
    """prints the contents of a dictionary
        prints in the format of the project"""
    print('AQI',my_dict['aqi'])
    print_coordinate(my_dict)
    print(my_dict['name'])