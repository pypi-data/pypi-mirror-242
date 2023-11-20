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

class TmapAPI:
    def __init__(self):
        self.session = requests.Session()

        self.api_key = os.getenv('TMAP_API_KEY')

        self.headers = {
            'appKey': self.api_key,
            'Content-Type': 'application/json'
        }
        self.directions_url = "https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1&callback=result"

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

    def get_walking_direction(self, route_info, waypoints=None, options=None, cartype=None):
        start = route_info['start']
        startX, startY = start.to_list()
        goal = route_info['goal']
        endX, endY = goal.to_list()

        params = {
            'startX': startX,
            'startY': startY,
            'endX': endX,
            'endY': endY,
            'startName': 'start',
            'endName': 'end'
        }

        if waypoints:
            pass
    
        if options:
            pass

        if cartype:
            pass

        response_data = self._make_request(self.directions_url, params)
        if response_data:
            summary = response_data['features'][0]['properties']
    
            path = []
            for feature in response_data['features']:
                if feature['geometry']['type'] == 'LineString':
                    path.extend(feature['geometry']['coordinates'])
                    
            return {
                'start_coords': Point(response_data['features'][0]['geometry']['coordinates']).to_list(),
                'goal_coords': Point(response_data['features'][-1]['geometry']['coordinates']).to_list(),
                'duration': summary['totalTime'],
                'distance': summary['totalDistance'],
                'path': [[coord[0], coord[1]] for coord in path]
            }
        else:
            raise InvalidValueError([str(start), str(goal)])

    def get_walking_directions(self, routes, waypoints=None, options=None, cartype=None, only_closest=False):
        all_directions = []
        for route in routes:
            direction = self.get_walking_direction({
                'start': route['start'],
                'goal': route['goal']
            }, waypoints, options, cartype)
            all_directions.append(direction)

        if only_closest:
            return min(all_directions, key=lambda x: x['distance'])

        return all_directions
