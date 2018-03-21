import sygicmaps as c
import responses
import requests
import requests_mock
import unittest as ut
import json
import os


class ClientTests(ut.TestCase):
    def __get_sample_response_json(self):
        sample_response_json = """ {
            "results": [
                {
                    "location": {
                        "country": "Germany",
                        "city": "Berlin",
                        "street": "Bernauer Straße",
                        "house_number": "36",
                        "zip": "13355",
                        "admin_level_1": "Berlin"
                    },
                    "geometry": {
                        "lat": 52.53874,
                        "lon": 13.39849
                    },
                    "confidence": 0.25454903381642513,
                    "distance": 0
                }
            ],
            "status": "OK",
            "copyright": "© 2018 Sygic a.s."
        }   """
        return json.loads(sample_response_json)


    @requests_mock.mock()
    def test_default_call(self, m):
        response_json = self.__get_sample_response_json()

        print(response_json)
        response_json_str = json.dumps(response_json)
        response_results_json_str = json.dumps(response_json['results'])

        m.get('https://eu-geocoding.api.sygic.com/v0/api/geocode', text=response_json_str)

        client = c.Client(key="test-key")
        result = client.geocode("Zochova 10 Bratislava")

        result_json = json.dumps(result)

        self.assertEqual(response_results_json_str, result_json)

    @requests_mock.mock()
    def test_region_parameter(self, m):
        response_json = self.__get_sample_response_json()

        print(response_json)
        response_json_str = json.dumps(response_json)
        response_results_json_str = json.dumps(response_json['results'])

        m.get('https://na-geocoding.api.sygic.com/v0/api/geocode', text=response_json_str)

        client = c.Client(key="test-key", region="na")
        result = client.geocode("Zochova 10 Bratislava")

        result_json = json.dumps(result)

        self.assertEqual(response_results_json_str, result_json)