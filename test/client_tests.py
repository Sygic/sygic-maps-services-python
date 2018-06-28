import sygicmaps as c
import requests_mock
import unittest as ut
import json


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


class ClientTests_v1(ut.TestCase):
    def __get_sample_response_json(self):
        sample_response_json = """{
              "results": [
                {
                  "components": [
                    {
                      "type": "admin_level_1",
                      "value": "Ticino"
                    },
                    {
                      "type": "admin_level_7",
                      "value": "Bellinzona"
                    },
                    {
                      "type": "admin_level_8",
                      "value": "Bellinzona"
                    },
                    {
                      "type": "country",
                      "value": "Switzerland"
                    }
                  ],
                  "formatted_result": "Bellinzona, Switzerland",
                  "location": {
                    "lat": 46.204537,
                    "lon": 9.019503
                  },
                  "location_type": "Centroid",
                  "type": "locality",
                  "country_iso": "che"
                }
              ],
              "status": "OK",
              "copyright": "© 2018 Sygic a.s."
            }"""
        return json.loads(sample_response_json)

    def __get_sample_batch_reverse_response_json(self):
        batch_reverse_response_json = """
        {
    "results": [
        [
            {
                "components": [
                    {
                        "type": "admin_level_1",
                        "value": "Ticino"
                    },
                    {
                        "type": "admin_level_7",
                        "value": "Bellinzona"
                    },
                    {
                        "type": "admin_level_8",
                        "value": "Bellinzona"
                    },
                    {
                        "type": "country",
                        "value": "Switzerland"
                    }
                ],
                "formatted_result": "Bellinzona, Switzerland",
                "location": {
                    "lat": 46.204537,
                    "lon": 9.019503
                },
                "location_type": "Centroid",
                "type": "locality",
                "country_iso": "che"
            }
        ],
        [
            {
                "components": [
                    {
                        "type": "admin_level_1",
                        "value": "Ticino"
                    },
                    {
                        "type": "admin_level_7",
                        "value": "Bellinzona"
                    },
                    {
                        "type": "admin_level_8",
                        "value": "Bellinzona"
                    },
                    {
                        "type": "country",
                        "value": "Switzerland"
                    }
                ],
                "formatted_result": "Bellinzona, Switzerland",
                "location": {
                    "lat": 46.204537,
                    "lon": 9.019503
                },
                "location_type": "Centroid",
                "type": "locality",
                "country_iso": "che"
            }
        ]
    ],
    "state": "FINISHED",
    "status": "OK",
    "copyright": "© 2018 Sygic a.s."
}"""
        return json.loads(batch_reverse_response_json)

    @requests_mock.mock()
    def test_default_call(self, m):
        response_json = self.__get_sample_response_json()

        response_json_str = json.dumps(response_json)
        response_results_json_str = json.dumps(response_json['results'])

        m.get('https://eu-geocoding.api.sygic.com/v1/api/geocode', text=response_json_str)

        client = c.Client(key="test-key", version='v1')
        result = client.geocode("Zochova 10 Bratislava")

        result_json = json.dumps(result)

        self.assertEqual(response_results_json_str, result_json)

    @requests_mock.mock()
    def test_reverse_geocode_batch(self, m):
        response_json = self.__get_sample_batch_reverse_response_json()

        response_json_str = json.dumps(response_json)
        response_results_json_str = json.dumps(response_json['results'])

        m.post('https://eu-geocoding.api.sygic.com/v1/api/batch/reversegeocode',
               headers={"Location":
                        "https://geocoding.api.sygic.com/v1/api/batch/reversegeocode/i21dsai21e2inian213?key=test-key"})

        m.get("https://geocoding.api.sygic.com/v1/api/batch/reversegeocode/i21dsai21e2inian213?key=test-key",
              text=response_json_str)

        client = c.Client(key="test-key", version='v1')
        result = client.reverse_geocode_batch(["46.204537,9.019503", "46.104537,9.019503"])
        result_json = json.dumps(result)

        self.assertEqual(response_results_json_str, result_json)

    @requests_mock.mock()
    def test_user_input_to_reverse_geocode_batch(self, m):
        client = c.Client(key="test-key", version='v1')

        with self.assertRaises(ValueError):
            client.reverse_geocode_batch(["46.2045379.019503", "46.104537,9.019503"])

        with self.assertRaises(ValueError):
            client.reverse_geocode_batch(["46.204537    9.019503", "46.104537,9.019503"])

        with self.assertRaises(ValueError):
            client.reverse_geocode_batch(["46.204537 9.019503", "46.104537,9.019503"])

