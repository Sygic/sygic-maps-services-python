import json
import time

import requests

from sygicmaps.input import Input


SERVICES_URL = "https://{}-geocoding.api.sygic.com"

GEOCODE_URL_PATH = "/{}/api/geocode"
GEOCODE_BATCH_URL_PATH = "/{}/api/batch/geocode"
REVERSE_GEOCODE_URL_PATH = "/{}/api/reversegeocode"
REVERSE_GEOCODE_BATCH_URL_PATH = "/{}/api/batch/reversegeocode"


class Client(object):
    def __init__(self, key=None, region='eu', custom_url=None, version='v0'):
        if not key:
            raise ValueError("API key is not set.")

        if custom_url:
            self.services_url = custom_url
        else:
            self.services_url = SERVICES_URL.format(region)
        self.version = version

        self.session = requests.Session()
        self.key = key

    @staticmethod
    def __to_inputs_data(input):
        if type(input) is str:
            return Input(input)
        return input

    @staticmethod
    def __remove_nulls(d):
        return {k: v for k, v in d.items() if v is not None}

    def __get_services_url_geocode(self):
        return self.services_url + GEOCODE_URL_PATH.format(self.version)

    def __get_services_url_reverse_geocode_batch(self):
        return self.services_url + REVERSE_GEOCODE_BATCH_URL_PATH.format(self.version)

    def __get_services_url_geocode_batch(self):
        return self.services_url + GEOCODE_BATCH_URL_PATH.format(self.version)

    def __get_services_url_reverse_geocode(self):
        return self.services_url + REVERSE_GEOCODE_URL_PATH.format(self.version)

    @staticmethod
    def __make_coords_dict_helper(line_of_coords):
        lat, lon = line_of_coords.split(',')
        return dict(lat=lat, lon=lon)

    def geocode(self, location=None, country=None, city=None, suburb=None, street=None, house_number=None,
                zip=None, admin_level_1=None):

        params = {"key": self.key}

        if location:
            params["location"] = location
        if country:
            params["country"] = country
        if city:
            params["city"] = city
        if suburb:
            params["suburb"] = suburb
        if street:
            params["street"] = street
        if house_number:
            params["house_number"] = house_number
        if zip:
            params["zip"] = zip
        if admin_level_1:
            params["admin_level_1"] = admin_level_1

        requests_method = self.session.get

        url = self.__get_services_url_geocode()
        response = requests_method(url, params=params)
        body = response.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])

    def reverse_geocode(self, location=None):

        params = {"key": self.key}

        if location:
            params["location"] = location

        requests_method = self.session.get

        url = self.__get_services_url_reverse_geocode()
        response = requests_method(url, params=params)
        body = response.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])

    def __geocode_batch_base(self, post_data, services_url):
        url = services_url
        params = {"key": self.key}
        post_body = json.dumps(post_data)
        r = requests.post(url, data=post_body, params=params, headers={'Content-type': 'application/json'})

        results_url = r.headers.get('location')

        r = requests.get(results_url)

        while True:
            retry_after = r.headers.get('retry-after')
            if retry_after is not None:
                time.sleep(int(retry_after))
                r = requests.get(results_url)
                continue
            break

        body = r.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])

    def reverse_geocode_batch(self, locations: list):
        inputs = locations
        if type(inputs) is str:
            inputs = [inputs]
        if len(inputs) == 0:
            raise ValueError("Param locations has to contain some items.")
        if len(inputs) >= 10000:
            raise ValueError("Param locations has to be less than 10000.")
        if ',' not in inputs[0]:
            raise ValueError("No comma delimiter found, please verify that location input format is list of LAT,LON")

        inputs = list(map(lambda line_of_coords: self.__make_coords_dict_helper(line_of_coords), inputs))
        json_string = json.dumps(inputs)
        post_data = list(json.loads(json_string))

        services_url = self.__get_services_url_reverse_geocode_batch()

        return self.__geocode_batch_base(post_data, services_url)

    def geocode_batch(self, locations: list):
        inputs = locations
        if type(inputs) is str:
            inputs = [inputs]
        if len(inputs) == 0:
            raise ValueError("Param locations has to contain some items.")
        if len(inputs) >= 10000:
            raise ValueError("Param locations has to be less than 10000.")

        inputs_data = list(map(self.__to_inputs_data, inputs))
        json_string = json.dumps(inputs_data, default=lambda x: x.__dict__)

        post_data = list(json.loads(json_string))
        post_data = list(map(self.__remove_nulls, post_data))

        services_url = self.__get_services_url_geocode_batch()

        return self.__geocode_batch_base(post_data, services_url)







