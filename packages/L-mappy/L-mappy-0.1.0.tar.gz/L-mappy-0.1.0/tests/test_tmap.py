import unittest
from unittest.mock import MagicMock, patch
import requests_mock
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

import os
import requests

from mappy import Mappy, Point, Address
from mappy.types.point import Point
from mappy.tmap import TmapAPI
from mappy.error.base import (
    MappyError, 
    InvalidTypeError, 
    InvalidValueError, 
    APIConnectionError, 
    APITimeoutError, 
    ResponseError
)

class MockResponse:
    def __init__(self, status_code, reason):
        self.status_code = status_code
        self.reason = reason

    def raise_for_status(self):
        raise HTTPError(response=self)

class TestTmapAPI(unittest.TestCase):

    # 0-1. test: __init__()
    @classmethod
    def setUpClass(cls):
        # 환경 변수 설정
        cls.expected_client_key = 'test_key'
        os.environ['TMAP_API_KEY'] = cls.expected_client_key

    def setUp(self):
        # 각 테스트 메서드 실행 전 API 인스턴스 생성
        self.api = TmapAPI()

    def test_init(self):
        # API 인스턴스 초기화 확인
        self.assertEqual(self.api.api_key, self.expected_client_key)
        self.assertIsInstance(self.api.session, requests.Session)
        self.assertEqual(self.api.headers['Content-Type'], 'application/json')
    
    # 0-2. test: _make_request()
    @patch('requests.Session.get')
    def test_make_request_http_error(self, mock_get):
        mock_get.side_effect = HTTPError(response=MockResponse(status_code=404, reason="Not Found"))
        with self.assertRaises(ResponseError) as context:
            self.api._make_request('http://example.com', {})
        self.assertIn('Not Found', str(context.exception))

    @patch('requests.Session.get')
    def test_make_request_connection_error(self, mock_get):
        mock_get.side_effect = ConnectionError()
        with self.assertRaises(APIConnectionError) as context:
            self.api._make_request('http://example.com', {})
        self.assertIn('http://example.com', str(context.exception))

    @patch('requests.Session.get')
    def test_make_request_timeout_error(self, mock_get):
        mock_get.side_effect = Timeout()
        with self.assertRaises(APITimeoutError) as context:
            self.api._make_request('http://example.com', {})
        self.assertIn('30', str(context.exception))

    @patch('requests.Session.get')
    def test_make_request_request_exception(self, mock_get):
        mock_get.side_effect = RequestException(response=MockResponse(status_code=500, reason="Server Error"))
        with self.assertRaises(ResponseError) as context:
            self.api._make_request('http://example.com', {})
        self.assertIn('Server Error', str(context.exception))

    # 1. test: get_direction()
    @patch('mappy.tmap.TmapAPI._make_request')
    def test_get_direction_returns_correct_route_info(self, mock_make_request):
        mock_make_request.return_value = {
            "features": [
                {
                    "geometry": {
                        'type': 'Point',
                        "coordinates": [126.83122524091145,37.19943077769807]
                    },
                    "properties": {
                        "totalDistance": 437,
                        "totalTime": 336
                    }
                },
                {
                    "type": "Feature",
                    "geometry": {
                        'type': 'LineString',
                        "coordinates": [
                            [126.83122524091145, 37.19943077769807],
                            [126.83118635662704, 37.199391892626345],
                            [126.83118635662704, 37.199391892626345],
                            [126.82885324393425, 37.19907244394085]
                        ]
                    },
                    "properties": {}
                },
                {
                    "type": "Feature",
                    "geometry": {
                        'type': 'Point',
                        "coordinates": [126.82885324393425, 37.19907244394085]
                    },
                    "properties": {}
                }
            ]
        }
        expected = {
            'start_coords': [126.83122524091145,37.19943077769807],
            'goal_coords': [126.82885324393425, 37.19907244394085],
            'duration': 336,
            'distance': 437,
            'path': [
                [126.83122524091145, 37.19943077769807],
                [126.83118635662704, 37.199391892626345],
                [126.83118635662704, 37.199391892626345],
                [126.82885324393425, 37.19907244394085]
            ]
        }
        result = self.api.get_direction({
            'start': Point([126.8314049, 37.1995648]),
            'goal': Point([126.8299873, 37.2002067])
        })
        self.assertEqual(result, expected)

    # 2-1. test: get_directions()
    @patch('mappy.tmap.TmapAPI._make_request')
    def test_get_directions_returns_all_routes(self, mock_make_request):
        mock_make_request.side_effect = [
            {
                "features": [
                    {
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.83122524091145,37.19943077769807]
                        },
                        "properties": {
                            "totalDistance": 437,
                            "totalTime": 336
                        }
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'LineString',
                            "coordinates": [
                                [126.83122524091145, 37.19943077769807],
                                [126.83118635662704, 37.199391892626345],
                                [126.83118635662704, 37.199391892626345],
                                [126.82885324393425, 37.19907244394085]
                            ]
                        },
                        "properties": {}
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.82885324393425, 37.19907244394085]
                        },
                        "properties": {}
                    }
                ],
            },
            {
                "features": [
                    {
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.83122524091145,37.19943077769807]
                        },
                        "properties": {
                            "totalDistance": 258,
                            "totalTime": 194
                        }
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'LineString',
                            "coordinates": [
                                [126.83122524091145, 37.19943077769807], 
                                [126.83118635662704, 37.199391892626345], 
                                [126.82971147157467, 37.200077898190834],
                                [126.82969202782122, 37.20011678223139]
                            ]
                        },
                        "properties": {}
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.82969202782122, 37.20011678223139]
                        },
                        "properties": {}
                    }
                ],
            },
        ]
        expected = [
            {
                'start_coords': [126.83122524091145,37.19943077769807],
                'goal_coords': [126.82885324393425, 37.19907244394085],
                'duration': 336,
                'distance': 437,
                'path': [
                    [126.83122524091145, 37.19943077769807],
                    [126.83118635662704, 37.199391892626345],
                    [126.83118635662704, 37.199391892626345],
                    [126.82885324393425, 37.19907244394085]
                ]
            },
            {
                'start_coords': [126.83122524091145, 37.19943077769807], 
                'goal_coords': [126.82969202782122, 37.20011678223139], 
                'duration': 194, 
                'distance': 258, 
                'path': [
                    [126.83122524091145, 37.19943077769807], 
                    [126.83118635662704, 37.199391892626345], 
                    [126.82971147157467, 37.200077898190834],
                    [126.82969202782122, 37.20011678223139]
                ]
            }
        ]
        result = self.api.get_directions([
            {
                'start': Point(lat='126.932863', lng=37.175001),
                'goal': Point('127.0505815,37.1990052'),
            }, 
            {
                'start': Point(lat='126.932863', lng=37.175001),
                'goal': Point('126.8364251,37.1947086'),
            },
        ])
        self.assertEqual(result, expected)

    # 2-2. test: get_directions(only_closest=True)
    @patch('mappy.tmap.TmapAPI._make_request')
    def test_get_directions_returns_only_closest_route(self, mock_make_request):
        mock_make_request.side_effect = [
            {
                "features": [
                    {
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.83122524091145,37.19943077769807]
                        },
                        "properties": {
                            "totalDistance": 437,
                            "totalTime": 336
                        }
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'LineString',
                            "coordinates": [
                                [126.83122524091145, 37.19943077769807],
                                [126.83118635662704, 37.199391892626345],
                                [126.83118635662704, 37.199391892626345],
                                [126.82885324393425, 37.19907244394085]
                            ]
                        },
                        "properties": {}
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.82885324393425, 37.19907244394085]
                        },
                        "properties": {}
                    }
                ],
            },
            {
                "features": [
                    {
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.83122524091145,37.19943077769807]
                        },
                        "properties": {
                            "totalDistance": 258,
                            "totalTime": 194
                        }
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'LineString',
                            "coordinates": [
                                [126.83122524091145, 37.19943077769807], 
                                [126.83118635662704, 37.199391892626345], 
                                [126.82971147157467, 37.200077898190834],
                                [126.82969202782122, 37.20011678223139]
                            ]
                        },
                        "properties": {}
                    },
                    {
                        "type": "Feature",
                        "geometry": {
                            'type': 'Point',
                            "coordinates": [126.82969202782122, 37.20011678223139]
                        },
                        "properties": {}
                    }
                ],
            },
        ]
        expected = {
            'start_coords': [126.83122524091145, 37.19943077769807], 
            'goal_coords': [126.82969202782122, 37.20011678223139], 
            'duration': 194, 
            'distance': 258, 
            'path': [
                [126.83122524091145, 37.19943077769807], 
                [126.83118635662704, 37.199391892626345], 
                [126.82971147157467, 37.200077898190834],
                [126.82969202782122, 37.20011678223139]
            ]
        }
        
        result = self.api.get_directions([
            {
                'start': Point(lat='126.932863', lng=37.175001),
                'goal': Point('127.0505815,37.1990052'),
            }, 
            {
                'start': Point(lat='126.932863', lng=37.175001),
                'goal': Point('126.8364251,37.1947086'),
            },
        ], only_closest=True)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
