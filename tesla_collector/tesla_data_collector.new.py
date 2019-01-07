#!/usr/local/bin/python2
##!/usr/bin/python

import teslajson
import get_elevation
import os
import sys
import time

tesla_info = {
    "id":"e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e",
    "secret":"c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220",
    "baseurl": "https://owner-api.teslamotors.com",
    "api": "/api/1/"
}

access_token = "51be69ce38106bf4204c3837f55bb2ec005be662e1969028fdad35249e032c72"

STATE_ERROR = -1
STATE_UNKNOWN = 0
STATE_NOT_ONLINE = 1
STATE_CHARGING = 2
STATE_CHARGING_COMPLETE = 3
STATE_NOT_CHARGING = 4
STATE_DRIVING = 5

SLEEP_STATE_UNKNOWN = 30
SLEEP_STATE_NOT_ONLINE = 60
SLEEP_STATE_ERROR = 30
SLEEP_STATE_CHARGING = 30
SLEEP_STATE_CHARGING_COMPLETE = 30
SLEEP_STATE_NOT_CHARGING = 30
SLEEP_STATE_DRIVING = 15

# charge_state['charging_state'] = 'Disconnected'|'Starting'|'Charging'|'Complete'
# drive_state['shift_state'] = None|'P'|'D'|'R'
# drive_state['speed'] = None|<speed>

# charge_state = {u'user_charge_enable_request': None, u'scheduled_charging_start_time': None, u'charge_current_request': 40, u'charge_to_max_range': False, u'charger_phases': 1, u'usable_battery_level': 74, u'battery_heater_on': False, u'scheduled_charging_pending': False, u'battery_range': 230.3, u'charger_power': 10, u'charge_limit_soc': 75, u'max_range_charge_counter': 0, u'trip_charging': False, u'charger_actual_current': 40, u'charge_enable_request': True, u'fast_charger_brand': u'<invalid>', u'fast_charger_type': u'ACSingleWireCAN', u'charging_state': u'Charging', u'charge_limit_soc_std': 90, u'managed_charging_start_time': None, u'battery_level': 74, u'charge_energy_added': 9.76, u'charge_port_door_open': True, u'charger_pilot_current': 40, u'timestamp': 1546588304144, u'charge_limit_soc_max': 100, u'ideal_battery_range': 230.3, u'managed_charging_active': False, u'conn_charge_cable': u'SAE', u'not_enough_power_to_heat': None, u'fast_charger_present': False, u'charge_port_latch': u'Engaged', u'managed_charging_user_canceled': False, u'time_to_full_charge': 0.08, u'est_battery_range': 175.17, u'charge_rate': 36.4, u'charger_voltage': 239, u'charge_current_request_max': 40, u'charge_miles_added_ideal': 40.0, u'charge_limit_soc_min': 50, u'charge_miles_added_rated': 40.0}
# drive_state = {u'native_longitude': -122.12837, u'power': -9, u'timestamp': 1546588304411, u'shift_state': None, u'longitude': -122.12837, u'native_location_supported': 1, u'latitude': 47.566833, u'native_type': u'wgs', u'gps_as_of': 1546588303, u'native_latitude': 47.566833, u'speed': None, u'heading': 171}
def collect_data(ge):
    try:
        print("collect_data_loop: time = " + str(time.ctime()))
        c = teslajson.Connection(tesla_info = tesla_info, access_token = access_token)
        print("collect_data_loop: CONNECTED: time = " + str(time.ctime()))
        v = c.vehicles[0]
        #print("collect_data_loop: vehicle = " + str(v))
        #print("collect_data_loop: id = " + str(v['id']))
        #print("collect_data_loop: vehicle_id = " + str(v['vehicle_id']))
        #print("collect_data_loop: VIN = " + str(v['vin']))
        print("collect_data_loop: display_name = " + str(v['display_name']))
        print("collect_data_loop: state = " + str(v['state']))
        #
        # v['state'] = 'online'|'offline'|'asleep'
        #
        if v['state'] == 'online':
