import os
import requests
from dotenv import load_dotenv
from .types.point import Point
from .error.base import (
    InvalidTypeError,
    InvalidValueError,
    APIConnectionError,
    APITimeoutError,
    ResponseError
)

load_dotenv()

class NaverAPI:
    def __init__(self):
        self.session = requests.Session()

        self.client_id = os.getenv('NAVER_CLIENT_ID')
        self.client_secret = os.getenv('NAVER_CLIENT_SECRET')
        
        self.headers = {
            'X-NCP-APIGW-API-KEY-ID': self.client_id,
            'X-NCP-APIGW-API-KEY': self.client_secret,
            'Content-Type': 'application/json'
        }
        self.directions_url = "https://naveropenapi.apigw.ntruss.com/map-direction/v1/driving"
        self.geocoding_url = "https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode"

    def _make_request(self, url, params):
        try:
            response = self.session.get(url, headers=self.headers, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise ResponseError(e.response.status_code, e.response.reason)
        except requests.exceptions.ConnectionError:
            raise APIConnectionError(url)
        except requests.exceptions.Timeout:
            raise APITimeoutError(30)  # 예를 들어 30초
        except requests.exceptions.RequestException as e:
            raise ResponseError(e.response.status_code, e.response.reason)

        return response.json()
        
    # geocode
    def get_geocode(self, query):
        params = {'query': query}
        response_data = self._make_request(self.geocoding_url, params)
        if response_data['status'] == 'OK':
            address_info = response_data['addresses'][0]
            return Point(address_info['x'], address_info['y']).to_list()
        else:
            raise InvalidValueError(query)

    def get_geocodes(self, addresses):
        points = []
        for address in addresses:
            points.append(self.get_geocode(address))
        return points

    # direction
    def get_driving_direction(self, route_info, waypoints=None, options=None, cartype=None):
        start = route_info['start']
        goal = route_info['goal']
        params = {'start': f'{start}', 'goal': f'{goal}'}

        if waypoints:
            pass

        if options:
            pass
        
        if cartype:
            pass

        response_data = self._make_request(self.directions_url, params)
        if response_data['code'] == 0:
            summary = response_data['route']['traoptimal'][0]['summary']

            return {
                'start_coords': Point(summary['start']['location'][0], summary['start']['location'][1]).to_list(),
                'goal_coords': Point(summary['goal']['location'][0], summary['goal']['location'][1]).to_list(),
                'duration': summary['duration'],
                'distance': summary['distance'],
                'path': response_data['route']['traoptimal'][0]['path']
            }
        else:
            raise InvalidValueError([str(start), str(goal)])

    def get_driving_directions(self, routes, waypoints=None, options=None, cartype=None, only_closest=False):
        all_directions = []
        for route in routes:
            direction = self.get_driving_direction({
                'start': route['start'],
                'goal': route['goal']
            }, waypoints, options, cartype)
            all_directions.append(direction)

        if only_closest:
            return min(all_directions, key=lambda x: x['distance'])

        return all_directions
