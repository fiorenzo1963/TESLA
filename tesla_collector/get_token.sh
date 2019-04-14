#!/bin/bash
#
# tesla creds
#
client_id='e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e'
client_secret='c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220'
#
# my app
#
user_agent="curl/7.58.0/Linux"
tesla_app="fioTeslaApp/0.0.1"
#
# fio vehicle id -- FIXME: shouldn't be here
#
id="59707325074886112"
vehicle_id="749879137"
#
#
#
rm -f access_token.json
echo -n 'user_email:'
read user_email
echo -n 'password:'
read password
echo user_email = $user_email
echo password = $password
curl -s -q -X POST -H "Cache-Control: no-cache" -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "grant_type=password" -F "client_id=$client_id" -F "client_secret=$client_secret" -F "email=$user_email" -F "password=$password" "https://owner-api.teslamotors.com/oauth/token" > access_token.json
