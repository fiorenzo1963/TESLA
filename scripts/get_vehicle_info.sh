#!/bin/bash
source ./token.sh
cmd=""
case "$1" in
"data")
	cmd="vehicle_data" # legacy
	;;
"vehicle_data")
	cmd="vehicle_data"
	;;
"service_data")
	cmd="service_data"
	;;
"mobile_enabled")
	cmd="mobile_enabled"
	;;
"charge_state")
	cmd="data_request/charge_state"
	;;
"climate_state")
	cmd="data_request/climate_state"
	;;
"drive_state")
	cmd="data_request/drive_state"
	;;
"gui_settings")
	cmd="data_request/gui_settings"
	;;
*)
	echo $0: usage: $0: 'data|vehicle_data|service_data|mobile_enabled|charge_state|climate_state|drive_state|gui_settings'
	exit 1
	;;
esac
curl --header "Authorization: Bearer $access_token" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" https://owner-api.teslamotors.com/api/1/vehicles/$id/$cmd
echo ''
