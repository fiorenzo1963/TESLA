#!/bin/bash
source ./token.sh
cmd="wake_up"
curl -X POST --header "Authorization: Bearer $access_token" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" https://owner-api.teslamotors.com/api/1/vehicles/$id/$cmd
echo ''
