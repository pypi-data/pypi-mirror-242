import re
from mappy.error import InvalidTypeError

class Point:
    def __init__(self, lng, lat=None):

        def is_valid_coordinate(value):
            return bool(re.match(r'^\d{2,3}\.\d{6,}$', str(value)))

        # 'string' case
        if isinstance(lng, str) and lat is None:
            coords = lng.split(',')
            if len(coords) != 2 or not all(is_valid_coordinate(coord.strip()) for coord in coords):
                raise InvalidTypeError(lng, "123.123456,12.123456")
            lng, lat = map(float, coords)
        
        # 'list' case
        elif isinstance(lng, list) and lat is None:
            if len(lng) != 2 or not all(is_valid_coordinate(coord) for coord in lng):
                raise InvalidTypeError(lng, [123.123456,12.123456])
            lng, lat = map(float, lng)

        # 'float' case
        elif isinstance(lng, float) and isinstance(lat, float):
            if not is_valid_coordinate(lng) or not is_valid_coordinate(lat):
                raise InvalidTypeError(f'lng={lng}, lat={lat}', 'lng=123.123456, lat=12.123456')
            lng, lat = map(float, [lng, lat])

        else:
            if not is_valid_coordinate(lng) or not is_valid_coordinate(lat):
                raise InvalidTypeError(f'lng={lng}, lat={lat}', 'lng=123.123456, lat=12.123456')

        self.lng = float(lng)
        self.lat = float(lat)

    def __str__(self):
        return f'{self.lng},{self.lat}'

    def to_list(self):
        return [self.lng, self.lat]