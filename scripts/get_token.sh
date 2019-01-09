#!/bin/bash
rm -f access_token.sh
touch access_token.sh
source ./token.sh
echo -n 'user_email:'
read user_email
echo -n 'password:'
read password
echo user_email = $user_email
echo password = $password
curl -s -q -X POST -H "Cache-Control: no-cache" -H "Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW" -F "grant_type=password" -F "client_id=$client_id" -F "client_secret=$client_secret" -F "email=$user_email" -F "password=$password" "https://owner-api.teslamotors.com/oauth/token" > access_token.sh
