""" Simple Python class to access https://elevation-api.io

curl example:

    (latitude,longitude)
    curl "https://elevation-api.io/api/elevation?points=(46,-122)"

"""

try: # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, build_opener
    from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
except: # Python 2
    from urllib import urlencode
    from urllib2 import Request, build_opener
    from urllib2 import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
import json
import datetime
import calendar

class Elevation(object):
    """
    " cache last request
    """
    def __init__(self):
        self.last_latitude = 0.0
        self.last_longitude = 0.0
        self.last_elevation = 0.0

    def __get(self, latitude, longitude, headers={}):
        """Raw urlopen command"""
        req = Request("https://elevation-api.io/api/elevation?points=(%s,%s)" % (str(latitude), str(longitude)), headers=headers)
        opener = build_opener()
        resp = opener.open(req)
        charset = resp.info().get('charset', 'utf-8')
        return json.loads(resp.read().decode(charset))

    def get(self, latitude, longitude):
        if latitude == self.last_latitude and longitude == self.last_longitude:
            print("get_elevation: cache hit: return " + str(self.last_elevation))
            return self.last_elevation
        else:
            print("get_elevation: no cache hit")
            self.last_latitude = latitude
            self.last_longitude = longitude
            e = self.__get(latitude, longitude)
            self.last_elevation = e['elevations'][0]['elevation']
            print("get_elevation: caching result: " + str(self.last_elevation))
            return self.last_elevation
