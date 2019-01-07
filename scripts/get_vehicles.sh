#!/bin/bash
source ./token.sh
curl --header "Authorization: Bearer $access_token" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" https://owner-api.teslamotors.com/api/1/vehicles
echo ''
