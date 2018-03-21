import json
import time

import requests

from sygicmaps.input import Input


SERVICES_URL = "https://{}-geocoding.api.sygic.com"

GEOCODE_URL_PATH = "/v0/api/geocode"
GEOCODE_BATCH_URL_PATH = "/v0/api/batch/geocode"
REVERSE_GEOCODE_URL_PATH = "/v0/api/reversegeocode"


class Client(object):
    def __init__(self, key=None, region='eu', custom_url=None):
        if not key:
            raise ValueError("API key is not set.")

        if not custom_url:
            self.services_url = SERVICES_URL.format(region)
        else:
            self.services_url = custom_url

        self.session = requests.Session()
        self.key = key

    def __to_inputs_data(self, input):
        if type(input) is str:
            return Input(input)
        return input

    def __remove_nulls(self, d):
        return {k: v for k, v in d.items() if v is not None}

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

        url = self.services_url + GEOCODE_URL_PATH
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

        url = self.services_url + REVERSE_GEOCODE_URL_PATH
        response = requests_method(url, params=params)
        body = response.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])

    def geocode_batch(self, inputs: list):
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

        url = self.services_url + GEOCODE_BATCH_URL_PATH
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
            break;

        body = r.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])









