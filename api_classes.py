import urllib.parse
import json
import time
import urllib.request
import functions_page as fp


class NetworkFailure(Exception):
    def __init__(self, status, url):
        print('FAILED')
        print(status, url)
        if status != 200:
            print('NOT 200')
        else:
            print('NETWORK')
        quit()


class FormatFailure(Exception):
    def __init__(self, status, url):
        print('FAILED')
        print(status, url)
        if status != 200:
            print('NOT 200')
        else:
            print('FORMAT')
        quit()


def collect_needed_data(full_dict: dict) -> dict:
    """creates a dictionary of keys that are important
        returns a dictionary with the keys: name, lat,lon"""
    new_dict = {
        'name': full_dict['display_name'],
        'lat': full_dict['lat'],
        'lon': full_dict['lon']
    }
    return new_dict


def filter_data(data: dict, threshold, user_range, max_res, center_obj) -> list[dict]:
    """filters data collected by the purple api
        returns a filtered sorted list of dictionaries of results"""
    temp_list = []
    for i in range(len(data['data'])):
        if str(data['data'][i][4]).isalpha():
            continue
        elif 0 <= fp.c_to_aqi(data['data'][i][4]) <= threshold:
            temp_lat = fp.degree_to_float(data['data'][i][2])
            temp_lon = fp.degree_to_float(data['data'][i][3])
            if 0 <= fp.degree_dist(temp_lat, temp_lon, center_obj) <= user_range:
                temp_list.append(data['data'][i])
    filtered_list = fp.sort_data(temp_list, max_res)

    return fp.list_to_dict(filtered_list)


class PurpleApi:
    def __init__(self, key: str, center_loc: str, range_miles: int, threshold: int, max_res: int):
        self.PURPLE_URL = 'https://api.purpleair.com/v1/sensors?'
        self._key = key
        self.forward_obj = ForwardNomin(center_loc)
        self._range_miles = range_miles
        self._threshold = fp.c_to_aqi(threshold)
        self._max_res = max_res
        self._built_url = self.build_url()
        self._data_dict = self.download_data()
        self.printable_list = self.compare_update_dict()

    def get_data_dict(self):
        """made to get the protected data_dict outside the class"""
        return self._data_dict

    def get_built_url(self) -> str:
        '''made to get the built url outside the class'''
        return self._built_url

    def build_url(self) -> str:
        """bulids the url with the parameters attached
            returns an encoded url"""
        parameters = {
            'fields': "name,latitude,longitude,pm2.5"
        }
        encoded = urllib.parse.urlencode(parameters)
        return f'{self.PURPLE_URL}{encoded}'

    def download_data(self) -> list[dict]:
        """downloading data from purple api
            return a list of dictionaries"""
        request = urllib.request.Request(
            self._built_url,
            headers={'X-API-KEY': self._key})
        response = urllib.request.urlopen(request)
        try:
            response_json = response.read().decode(encoding='utf-8')
            data = json.loads(response_json)
            data_filtered = filter_data(data, self._threshold, self._range_miles, self._max_res, self.forward_obj)
            return data_filtered
        finally:
            response.close()

    def compare_update_dict(self) -> list[dict]:
        """compares the filtered results with results from ReverseNominatim
            returns a list dictionary of the results with keys: name,lat,lon"""
        temp_list = self._data_dict
        for i in range(len(temp_list)):
            temp_reverse = ReverseNomin(temp_list[i]['lat'], temp_list[i]['lon'])
            temp_list[i]['name'] = temp_reverse.get_name()
        return temp_list

    def print_results(self) -> None:
        """prints the results in the format for project"""
        self.forward_obj.print_center()
        fp.print_results(self.printable_list)

    def purple_test(self) -> None:
        """for testing the class"""
        self.print_results()
        print()


