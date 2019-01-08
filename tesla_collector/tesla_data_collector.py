#!/usr/bin/python

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
STATE_USER_PRESENT_NOT_DRIVING = 5
STATE_USER_NOT_PRESENT_NOT_LOCKED = 6
STATE_DRIVING = 7

SLEEP_STATE_DRIVING = 15
#SLEEP_STATE_NOT_DRIVING = 30
SLEEP_STATE_NOT_DRIVING = 15

# sleep this much time to let the car go from online to 'offline' or 'asleep'
WAIT_TO_GO_ASLEEP = (60 * 10)

# charge_state['charging_state'] = 'Disconnected'|'Starting'|'Charging'|'Complete'
# drive_state['shift_state'] = None|'P'|'D'|'R'
# drive_state['speed'] = None|<speed>

# charge_state = {u'user_charge_enable_request': None, u'scheduled_charging_start_time': None, u'charge_current_request': 40, u'charge_to_max_range': False, u'charger_phases': 1, u'usable_battery_level': 74, u'battery_heater_on': False, u'scheduled_charging_pending': False, u'battery_range': 230.3, u'charger_power': 10, u'charge_limit_soc': 75, u'max_range_charge_counter': 0, u'trip_charging': False, u'charger_actual_current': 40, u'charge_enable_request': True, u'fast_charger_brand': u'<invalid>', u'fast_charger_type': u'ACSingleWireCAN', u'charging_state': u'Charging', u'charge_limit_soc_std': 90, u'managed_charging_start_time': None, u'battery_level': 74, u'charge_energy_added': 9.76, u'charge_port_door_open': True, u'charger_pilot_current': 40, u'timestamp': 1546588304144, u'charge_limit_soc_max': 100, u'ideal_battery_range': 230.3, u'managed_charging_active': False, u'conn_charge_cable': u'SAE', u'not_enough_power_to_heat': None, u'fast_charger_present': False, u'charge_port_latch': u'Engaged', u'managed_charging_user_canceled': False, u'time_to_full_charge': 0.08, u'est_battery_range': 175.17, u'charge_rate': 36.4, u'charger_voltage': 239, u'charge_current_request_max': 40, u'charge_miles_added_ideal': 40.0, u'charge_limit_soc_min': 50, u'charge_miles_added_rated': 40.0}

# collect_data_loop: vehicle_state = {u'remote_start_supported': True, u'homelink_nearby': True, u'parsed_calendar_supported': True, u'odometer': 2655.062064, u'remote_start': False, u'pr': 0, u'valet_mode': False, u'calendar_supported': True, u'speed_limit_mode': {u'active': False, u'current_limit_mph': 50.0, u'max_limit_mph': 90, u'min_limit_mph': 50, u'pin_code_set': True}, u'pf': 0, u'sun_roof_percent_open': None, u'media_state': {u'remote_control_enabled': False}, u'api_version': 6, u'rt': 0, u'ft': 0, u'df': 1, u'timestamp': 1546889059258, u'sun_roof_state': u'unknown', u'notifications_supported': True, u'software_update': {u'expected_duration_sec': 2700, u'status': u''}, u'is_user_present': True, u'vehicle_name': u'HAL9001', u'dr': 0, u'autopark_style': u'dead_man', u'locked': False, u'center_display_state': 2, u'last_autopark_error': u'no_error', u'car_version': u'2018.50 7e49f8a', u'autopark_state_v3': u'disabled'}

# drive_state = {u'native_longitude': -122.12837, u'power': -9, u'timestamp': 1546588304411, u'shift_state': None, u'longitude': -122.12837, u'native_location_supported': 1, u'latitude': 47.566833, u'native_type': u'wgs', u'gps_as_of': 1546588303, u'native_latitude': 47.566833, u'speed': None, u'heading': 171}

