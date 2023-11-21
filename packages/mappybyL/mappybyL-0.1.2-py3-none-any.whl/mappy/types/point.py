import re
from mappy.error import InvalidTypeError
import re

longitude_pattern = r'^(\+|-)?(?:180(?:(?:\.0{1,6})?)|(?:[1-9][0-9]?|1[0-7][0-9])(?:(?:\.\d{1,6})?))$'
latitude_pattern = r'^(\+|-)?(?:90(?:(?:\.0{1,6})?)|(?:[1-8]?[0-9])(?:(?:\.\d{1,6})?))$'

class Point:
    def __init__(self, lng, lat=None):

        def is_valid_longitude(value):
            return bool(re.match(longitude_pattern, str(value)))

        def is_valid_latitude(value):
            return bool(re.match(latitude_pattern, str(value)))

        # 'string' case
        if isinstance(lng, str) and lat is None:
            coords = lng.split(',')
            if len(coords) != 2 or not (is_valid_longitude(coords[0].strip()) and is_valid_latitude(coords[1].strip())):
                raise InvalidTypeError(lng, "123.123456,12.123456")
            lng, lat = map(float, coords)
        
        # 'list' case
        elif isinstance(lng, list) and lat is None:
            if len(lng) != 2 or not (is_valid_longitude(lng[0]) and is_valid_latitude(lng[1])):
                raise InvalidTypeError(lng, "[123.123456,12.123456]")
            lng, lat = map(float, lng)

        # 'float' case
        elif isinstance(lng, float) and isinstance(lat, float):
            if not (is_valid_longitude(lng) and is_valid_latitude(lat)):
                raise InvalidTypeError(f'lng={lng}, lat={lat}', "lng=123.123456, lat=12.123456")
            lng, lat = float(lng), float(lat)

        else:
            raise InvalidTypeError(f'Invalid input: lng={lng}, lat={lat}', "lng=123.123456, lat=12.123456")

        self.lng = float(lng)
        self.lat = float(lat)

    def __str__(self):
        return f'{self.lng},{self.lat}'

    def to_list(self):
        return [self.lng, self.lat]