class ForwardNomin:
    def __init__(self, location: str):
        self.FORWARD_URL = 'https://nominatim.openstreetmap.org/search'
        self._location = location
        self._built_url = self.build_url(location)
        self._data_dict = self.download_data()

    def get_data_dict(self) -> dict:
        """made to access data_dict outside of class"""
        return self._data_dict

    def get_lat(self) -> float:
        """made to access lat outside of class"""
        return self._data_dict['lat']

    def get_lon(self) -> float:
        """made to access lon outside of class"""
        return self._data_dict['lon']

    def get_name(self) -> str:
        """made to access name outside of class"""
        return self._data_dict['name']

    def get_status(self) -> int:
        """made to access status code outside of class"""
        return self._status_code

    def collect_status(self, status_code: int) -> None:
        """collects status code"""
        self._status_code = status_code

    def get_built_url(self) -> str:
        '''made to get the built url outside the class'''
        return self._built_url

    def build_url(self, location: str) -> str:
        """builds url with parameters
            returns encoded url"""
        parameters = {
            'q': location,
            'format': 'json'
        }
        encoded = urllib.parse.urlencode(parameters)
        return f'{self.FORWARD_URL}?{encoded}'

    def download_data(self) -> dict:
        """downloads content from ForwardNominatim site
            returns dictionary of data needed"""
        request = urllib.request.Request(
            self._built_url,
            headers={'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/japanto1'})
        response = urllib.request.urlopen(request)
        self.collect_status(response.status)
        try:
            response_json = response.read().decode(encoding='utf-8')
            data = json.loads(response_json)
            return collect_needed_data(data[0])
        finally:
            response.close()
            time.sleep(1)

    def print_center(self) -> None:
        """prints the center"""
        print('CENTER ', end='')
        fp.print_coordinate(self._data_dict)

    def _test_forward(self):
        """for testing ForwardNomin class"""
        print('testing in forward function:')
        print(self.get_name())
        print(self.get_lon())
        print(self.get_lat())
        print()
        fp.print_coordinate(self.get_data_dict())


class ReverseNomin:
    def __init__(self, lat: str, lon: str):
        self.REVERSE_URL = 'https://nominatim.openstreetmap.org/reverse'
        self._lon = lon
        self._lat = lat
        self._built_url = self.build_url(lat, lon)
        self._data_dict = self.download_data()

    def get_data_dict(self):
        """made to access the protected data_dict outside of class"""
        return self._data_dict

    def get_name(self):
        """made to access the protected name outside of class"""
        return self._data_dict['name']

    def get_lat(self):
        """made to access the protected lat outside of class"""
        return self._data_dict['lat']

    def get_lon(self):
        """made to access the protected lon outside of class"""
        return self._data_dict['lon']

    def get_built_url(self) -> str:
        '''made to get the built url outside the class'''
        return self._built_url

    def build_url(self, lat: str, lon: str) -> str:
        """builds url with following parameters
            returns an encoded url"""
        parameters = {
            'lat': lat,
            'lon': lon,
            'format': 'json'
        }

        encoded = urllib.parse.urlencode(parameters)
        return f'{self.REVERSE_URL}?{encoded}'

    def download_data(self) -> dict:
        """downloads content from the ReverseNominatim urll
            returns the data collected"""
        request = urllib.request.Request(
            self._built_url,
            headers={'Referer': 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/japanto1'})
        response = urllib.request.urlopen(request)

        try:
            response_json = response.read().decode(encoding='utf-8')
            data = json.loads(response_json)
            return collect_needed_data(data)
        finally:
            response.close()
            time.sleep(1)

    def test_reverse(self) -> None:
        """for testing reverseNominatim class"""
        print(self.get_data_dict())
        fp.print_coordinate(self.get_data_dict())


def run():
    Purple_url = 'https://api.purpleair.com/v1/sensors?'
    center_loc = 'Valley, CA '
    range_mi = 10
    thresh = 20
    max_res = 4

    # purpleObj = PurpleApi(Purple_url, center_loc, range_mi, thresh, max_res)
    # purpleObj.purple_test()
    forwardObj = ForwardNomin(center_loc)
    forwardObj.print_center()
    pass


if __name__ == '__main__':
    run()
