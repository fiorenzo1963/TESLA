#!/bin/bash
#
# tesla creds
#
client_id='81527cff06843c8634fdc09e8ac0abefb46ac849f38fe1e431c2ef2106796384'
client_secret='c7257eb71a564034f9419ee651c7d0e5f7aa6bfbd18bafb5c5c033b093bb2fa3'
access_token=`jq .access_token < access_token.json | sed -e 's/"//g'`
token_type=`jq .token_type < access_token.json | sed -e 's/"//g'`
expires_in=`jq .expires_in < access_token.json | sed -e 's/"//g'`
refresh_token=`jq .refresh_token < access_token.json | sed -e 's/"//g'`
created_at=`jq .created_at < access_token.json | sed -e 's/"//g'`
#
# my app
#
user_agent="curl/7.58.0/Linux"
tesla_app="fioTeslaApp/0.0.1"
#
#
#
source ./vehicle_id
#
#
#
