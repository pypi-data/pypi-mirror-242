import re
from mappy.error import InvalidTypeError

class Point:
    def __init__(self, lat, lng=None):

        def is_valid_coordinate(value):
            return bool(re.match(r'^\d{2,3}\.\d{6,}$', str(value)))

        # 'string' case
        if isinstance(lat, str) and lng is None:
            coords = lat.split(',')
            if len(coords) != 2 or not all(is_valid_coordinate(coord.strip()) for coord in coords):
                raise InvalidTypeError(lat, "123.123456,12.123456")
            lat, lng = map(float, coords)
        
        # 'list' case
        elif isinstance(lat, list) and lng is None:
            if len(lat) != 2 or not all(is_valid_coordinate(coord) for coord in lat):
                raise InvalidTypeError(lat, [123.123456,12.123456])
            lat, lng = map(float, lat)

        # 'float' case
        elif isinstance(lat, float) and isinstance(lng, float):
            if not is_valid_coordinate(lat) or not is_valid_coordinate(lng):
                raise InvalidTypeError(f'lat={lat}, lng={lng}', 'lat=123.123456, lng=12.123456')
            lat, lng = map(float, [lat, lng])

        else:
            if not is_valid_coordinate(lat) or not is_valid_coordinate(lng):
                raise InvalidTypeError(f'lat={lat}, lng={lng}', 'lat=123.123456, lng=12.123456')

        self.lat = float(lat)
        self.lng = float(lng)

    def __str__(self):
        return f'{self.lat},{self.lng}'

    def to_list(self):
        return [self.lat, self.lng]