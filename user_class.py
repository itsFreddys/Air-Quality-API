import api_classes as ac
import file_classes as fc


class UserInput:
    def __init__(self, center: str, user_range: int, threshold: int, user_max: int, aqi_source: str,reverse: str):
        self._center = self.check_center(center)
        self._range = user_range
        self._threshold = threshold
        self._max = user_max
        self._reverse = self.check_reverse(reverse)
        self._purple_source = self.check_purple(aqi_source)

    def check_center(self,center: str) -> 'NomCenterFile or ForwardNomin':
        """checks center if it begins with NOMINATIM OR FILE,
            returns center without NOMINATIM OR FILE"""
        if center.startswith('NOMINATIM '):
            temp_cent = center.replace('NOMINATIM ', '')
            return temp_cent
        elif center.startswith('FILE '):
            temp_cent = center.replace('FILE ','')
            return temp_cent

    def check_reverse(self,reverse: str) -> 'str or list':
        """checks reverse if it begins with NOMINATIM OR FILES,
                    returns reverse without NOMINATIM [str] OR FILES [list]"""
        if reverse.startswith('NOMINATIM '):
            temp_cent = reverse.replace('NOMINATIM ', '')
            return temp_cent
        elif reverse.startswith('FILES '):
            temp_cent = reverse.replace('FILES ','')
            temp_list = temp_cent.split(' ')
            return temp_list

    def check_purple(self,purple: str) -> 'NomCenterFile or ForwardNomin':
        """checks purple entry if it begins with PURPLEAIR OR FILE,
                    returns purple object for api or file"""
        if purple.startswith('PURPLEAIR '):
            temp_key = purple.replace('PURPLEAIR ', '')
            purpleObj = ac.PurpleApi(temp_key,self._center,self._range,self._threshold,self._max)
            return purpleObj
        elif purple.startswith('FILE '):
            temp_cent = purple.replace('FILE ','')
            purpleObj = fc.PurpleFile(temp_cent,self._center,self._range,self._threshold,self._max,self._reverse)
            return purpleObj

    def print_res(self) -> None:
        """prints the results of the user's inputs"""
        self._purple_source.print_results()

    def test_user(self):
        '''for testing'''
        pass


def run():
    '''for testing'''
    pass
    #user1 = UserInput(CENTER_FILE, RANGE_USER, THRESHOLD, USER_MAX, AQI_FILE, REVERSE_FILES)
    #user1.print_res()

if __name__ == '__main__':
    run()