[![Build Status](https://travis-ci.org/Sygic/sygic-maps-services-python.svg?branch=master)](https://travis-ci.org/Sygic/sygic-maps-services-python)

[![PyPI version](https://badge.fury.io/py/sygicmaps.svg)](https://badge.fury.io/py/sygicmaps)

# Sygic Maps Python Client

*Current repo is under development. It contains only subset of desired functionality.

The Sygic Maps Python Client is simplest way how to use Sygic Maps services from your Python code. The client contains method returning json response defined in the official [Sygic Maps services documentation](https://www.sygic.com/developers/maps-api-services/introduction).   

List of supported services in this package

- [Geocoding API](https://www.sygic.com/developers/maps-api-services/geolocation-and-search-api)

## Installation

    $ pip install -U sygicmaps
    
## Usage

Example of using Sygic [Geocoding API](https://www.sygic.com/developers/maps-api-services/geolocation-and-search-api). Before use ask for an API key from the [Sygic page](http://www.sygic.com/business/request-sygic-maps-trial-api-key).

### Client initialization

```python
import sygicmaps as s 

# Create a client with your API key 
client = s.Client(key='Your API key')

```
### Geocoding

```python
# Geocoding an fulltext address
result_geocoding = client.geocode("Bernauerstrasse 10 Berlin")

````

### Reverse geocoding

```python
# Reverse geocode a coordinates
result_reverse_geocoding = client.reverse_geocode("48.204876,16.351456")
```

### Batch geocoding
```python
# Batch geocode of list of fulltext addresses
result_batch_geocoding = client.geocode_batch(["Ashton Drive 3 Doncaster", "Rustoord 38 Beesel", "Via Stilicone 36 Milano"])
```