def collect_state(ge, c, v):
    #
    #
    # charge_state['charging_state'] = 'Disconnected'|'Starting'|'Charging'|'Complete'
    # drive_state['shift_state'] = None|'P'|'D'|'R'
    # drive_state['speed'] = None|<speed>
    #
    #
    print("collect_state: " + str(time.ctime()))
    print("collect_state: state = " + str(v['state']))
    print("collect_state: VIN = " + str(v['vin']))
    print("collect_state: display_name = " + str(v['display_name']))
    try:
        charge_state = v.data_request('charge_state')
        print("collect_state: charge_state = " + str(charge_state))
    except Exception as e:
        print("collect_state: EXCEPTION -> STATE_ERROR (cannot get charge_state -- ignoring and setting charge_state[charging_state] to Unknown): " + str(e))
        charge_state = {
            "charging_state" : "Unknown"
        }
        #return STATE_ERROR

    state_error = False
    try:
        drive_state = v.data_request('drive_state')
        print("collect_state: drive_state = " + str(drive_state))
    except Exception as e:
        print("collect_state: EXCEPTION -> STATE_ERROR (cannot get drive_state): " + str(e))
        state_error = True
    try:
        vehicle_state = v.data_request('vehicle_state')
        print("collect_state: vehicle_state = " + str(vehicle_state))
    except Exception as e:
        print("collect_state: EXCEPTION -> STATE_ERROR (cannot get vehicle_state): " + str(e))
        state_error = True


    #
    # FIXME: collect partial data
    #
    if state_error == True:
        return STATE_ERROR

    print("collect_state: vehicle_state[odometer] = " + str(vehicle_state['odometer']))
    print("collect_state: vehicle_state[is_user_present] = " + str(vehicle_state['is_user_present']))
    print("collect_state: vehicle_state[locked] = " + str(vehicle_state['locked']))
    print("collect_state: charge_state[charging_state] = " + str(charge_state['charging_state']))
    print("collect_state: drive_state[shift_state] = " + str(drive_state['shift_state']))
    print("collect_state: drive_state[speed] = " + str(drive_state['speed']))
    print("collect_state: drive_state[latitude] = " + str(drive_state['latitude']))
    print("collect_state: drive_state[longitude] = " + str(drive_state['longitude']))
    drive_state['altitude'] = ge.get(drive_state['latitude'], drive_state['longitude'], True)
    print("collect_state: drive_state[altitude] = " + str(drive_state['altitude']))
    print("collect_state: done, time = " + str(time.ctime()))
    #data = v.data();
    #print("collect_state: all_vehicle_data = " + str(data));
    if (drive_state['shift_state'] is None) or (drive_state['speed'] is None):
        if vehicle_state['is_user_present']:
            print("collect_state: " + str(v['state']) + " -> STATE_USER_PRESENT_NOT_DRIVING")
            return STATE_USER_PRESENT_NOT_DRIVING
        if vehicle_state['locked'] == False:
            print("collect_state: " + str(v['state']) + " -> STATE_USER_NOT_PRESENT_NOT_LOCKED")
            return STATE_USER_NOT_PRESENT_NOT_LOCKED
        #
        # not driving
        #
        if (charge_state['charging_state'] == 'Starting') or (charge_state['charging_state'] == 'Charging'):
            print("collect_state: " + str(v['state']) + " -> STATE_CHARGING")
            return STATE_CHARGING
        if charge_state['charging_state'] == 'Complete':
            print("collect_state: " + str(v['state']) + " -> STATE_CHARGING_COMPLETE")
            return STATE_CHARGING_COMPLETE
        #
        # unknown / not charging / charging not complete
        #
        print("collect_state: " + str(v['state']) + " -> STATE_NOT_CHARGING")
        return STATE_NOT_CHARGING
    else:
        #
        # driving
        #
        print("collect_state: " + str(v['state']) + " -> STATE_DRIVING")
        return STATE_DRIVING

