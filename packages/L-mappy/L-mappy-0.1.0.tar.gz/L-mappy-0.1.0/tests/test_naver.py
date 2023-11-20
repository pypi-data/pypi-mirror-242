import unittest
from unittest.mock import patch, Mock, MagicMock
import requests_mock
from requests.exceptions import HTTPError, ConnectionError, Timeout, RequestException

import os
import requests

from mappy import Mappy, Point, Address
from mappy.types.point import Point
from mappy.naver import NaverAPI
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

class TestNaverAPI(unittest.TestCase):

    # 0-1. test: __init__()
    @classmethod
    def setUpClass(cls):
        # 환경 변수 설정
        cls.expected_client_id = 'test_id'
        cls.expected_client_secret = 'test_secret'
        os.environ['NAVER_CLIENT_ID'] = cls.expected_client_id
        os.environ['NAVER_CLIENT_SECRET'] = cls.expected_client_secret

    def setUp(self):
        # 각 테스트 메서드 실행 전 API 인스턴스 생성
        self.api = NaverAPI()

    def test_init(self):
        # API 인스턴스 초기화 확인
        self.assertEqual(self.api.client_id, self.expected_client_id)
        self.assertEqual(self.api.client_secret, self.expected_client_secret)
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

    # 1. test: get_geocode()
    @patch('mappy.naver.NaverAPI._make_request')
    def test_get_geocode_returns_correct_coordinates(self, mock_make_request):
        mock_make_request.return_value = {
            'status': 'OK',
            'meta': {
                'totalCount': 1
            }, 
            'addresses': [
                {
                    'x': '126.831405', 
                    'y': '37.1995655',
                }
            ],
            'errorMessage': ''
        }
        expected = [126.831405, 37.1995655]
        result = self.api.get_geocode("경기 화성시 남양읍 시청로 159")
        self.assertEqual(result, expected)
    
    # 2. test: get_geocodes()
    def test_get_geocodes_returns_correct_coordinates(self):
        pass

    # 3. test: get_direction()
    @patch('mappy.naver.NaverAPI._make_request')
    def test_get_direction_returns_correct_route_info(self, mock_make_request):
        mock_make_request.return_value = {
            "code": 0,
            "route": {
                "traoptimal": [{
                        "summary": {
                            "start": {
                                "location": [126.8314049, 37.1995648]
                            },
                            "goal": {
                                "location": [126.8299873, 37.2002067],
                            },
                            "distance": 595,
                            "duration": 167953,
                        },
                        "path": [
                            [126.8311408, 37.1993551],
                            [126.8302911, 37.2000002]
                        ],
                    }]
            }
        }
        expected = {
            'start_coords': [126.8314049, 37.1995648],
            'goal_coords': [126.8299873, 37.2002067],
            'duration': 167953,
            'distance': 595,
            'path': [[126.8311408, 37.1993551], [126.8302911, 37.2000002]]
        }
        result = self.api.get_direction({
            'start': Point([126.8314049, 37.1995648]),
            'goal': Point([126.8299873, 37.2002067])
        })
        self.assertEqual(result, expected)

    # 4-1. test: get_directions()
    @patch('mappy.naver.NaverAPI._make_request')
    def test_get_directions_returns_all_routes(self, mock_make_request):
        mock_make_request.side_effect = [
            {
                "code": 0,
                "route": {
                "traoptimal": [{
                        "summary": {
                            "start": {
                                "location": [126.8314049, 37.1995648]
                            },
                            "goal": {
                                "location": [126.8299873, 37.2002067],
                            },
                            "distance": 595,
                            "duration": 167953,
                        },
                        "path": [
                            [126.8311408, 37.1993551],
                            [126.8302911, 37.2000002]
                        ],
                    }]
                }
            },
            {
                "code": 0,
                "route": {
                    "traoptimal": [{
                        "summary": {
                            "start": {
                                "location": [126.8314049, 37.1995648]
                            },
                            "goal": {
                                "location": [126.8286669, 37.198903],
                            },
                            "distance": 519,
                            "duration": 166238,
                        },
                        "path": [
                            [126.8311408, 37.1993551],
                            [126.828901, 37.1990639]
                        ],
                    }]
                }
            }
        ]
        expected = [
            {
                'start_coords': [126.8314049, 37.1995648],
                'goal_coords': [126.8299873, 37.2002067],
                'duration': 167953,
                'distance': 595,
                'path': [[126.8311408, 37.1993551], [126.8302911, 37.2000002]]
            },
            {
                'start_coords': [126.8314049, 37.1995648],
                'goal_coords': [126.8286669, 37.198903],
                'duration': 166238,
                'distance': 519,
                "path": [[126.8311408, 37.1993551],[126.828901, 37.1990639]]
            }
        ]
        result = self.api.get_directions([
            {'start': "testdata1", 'goal': "testdata1"},
            {'start': "testdata2", 'goal': "testdata2"},
        ])
        self.assertEqual(result, expected)

    # 4-2. test: get_directions(only_closest=True)
    @patch('mappy.naver.NaverAPI._make_request')
    def test_get_directions_returns_only_closest_route(self, mock_make_request):
        mappy = Mappy()
        
        mock_make_request.side_effect = [
            {
                "code": 0,
                "route": {
                "traoptimal": [{
                        "summary": {
                            "start": {
                                "location": [126.8314049, 37.1995648]
                            },
                            "goal": {
                                "location": [126.8299873, 37.2002067],
                            },
                            "distance": 595,
                            "duration": 167953,
                        },
                        "path": [
                            [126.8311408, 37.1993551],
                            [126.8302911, 37.2000002]
                        ],
                    }]
                }
            },
            {
                "code": 0,
                "route": {
                    "traoptimal": [{
                        "summary": {
                            "start": {
                                "location": [126.8314049, 37.1995648]
                            },
                            "goal": {
                                "location": [126.8286669, 37.198903],
                            },
                            "distance": 519,
                            "duration": 166238,
                        },
                        "path": [
                            [126.8311408, 37.1993551],
                            [126.828901, 37.1990639]
                        ],
                    }]
                }
            }
        ]
        expected = {
            'start_coords': [126.8314049, 37.1995648],
            'goal_coords': [126.8286669, 37.198903],
            'duration': 166238,
            'distance': 519,
            "path": [[126.8311408, 37.1993551],[126.828901, 37.1990639]]
        }
        result = self.api.get_directions([
            {'start': "testdata1", 'goal': "testdata1"},
            {'start': "testdata2", 'goal': "testdata2"},
        ], only_closest=True)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    # unittest.main()
    unittest.TextTestRunner(verbosity=2).run(unittest.makeSuite(TestNaverAPI))