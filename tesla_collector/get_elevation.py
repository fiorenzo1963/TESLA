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
        self.calls = 0
        self.hits = 0
        self.misses = 0

    def __get(self, latitude, longitude, headers={}):
        """Raw urlopen command"""
        req = Request("https://elevation-api.io/api/elevation?points=(%s,%s)" % (str(latitude), str(longitude)), headers=headers)
        try:
            req.data = urlencode(data).encode('utf-8') # Python 3
        except:
            try:
                req.add_data(urlencode(data)) # Python 2
            except:
                pass
        opener = build_opener()
        resp = opener.open(req)
        charset = resp.info().get('charset', 'utf-8')
        return json.loads(resp.read().decode(charset))

    def get(self, latitude, longitude, in_feet):
        if (self.calls % 100) == 0:
            print("get_elevation: stats: calls = " + str(self.calls) + ", hits = " + str(self.hits) + ", misses = " + str(self.misses))
        self.calls += 1
        try:
            if latitude != self.last_latitude or longitude != self.last_longitude:
                self.misses += 1
                #print("get_elevation: no cache hit")
                self.last_latitude = latitude
                self.last_longitude = longitude
                e = self.__get(latitude, longitude)
                self.last_elevation = e['elevations'][0]['elevation']
                #print("get_elevation: caching result: " + str(self.last_elevation))
            else:
                self.hits += 1
            if in_feet:
                return int(self.last_elevation / 0.3408)
            else:
                return int(self.last_elevation)
        except Exception as e:
            print("get_elevation: Elevation.get(): EXCEPTION: " + str(e))
            return 0