def collect_data(ge, let_sleep):
    try:
        print("collect_data: connecting, time = " + str(time.ctime()))
        c = teslajson.Connection(tesla_info = tesla_info, access_token = access_token)
        print("collect_data: connected, time = " + str(time.ctime()))
        v = c.vehicles[0]
        print("collect_data: vehicle = " + str(v))
        #print("collect_data: id = " + str(v['id']))
        #print("collect_data: vehicle_id = " + str(v['vehicle_id']))
        print("collect_data: display_name = " + str(v['display_name']))
        print("collect_data: vin = " + str(v['vin']))
        print("collect_data: state = " + str(v['state']))
        #
        # v['state'] = 'online'|'offline'|'asleep'
        #
        if v['state'] == 'online':
            #
            # online
            #
            if let_sleep == True:
                print("collect_data: letting car go asleep, time = " + str(time.ctime()))
                print("collect_data: " + str(v['state']) + " -> STATE_NOT_CHARGING")
                return STATE_NOT_CHARGING
            return collect_state(ge, c, v)
        #
        #elif v['state'] == 'offline':
        #    #
        #    # offline
        #    #
        #    r = collect_state(ge, c, v)
        #    print("collect_data: done, r = " + str(r) + ", time = " + str(time.ctime()))
        #    if r == STATE_ERROR:
        #        print("collect_data: " + str(v['state']) + " (probably WAKING_UP) -> STATE_NOT_ONLINE")
        #        return STATE_NOT_ONLINE
        #    else:
        #        print("collect_data: " + str(v['state']) + " -> r = " + str(r))
        #        return r
        else:
            #
            # asleep
            #
            print("collect_data: done, time = " + str(time.ctime()))
            print("collect_data: " + str(v['state']) + " -> STATE_NOT_ONLINE")
            return STATE_NOT_ONLINE
    except Exception as e:
        print("collect_data: EXCEPTION -> STATE_ERROR: " + str(e))
        return STATE_ERROR

def main_loop():
    # don't buffer stdout
    sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
    #
    ge = get_elevation.Elevation()
    not_charging_last_time_timer = 0
    let_sleep = False
    iteration = 0
    while True:
        print("main_loop(): =======================================================================")
        iteration += 1
        print("main_loop(): iteration = " + str(iteration) + ", let_sleep = " + str(let_sleep) + ", time = " + str(time.ctime()))
        r = collect_data(ge, let_sleep)
        print("main_loop(): iteration = " + str(iteration) + ", let_sleep = " + str(let_sleep) + ", time = " + str(time.ctime()) + ", r = " + str(r))
        if r == STATE_CHARGING:
            print("main_loop(): STATE_CHARGING")
            not_charging_last_time_timer = 0
            let_sleep = False
        elif (r == STATE_CHARGING_COMPLETE) or (r == STATE_NOT_CHARGING):
            print("main_loop(): STATE_CHARGING_COMPLETE/STATE_NOT_CHARGING")
            if not_charging_last_time_timer == 0:
                not_charging_last_time_timer = int(time.time())
                print("main_loop: setting not_charging_last_time_timer: " + str(not_charging_last_time_timer))
            timer_elapsed = int(time.time()) - not_charging_last_time_timer
            print("main_loop: timer_elapsed = " + str(timer_elapsed) + ", WAIT_TO_GO_ASLEEP = " + str(WAIT_TO_GO_ASLEEP))
            if timer_elapsed >= WAIT_TO_GO_ASLEEP:
                print("main_loop: timer_elapsed exceeded delay " + str(WAIT_TO_GO_ASLEEP) + ", letting car to go asleep")
                let_sleep = True
            else:
                let_sleep = False
        elif (r == STATE_DRIVING) or (r == STATE_USER_PRESENT_NOT_DRIVING):
            print("main_loop(): STATE_DRIVING/STATE_USER_PRESENT_NOT_DRIVING")
            not_charging_last_time_timer = 0
            let_sleep = False
        elif r == STATE_USER_NOT_PRESENT_NOT_LOCKED:
            print("main_loop(): STATE_USER_NOT_PRESENT_NOT_LOCKED")
            not_charging_last_time_timer = 0
            let_sleep = False
        elif r == STATE_NOT_ONLINE:
            print("main_loop(): STATE_NOT_ONLINE")
            not_charging_last_time_timer = 0
            let_sleep = False
        else:
            print("main_loop(): STATE_UNKNOWN/STATE_ERROR")
            not_charging_last_time_timer = 0
            let_sleep = False
        if (r == STATE_DRIVING) or (r == STATE_USER_PRESENT_NOT_DRIVING):
            time.sleep(SLEEP_STATE_DRIVING)
        else:
            time.sleep(SLEEP_STATE_NOT_DRIVING)
        print("main_loop: done loop iteration, time = " + str(time.ctime()))

main_loop()
