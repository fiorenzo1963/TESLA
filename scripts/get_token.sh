#!/bin/bash
#
# tesla creds
#
client_id='81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
client_secret='c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
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
