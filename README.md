# Sygic Maps Python Client

*Current repo is under development. It contains only subset of desired functionality.

The Sygic Maps Python Client is simplest way how to use Sygic Maps services from your Python code. The client contains method returning json response defined in the official [Sygic Maps services documentation](https://www.sygic.com/developers/maps-api-services/introduction).   

List of supported services in this package

- [Geocoding API] (https://www.sygic.com/developers/maps-api-services/geolocation-and-search-api)

## Installation

    $ pip install -U sygicmaps
    
## Usage

Example of using Sygic [Geocoding API] (https://www.sygic.com/developers/maps-api-services/geolocation-and-search-api). Before use ask for an API key from the [Sygic page](http://www.sygic.com/business/request-sygic-maps-trial-api-key).

```python
import sygicmaps.client as s 

# Create a client with your API key 
client = s.Client(key='Your API key')

# Geocoding an fulltext address
result_geocoding = client.geocode("Bernauerstrasse 10 Berlin")

# Reverse geocode a coordinates
result_reverse_geocoding = client.reverse_geocode(location="48.204876,16.351456")

