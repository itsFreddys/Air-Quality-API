import user_class

def collect_center() -> str:
    """Collects the users center input,
    returns center input minus the CENTER part"""
    center = input()
    if center.startswith('CENTER '):
        temp_cent = center.replace('CENTER ', '')
        return temp_cent

def collect_range() -> int:
    """Collects the users range input,
        returns RANGE input minus the RANGE part"""
    user_range = input()
    if user_range.startswith('RANGE '):
        temp_range = user_range.replace('RANGE ', '')
        return int(temp_range)

def collect_threshold() -> int:
    """Collects the users THRESHOLD input,
        returns THRESHOLD input minus the THRESHOLD part"""
    user_threshold = input()
    if user_threshold.startswith('THRESHOLD '):
        temp_threshold = user_threshold.replace('THRESHOLD ', '')
        return int(temp_threshold)

def collect_max() -> int:
    """Collects the users MAX input,
        returns MAX input minus the MAX part"""
    user_max = input()
    if user_max.startswith('MAX '):
        temp_max = user_max.replace('MAX ', '')
        return int(temp_max)

def collect_aqi_source() -> str:
    """Collects the users AQI input,
        returns AQI input minus the AQI part"""
    user_aqi_source = input()
    if user_aqi_source.startswith('AQI '):
        temp_aqi = user_aqi_source.replace('AQI ', '')
        return temp_aqi

def collect_reverse_source():
    """Collects the REVERSE input,
        returns REVERSE input minus the REVERSE part"""
    user_reverse = input()
    if user_reverse.startswith('REVERSE '):
        temp_reverse = user_reverse.replace('REVERSE ', '')
        return temp_reverse


def start_program() -> None:
    """Running this function will run the program,
        you'll need to provide the inputs"""
    center = collect_center()
    my_range = collect_range()
    thresh = collect_threshold()
    my_max = collect_max()
    my_aqi = collect_aqi_source()
    reverse_source = collect_reverse_source()

    user1 = user_class.UserInput(center, my_range, thresh, my_max, my_aqi, reverse_source)
    user1.print_res()


def run():
    '''testing in module'''
    start_program()

if __name__ == '__main__':
    run()