import requests

SERVICES_URL = "https://eu-geocoding.api.sygic.com/v0/api/"


class Client(object):
    def __init__(self, key=None):
        if not key:
            raise ValueError("API key is not set.")

        self.session = requests.Session()
        self.key = key

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

        url = SERVICES_URL + "/geocode"
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

        url = SERVICES_URL + "/reversegeocode"
        response = requests_method(url, params=params)
        body = response.json()

        api_status = body["status"]
        if api_status == "OK" or api_status == "NO_RESULTS":
            return body.get("results", [])

