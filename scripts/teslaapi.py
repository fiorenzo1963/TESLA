#!/usr/bin/python3

""" Simple Python class to access the Tesla JSON API
Reference:
      https://github.com/gglockner/teslajson
      http://docs.timdorr.apiary.io/
      https://www.teslaapi.io/
"""

from urllib.parse import urlencode
from urllib.request import Request, build_opener
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler
import json
import datetime
import sys
import os
import calendar

class Connection():
    """Connection to Tesla Motors API"""
    def __init__(self,
            access_info=None):
        self.info = access_info
        if self.info is None:
                # Nothing passed, read from access_info.json
                fd = open('access_info.json', 'r')
                data = fd.read()
                #print("STR: " + str(data))
                self.info = json.loads(data)
                #print("JS: " + str(self.info))
        self.head = {
            "Authorization": "Bearer %s" % self.info['token']['access_token'],
            "User-Agent": "Tesla/App/Fio/Py/TeslaAPI/0.1",
            "X-Tesla-User-Agent": "X-Tesla/Agent/App/Fio"
        }
        #print("self.head = " + str(self.head))

    def get(self, command):
        """Utility command to get data from API"""
        return self.post(command, None)
    
    def post(self, command, data={}):
        url = "%s%s" % (self.info['api']['api_url'], command)
        headers = self.head
        data = data
        #print("url = " + url)
        #print("headers = " + str(headers))
        #print("data = " + str(data))
        return self.__open(url, headers=self.head, data=data)
    
    def __open(self, url, headers={}, data=None):
        req = Request(url, headers=headers)
        if data is not None:
                req.data = urlencode(data).encode('utf-8')
        opener = build_opener()
        resp = opener.open(req)
        charset = resp.info().get('charset', 'utf-8')
        resp = resp.read().decode(charset)
        #print("__open(" + url + ").get() = '" + str(resp) + "'")
        js = json.loads(resp)
        #print("js = " + str(js))
        return js

class Vehicle():
    """Vehicle class
    There are 3 primary methods: wake_up, data_request and command.
    data_request and command both require a name to specify the data
    or command, respectively. These names can be found in the
    Tesla JSON API."""
    def __init__(self, connection, vehicle_id='0'):
        """Initialize vehicle class
        """
        self.connection = connection
        self.vehicle_id = vehicle_id

    def set_vehicle_id(self, vehicle_id):
        self.vehicle_id = vehicle_id

    def vehicles(self):
        """Return Vehicles"""
        return self.connection.get('/vehicles')

    #def get(self, command):
    #    """Utility command to get data from API"""
    #    return self.connection.get(command)
 
    def data_request(self, name):
        """Get vehicle data"""
        result = self.get('data_request/%s' % name)
        return result['response']
 
    def data_legacy(self):
        """Get vehicle data (legacy)"""
        result = self.get('')
        return result['response']
 
    def data(self):
        """Get vehicle data (legacy)"""
        result = self.get('data')
        return result['response']
    
    def wake_up(self):
        """Wake the vehicle"""
        return self.post('wake_up')
    
    #def command(self, name, data={}):
    #    """Run the command for the vehicle"""
    #    return self.post('/command/%s' % name, data)
    
    def get(self, command):
        """Utility command to get data from API"""
        return self.connection.get('/vehicles/%s/%s' % (self.vehicle_id, command))
    
    def post(self, command, data={}):
        """Utility command to post data to API"""
        return self.connection.post('/vehicles/%s/%s' % (self.vehicle_id, command), data)
