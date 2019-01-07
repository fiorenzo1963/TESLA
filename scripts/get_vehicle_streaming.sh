#!/bin/bash
source ./token.sh
#curl --include --user $user_email:$vehicle_token_1 --header "Inactivity-Timeout: 30" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" "https://streaming.vn.teslamotors.com/stream/$vehicle_id/?values=time,speed,odometer,elevation,heading,est_lat,est_lng,soc,power,shift_state,range,est_range"
curl --user $user_email:$vehicle_token_1 --header "Inactivity-Timeout: 30" --header "User-Agent: $user_agent" --header "X-Tesla-User-Agent: $tesla_app" "https://streaming.vn.teslamotors.com/stream/$vehicle_id/?values=time,speed,odometer,elevation,heading,est_lat,est_lng,soc,power,shift_state,range,est_range"
echo ''
