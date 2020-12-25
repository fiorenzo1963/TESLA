#!/usr/bin/python3

""" Simple Python class to get TESLA Token
References:
       https://github.com/gglockner/teslajson
       http://docs.timdorr.apiary.io/
       https://www.teslaapi.io/
"""

from urllib.parse import urlencode
from urllib.request import Request, build_opener
from urllib.request import ProxyHandler, HTTPBasicAuthHandler, HTTPHandler

import json
import datetime
import calendar
import sys
import os

#
# use this if nothing is passed
#
tesla_info_2020_12_24 = {
        "client_id" : "81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384",
        "client_secret" : "c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3",
        "token_url" : "https://owner-api.teslamotors.com/oauth/token",
        "api_url" : "https://owner-api.teslamotors.com/api/1"
}

class TeslaToken(object):
    def __init__(self,
            email='',
            password='',
            tesla_info=tesla_info_2020_12_24):
        self.tesla_info = tesla_info
        self.oauth = {
                "grant_type" : "password",
                "client_id" : self.tesla_info['client_id'],
                "client_secret" : self.tesla_info['client_secret'],
                "email" : email,
                "password" : password
        }

    """Get Token from Tesla API"""
    def get(self):
        """Utility command to post data to API"""
        req = Request(self.tesla_info['token_url'])
        req.data = urlencode(self.oauth).encode('utf-8') # Python 3
        opener = build_opener()
        resp = opener.open(req)
        #print("resp = " + str(resp))
        charset = resp.info().get('charset', 'utf-8')
        #print("charset = " + str(charset))
        s = resp.read().decode(charset)
        #print("s = " + str(s))
        js = json.loads(s)
        #print("js = " + str(js))
        return js

    """Get API info from Tesla API"""
    def get_info(self):
        return self.tesla_info

def main():
        #print(str(len(sys.argv)))
        if len(sys.argv) != 3:
                print("teslatoken: usage: teslatoken user_email password")
                sys.exit(1)
        arg_email = sys.argv[1]
        arg_password = sys.argv[2]
        tt = TeslaToken(email=arg_email, password=arg_password)
        #print("API info: " + str(tt.get_info()))
        token = tt.get()
        #print("Tesla token for " + arg_email + ": " + str(token))
        print("Writing User email, Token and API info to ./access_info.json")
        info = { }
        info['api'] = tt.get_info()
        info['token'] = token
        info['user_email'] = arg_email
        #print("info = " + str(info))
        fd = open("access_info.json", "w")
        fd.write(json.dumps(info, indent=8))

main()
