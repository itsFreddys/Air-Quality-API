import json
from pathlib import Path
import functions_page as fp


class MissingFile(Exception):
    def __init__(self,file):
        print('FAILED')
        print(file)
        print('MISSING')
        quit()


class FormatError(Exception):
    def __init__(self, url):
        print('FAILED')
        print(url)
        print('FORMAT')
        quit()


class PurpleFile:
    def __init__(self, purple_path: str, center_path: str, range_miles: int, threshold: int, max_search: int, reverse_list: list):
        self.file_path = Path(purple_path)
        self._purple_file = purple_path
        self.centerObj = NomCenterFile(center_path)
        self.reverseObj = NomReverseFile(reverse_list)
        self._range = range_miles
        self._threshold = fp.c_to_aqi(threshold)
        self._max_res = max_search
        self.file_data = self.data_collection(self.file_path)
        self._filtered_list_dict = self.filter_data()
        self.printable_list = self.compare_update_dict()

    def compare_update_dict(self) -> list[dict]:
        """compares the filtered results with results from Reverse files
            returns a list dictionary of the results with keys: name,lat,lon"""
        reverse_list = self.reverseObj.get_list_of_dicts()
        temp_list = self._filtered_list_dict
        for i in range(len(temp_list)):
            for j in range(len(reverse_list)):
                r_lat = fp.round_float(reverse_list[j]['lat'])
                r_lon = fp.round_float(reverse_list[j]['lon'])
                t_lat = fp.round_float(temp_list[i]['lat'])
                t_lon = fp.round_float(temp_list[i]['lon'])
                if r_lat == t_lat and r_lon == t_lon:
                    temp_list[i]['name'] = reverse_list[j]['name']
                    temp_list[i]['url'] = reverse_list[j]['url']
                    break
                temp_list[i]['url'] = reverse_list[j]['url']
        if (self.validate_list(temp_list)):
            return temp_list


    def validate_list(self,list_dict: list[dict]) -> bool:
        """makes sure that there is not a formatting issue,
            return true if there is no issue, else raises exception and ends"""
        for i in range(len(list_dict)):
            url = list_dict[i].get('url')
            aqi = list_dict[i]['aqi']
            lon = list_dict[i]['lon']
            lat = list_dict[i]['lat']
            name = list_dict[i].get('name')
            if name == None:
                raise FormatError(url)
            else:
                return True


    def data_collection(self, path: Path) -> dict:
        """Collects data from file and returns the data as a dictionary"""
        # validate if path exists
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
                return data
        except FileNotFoundError:
            raise MissingFile(path)

    def filter_data(self) -> list[dict]:
        """filters data collected by the purple api
                returns a filtered sorted list of dictionaries of results"""
        temp_list = []
        for i in range(len(self.file_data['data'])):
            if str(self.file_data['data'][i][4]).isalpha():
                continue
            elif 0 <= fp.c_to_aqi(self.file_data['data'][i][4]) <= self._threshold:
                temp_lat = fp.degree_to_float(self.file_data['data'][i][2])
                temp_lon = fp.degree_to_float(self.file_data['data'][i][3])
                if 0 <= fp.degree_dist(temp_lat, temp_lon, self.centerObj) <= self._range:
                    temp_list.append(self.file_data['data'][i])
        filtered_list = fp.sort_data(temp_list, self._max_res)
        if len(filtered_list) == 0:
            raise FormatError(self._purple_file)
        list_dict = fp.list_to_dict(filtered_list)

        return list_dict

    def print_results(self) -> None:
        """prints results in the format for the project"""
        self.centerObj.print_center()
        fp.print_results(self.printable_list)

    def print_test(self):
        """for testing purplefile class"""
        self.print_results()


class NomCenterFile:
    def __init__(self, path):
        self._center_path = Path(path)
        self._center_file = path
        self._center_data = self.data_collection(self._center_path)

    def get_lon(self) -> float:
        """made to access lon outside of class"""
        return self._center_data['lon']

    def get_lat(self) -> float:
        """made to access lat outside of class"""
        return self._center_data['lat']

    def get_name(self) -> str:
        """made to access display_name outside of class"""
        return self._center_data['display_name']

    def data_collection(self, path: Path) -> dict:
        """Collects data from file
            returns a dictionary of data collected from file"""
        try:
            with open(path, 'r') as json_file:
                data = json.load(json_file)
                data_dict = data[0]
                return data_dict
        except FileNotFoundError:
            raise MissingFile(self._center_file)


    def print_center(self) -> None:
        """prints center, returns nothing"""
        print('CENTER ', end='')
        fp.print_coordinate(self._center_data)

    def test_center(self):
        """for testing center class"""
        pass


class NomReverseFile:
    def __init__(self, reverse_list: list):
        self._reverse_files = reverse_list
        self._list_dicts = self.data_collection()

    def get_list_of_dicts(self) -> list[dict]:
        """made to access list_dicts outside of class"""
        return self._list_dicts

    def data_collection(self) -> list[dict]:
        """Collects data from file and returns the data as
            a list of dictionaries"""
        newlist = []
        for i in range(len(self._reverse_files)):
            path = Path(self._reverse_files[i])
            try:
                with open(path,'r') as json_file:
                    data = json.load(json_file)
                    temp_dict = {
                        'url': self._reverse_files[i],
                        'name': data['display_name'],
                        'lat': data['lat'],
                        'lon': data['lon']
                    }
                    newlist.append(temp_dict)
            except FileNotFoundError:
                raise MissingFile(path)
        return newlist


def run():
    pass
    #purplefile = PurpleFile(file_address, file_center, range_mi, thres, max_result, reverse_files)
    #purplefile.print_test()


if __name__ == '__main__':
    run()
