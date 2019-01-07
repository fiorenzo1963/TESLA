#!/bin/bash
source ./token.sh
cmd=""
case "$1" in
"data")
	cmd="vehicle_data"
	;;
"charge")
	cmd="data_request/charge_state"
	;;
"drive")
	cmd="data_request/drive_state"
	;;
"vehicle_state")
	cmd="data_request/vehicle_state"
	;;
"vehicle_config")
	cmd="data_request/vehicle_config"
	;;
*)
	echo $0: usage: $0: 'data|charge|drive|vehicle_state|vehicle_config'
	exit 1
	;;
esac
curl --header "Authorization: Bearer $access_token" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" https://owner-api.teslamotors.com/api/1/vehicles/$id/$cmd
echo ''