# charge_state['charging_state'] = 'Disconnected'|'Starting'|'Charging'|'Complete'
# drive_state['shift_state'] = None|'P'|'D'|'R'
# drive_state['speed'] = None|<speed>
            print("collect_data_loop: ONLINE: time = " + str(time.ctime()))
            print("collect_data_loop: ONLINE: VIN = " + str(v['vin']))
            print("collect_data_loop: ONLINE: display_name = " + str(v['display_name']))
            try:
                vehicle_data = v.data();
                ###
                ### print("collect_data_loop: vehicle_data = " + str(vehicle_data));
                ###
            except Exception as e:
                print("collect_data_loop: EXCEPTION -> STATE_ERROR (cannot get vehichle data): " + str(e))
                return STATE_ERROR

            charge_state = vehicle_data['charge_state']
            print("collect_data_loop: charge_state = " + str(charge_state))
            drive_state = vehicle_data['drive_state']
            print("collect_data_loop: drive_state = " + str(drive_state))
            vehicle_state = vehicle_data['vehicle_state']
            print("collect_data_loop: vehicle_state = " + str(vehicle_state))
            print("collect_data_loop: vehicle_state[odometer] = " + str(vehicle_state['odometer']))
            print("collect_data_loop: charge_state[charging_state] = " + charge_state['charging_state'])
            print("collect_data_loop: drive_state[shift_state] = " + str(drive_state['shift_state']))
            print("collect_data_loop: drive_state[speed] = " + str(drive_state['speed']))
            print("collect_data_loop: drive_state[latitude] = " + str(drive_state['latitude']))
            print("collect_data_loop: drive_state[longitude] = " + str(drive_state['longitude']))
            # augment drive_state with altitude using altitute service
            drive_state['altitude'] = ge.get(drive_state['latitude'], drive_state['longitude'], True)
            print("collect_data_loop: drive_state[altitude] = " + str(drive_state['altitude']))
            print("collect_data_loop: done time = " + str(time.ctime()))
            if (drive_state['shift_state'] is None) or (drive_state['speed'] is None):
                #
                # not driving
                #
                if (charge_state['charging_state'] == 'Starting') or (charge_state['charging_state'] == 'Charging'):
                    print("collect_data_loop: " + str(v['state']) + " -> STATE_CHARGING")
                    return STATE_CHARGING
                if charge_state['charging_state'] == 'Complete':
                    print("collect_data_loop: " + str(v['state']) + " -> STATE_CHARGING_COMPLETE")
                    return STATE_CHARGING_COMPLETE
                #
                # Disconnected -- not charging / charging not complete
                #
                print("collect_data_loop: " + str(v['state']) + " -> STATE_NOT_CHARGING")
                return STATE_NOT_CHARGING
            else:
                #
                # driving
                #
                print("collect_data_loop: " + str(v['state']) + " -> STATE_DRIVING")
                return STATE_DRIVING
        else:
            print("collect_data_loop: done time = " + str(time.ctime()))
            print("collect_data_loop: " + str(v['state']) + " -> STATE_NOT_ONLINE")
            return STATE_NOT_ONLINE
    except Exception as e:
        print("collect_data_loop: EXCEPTION -> STATE_ERROR: " + str(e))
        return STATE_ERROR

def main_loop():
    ge = get_elevation.Elevation()
    while True:
        r = collect_data(ge)
        sys.stdout.flush()
        if r == STATE_CHARGING:
            time.sleep(SLEEP_STATE_CHARGING)
        elif r == STATE_CHARGING_COMPLETE:
            time.sleep(SLEEP_STATE_CHARGING_COMPLETE)
        elif r == STATE_NOT_CHARGING:
            time.sleep(SLEEP_STATE_NOT_CHARGING)
        elif r == STATE_DRIVING:
            time.sleep(SLEEP_STATE_DRIVING)
        elif r == STATE_NOT_ONLINE:
            time.sleep(SLEEP_STATE_NOT_ONLINE)
        elif r == STATE_ERROR:
            time.sleep(SLEEP_STATE_ERROR)
        else:
            #
            # UNKNOWN or ERROR
            #
            time.sleep(SLEEP_STATE_UNKNOWN)

main_loop()
