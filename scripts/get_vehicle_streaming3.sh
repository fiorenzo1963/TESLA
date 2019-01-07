#!/bin/bash
source ./token.sh
#curl --user "$user_email:$vehicle_token_1" -i -N --output - --header "Sec-WebSocket-Key: SGVsbG8sIHevcmxkIQ==" -H "Sec-WebSocket-Version: 13" -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: streaming.vn.teslamotors.com" -H "Origin: https://streaming.vn.teslamotors.com" https://streaming.vn.teslamotors.com/connect/$vehicle_id
#curl --user "$user_email:$vehicle_token_1" -i -N --output - --header "Sec-WebSocket-Key: SGVsbG8sIHevcmxkIQ==" -H "Sec-WebSocket-Version: 13" -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: streaming.vn.teslamotors.com" -H "Origin: https://streaming.vn.teslamotors.com" "https://streaming.vn.teslamotors.com/connect/$vehicle_id?values=time,speed,odometer,elevation,heading,est_lat,est_lng,soc,power,shift_state,range,est_range"
curl --user "$user_email:$vehicle_token_1" -i -N --output - --header "Sec-WebSocket-Key: SGVsbG8sIHevcmxkIQ==" -H "Sec-WebSocket-Version: 13" -H "Connection: Upgrade" -H "Upgrade: websocket" -H "Host: streaming.vn.teslamotors.com" -H "Origin: https://streaming.vn.teslamotors.com" "https://streaming.vn.teslamotors.com/stream/$vehicle_id?values=time,speed,odometer,elevation,heading,est_lat,est_lng,soc,power,shift_state,range,est_range"
echo ''