#!/usr/bin/python3

import teslajson
import get_elevation
import os
import sys
import time
import daemon
import lockfile.pidlockfile
import json

last_logfile = ""

tesla_info = {
    "id":"e4a9949fcfa04068f59abb5a658f2bac0a3428e4652315490b659d5ab3f35a9e",
    "secret":"c75f14bbadc8bee3a7594412c31416f8300256d7668ea7e6e7f06727bfb9d220",
    "baseurl": "https://owner-api.teslamotors.com",
    "api": "/api/1/"
}

access_token="828a2d716ba26d04c6605bb9e5f628a9ffb147f0cf3848f16f3aa94a28771a8f"

#token_info = {
#    "access_token":"828a2d716ba26d04c6605bb9e5f628a9ffb147f0cf3848f16f3aa94a28771a8f",
#    "token_type":"bearer",
#    "expires_in":3888000,
#    "refresh_token":"4fb4903a2eb1fb8894b6bb7e211b7f8b2fa550d7c3341237bf2dc566fbd8ef49",
#    "created_at":1554098431
#}
token_info = { }

STATE_ERROR = -1
STATE_UNKNOWN = 0
STATE_OFFLINE = 1
STATE_ASLEEP = 2
STATE_CHARGING = 3
STATE_CHARGING_COMPLETE = 4
STATE_NOT_CHARGING = 5
STATE_USER_PRESENT_NOT_DRIVING = 6
STATE_USER_NOT_PRESENT_NOT_LOCKED = 7
STATE_DRIVING = 8
STATE_WAIT_ASLEEP = 9

state_names = {
    STATE_ERROR : "STATE_ERROR",
    STATE_UNKNOWN : "STATE_UNKNOWN",
    STATE_OFFLINE : "STATE_OFFLINE",
    STATE_ASLEEP : "STATE_ASLEEP",
    STATE_CHARGING : "STATE_CHARGING",
    STATE_CHARGING_COMPLETE : "STATE_CHARGING_COMPLETE",
    STATE_NOT_CHARGING : "STATE_NOT_CHARGING",
    STATE_USER_PRESENT_NOT_DRIVING : "STATE_USER_PRESENT_NOT_DRIVING",
    STATE_USER_NOT_PRESENT_NOT_LOCKED : "STATE_USER_NOT_PRESENT_NOT_LOCKED",
    STATE_DRIVING : "STATE_DRIVING",
    STATE_WAIT_ASLEEP : "STATE_WAIT_ASLEEP"
}

#SLEEP_STATE_DRIVING = 15
#SLEEP_STATE_NOT_DRIVING = 15
SLEEP_STATE_DRIVING = 30
SLEEP_STATE_NOT_DRIVING = 30

#
# wait this much time to let the car go from online to 'offline' or 'asleep'
#
#WAIT_TO_GO_ASLEEP = (60 * 20)
WAIT_TO_GO_ASLEEP = (60 * 20)
#WAIT_TO_GO_ASLEEP = (60 * 5)

#
# timeout to let sleep. sometimes the car does not go 'offline' or 'asleep', if tasks are scheduled or other reasons.
#
LET_SLEEP_TIMEOUT = (60 * 15)
#LET_SLEEP_TIMEOUT = (60 * 10)
#LET_SLEEP_TIMEOUT = (60 * 3)

# charge_state['charging_state'] = 'NoPower'|'Disconnected'|'Starting'|'Charging'|'Complete'
# drive_state['shift_state'] = None|'P'|'D'|'R'
# drive_state['speed'] = None|<speed>

# charge_state = {u'user_charge_enable_request': None, u'scheduled_charging_start_time': None, u'charge_current_request': 40, u'charge_to_max_range': False, u'charger_phases': 1, u'usable_battery_level': 74, u'battery_heater_on': False, u'scheduled_charging_pending': False, u'battery_range': 230.3, u'charger_power': 10, u'charge_limit_soc': 75, u'max_range_charge_counter': 0, u'trip_charging': False, u'charger_actual_current': 40, u'charge_enable_request': True, u'fast_charger_brand': u'<invalid>', u'fast_charger_type': u'ACSingleWireCAN', u'charging_state': u'Charging', u'charge_limit_soc_std': 90, u'managed_charging_start_time': None, u'battery_level': 74, u'charge_energy_added': 9.76, u'charge_port_door_open': True, u'charger_pilot_current': 40, u'timestamp': 1546588304144, u'charge_limit_soc_max': 100, u'ideal_battery_range': 230.3, u'managed_charging_active': False, u'conn_charge_cable': u'SAE', u'not_enough_power_to_heat': None, u'fast_charger_present': False, u'charge_port_latch': u'Engaged', u'managed_charging_user_canceled': False, u'time_to_full_charge': 0.08, u'est_battery_range': 175.17, u'charge_rate': 36.4, u'charger_voltage': 239, u'charge_current_request_max': 40, u'charge_miles_added_ideal': 40.0, u'charge_limit_soc_min': 50, u'charge_miles_added_rated': 40.0}

# collect_data_loop: vehicle_state = {u'remote_start_supported': True, u'homelink_nearby': True, u'parsed_calendar_supported': True, u'odometer': 2655.062064, u'remote_start': False, u'pr': 0, u'valet_mode': False, u'calendar_supported': True, u'speed_limit_mode': {u'active': False, u'current_limit_mph': 50.0, u'max_limit_mph': 90, u'min_limit_mph': 50, u'pin_code_set': True}, u'pf': 0, u'sun_roof_percent_open': None, u'media_state': {u'remote_control_enabled': False}, u'api_version': 6, u'rt': 0, u'ft': 0, u'df': 1, u'timestamp': 1546889059258, u'sun_roof_state': u'unknown', u'notifications_supported': True, u'software_update': {u'expected_duration_sec': 2700, u'status': u''}, u'is_user_present': True, u'vehicle_name': u'HAL9001', u'dr': 0, u'autopark_style': u'dead_man', u'locked': False, u'center_display_state': 2, u'last_autopark_error': u'no_error', u'car_version': u'2018.50 7e49f8a', u'autopark_state_v3': u'disabled'}

# drive_state = {u'native_longitude': -122.12837, u'power': -9, u'timestamp': 1546588304411, u'shift_state': None, u'longitude': -122.12837, u'native_location_supported': 1, u'latitude': 47.566833, u'native_type': u'wgs', u'gps_as_of': 1546588303, u'native_latitude': 47.566833, u'speed': None, u'heading': 171}

# climate_state = {'seat_heater_left': 0, 'passenger_temp_setting': 20.0, 'timestamp': 1555222736156, 'driver_temp_setting': 20.0, 'battery_heater': False, 'max_avail_temp': 28.0, 'is_front_defroster_on': False, 'battery_heater_no_power': None, 'is_preconditioning': False, 'wiper_blade_heater': False, 'seat_heater_rear_left': 0, 'inside_temp': 15.4, 'is_climate_on': False, 'side_mirror_heaters': False, 'is_auto_conditioning_on': False, 'min_avail_temp': 15.0, 'is_rear_defroster_on': False, 'right_temp_direction': 0, 'outside_temp': 15.5, 'remote_heater_control_enabled': False, 'seat_heater_rear_center': 0, 'fan_status': 0, 'smart_preconditioning': False, 'climate_keeper_mode': 'off', 'seat_heater_rear_right': 0, 'left_temp_direction': 0, 'seat_heater_right': 0}

def print_state(r, v, charge_state, drive_state, vehicle_state, climate_state):
    s = "PARSE ";
    s += '\t';
    s += str(int(time.time()));
    s += '\t';
    s += state_names[r];
    s += '\t';
    s += str(v);
    s += '\t';
    s += str(charge_state);
    s += '\t';
    s += str(drive_state);
    s += '\t';
    s += str(vehicle_state);
    s += '\t';
    s += str(climate_state);
    print(s);

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
    charge_state = { }
    drive_state = { }
    vehicle_state = { }
    climate_state = { }

    #
    # try get charge_state
    #
    try:
        charge_state = v.data_request('charge_state')
        print("collect_state: charge_state = " + str(charge_state))
        has_charge_state = True
    except Exception as e:
        print("collect_state: EXCEPTION (cannot get charge_state): " + str(e))
        has_charge_state = False

    #
    # try get drive_state
    #
    try:
        drive_state = v.data_request('drive_state')
        print("collect_state: drive_state = " + str(drive_state))
        has_drive_state = True
    except Exception as e:
        print("collect_state: EXCEPTION (cannot get drive_state): " + str(e))
        has_drive_state = False

    #
    # try get vehicle_state
    #
    try:
        vehicle_state = v.data_request('vehicle_state')
        print("collect_state: vehicle_state = " + str(vehicle_state))
        has_vehicle_state = True
    except Exception as e:
        print("collect_state: EXCEPTION (cannot get vehicle_state): " + str(e))
        has_vehicle_state = False

    #
    # try get climate_state
    #
    try:
        climate_state = v.data_request('climate_state')
        print("collect_state: climate_state = " + str(climate_state))
        has_climate_state = True
    except Exception as e:
        print("collect_state: EXCEPTION (cannot get climate_state): " + str(e))
        has_climate_state = False

    if not has_charge_state and not has_drive_state and not has_vehicle_state:
        print("collect_state: cannot retrieve charge_state,drive_state,vehicle_state")
        print_state(STATE_ERROR, v, charge_state, drive_state, vehicle_state, climate_state)
        return STATE_ERROR

    if not has_drive_state:
        print_state(STATE_ERROR, v, charge_state, drive_state, vehicle_state, climate_state)
        print("collect_state: drive_state is needed")
        return STATE_ERROR

    if has_vehicle_state:
        print("collect_state: vehicle_state[odometer] = " + str(vehicle_state['odometer']))
        print("collect_state: vehicle_state[is_user_present] = " + str(vehicle_state['is_user_present']))
        print("collect_state: vehicle_state[locked] = " + str(vehicle_state['locked']))

    if has_charge_state:
        print("collect_state: charge_state[charging_state] = " + str(charge_state['charging_state']))

    #
    # add altitude to drive state
    #
    drive_state['altitude'] = ge.get(drive_state['latitude'], drive_state['longitude'], True)

    print("collect_state: drive_state[shift_state] = " + str(drive_state['shift_state']))
    print("collect_state: drive_state[speed] = " + str(drive_state['speed']))
    print("collect_state: drive_state[latitude] = " + str(drive_state['latitude']))
    print("collect_state: drive_state[longitude] = " + str(drive_state['longitude']))
    print("collect_state: drive_state[altitude] = " + str(drive_state['altitude']))

    #data = v.data();
    #print("collect_state: all_vehicle_data = " + str(data));
    if (drive_state['shift_state'] is None) or (drive_state['speed'] is None):
        #
        # can only find out about this if has_vehicle_state == True
        #
        if has_vehicle_state:
            if vehicle_state['is_user_present']:
                print("collect_state: " + str(v['state']) + " -> STATE_USER_PRESENT_NOT_DRIVING")
                print_state(STATE_USER_PRESENT_NOT_DRIVING, v, charge_state, drive_state, vehicle_state, climate_state)
                return STATE_USER_PRESENT_NOT_DRIVING
            if vehicle_state['locked'] == False:
                print("collect_state: " + str(v['state']) + " -> STATE_USER_NOT_PRESENT_NOT_LOCKED")
                print_state(STATE_USER_NOT_PRESENT_NOT_LOCKED, v, charge_state, drive_state, vehicle_state, climate_state)
                return STATE_USER_NOT_PRESENT_NOT_LOCKED

        #
        # can only find out about this if has_charge_state == True
        #
        if has_charge_state:
            if (charge_state['charging_state'] == 'Starting') or (charge_state['charging_state'] == 'Charging'):
                print("collect_state: " + str(v['state']) + " -> STATE_CHARGING")
                print_state(STATE_CHARGING, v, charge_state, drive_state, vehicle_state, climate_state)
                return STATE_CHARGING
            if charge_state['charging_state'] == 'Complete':
                print("collect_state: " + str(v['state']) + " -> STATE_CHARGING_COMPLETE")
                print_state(STATE_CHARGING_COMPLETE, v, charge_state, drive_state, vehicle_state, climate_state)
                return STATE_CHARGING_COMPLETE

        #
        # unknown / not charging / charging not complete
        #
        print("collect_state: " + str(v['state']) + " -> STATE_NOT_CHARGING")
        print_state(STATE_NOT_CHARGING, v, charge_state, drive_state, vehicle_state, climate_state)
        return STATE_NOT_CHARGING
    else:
        #
        # driving
        #
        print("collect_state: " + str(v['state']) + " -> STATE_DRIVING")
        print_state(STATE_DRIVING, v, charge_state, drive_state, vehicle_state, climate_state)
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
            print("collect_data: " + str(v['state']) + " (-> STATE_ONLINE)")
            if let_sleep == True:
                print("collect_data: letting car go asleep")
                print("collect_data: " + str(v['state']) + " -> STATE_NOT_CHARGING")
                print_state(STATE_NOT_CHARGING, v, {}, {}, {}, {})
                return STATE_NOT_CHARGING
            return collect_state(ge, c, v)
        elif v['state'] == 'offline':
            #
            # offline
            #
            print_state(STATE_OFFLINE, v, {}, {}, {}, {})
            print("collect_data: " + str(v['state']) + " -> STATE_OFFLINE")
            return STATE_OFFLINE
        else:
            #
            # asleep
            #
            print_state(STATE_ASLEEP, v, {}, {}, {}, {})
            print("collect_data: " + str(v['state']) + " -> STATE_ASLEEP")
            return STATE_ASLEEP
    except Exception as e:
        print("collect_data: EXCEPTION -> STATE_ERROR: " + str(e))
        return STATE_ERROR

def log_redirect():
    sys.stderr.flush()
    sys.stdout.flush()
    t = time.gmtime()
    logfile = time.strftime("tesla_collector-%04Y-%02m-%02d.log", t)
    if logfile != last_logfile:
        sys.stdout = open(logfile, "a")
        sys.stderr = sys.stdout
        os.chmod(logfile, 0o644)

def main_loop():
    #
    ge = get_elevation.Elevation()
    not_charging_last_time_timer = 0
    let_sleep = False
    iteration = 0
    r = STATE_UNKNOWN
    while True:
        #
        log_redirect()
        #
        print("main_loop(): =======================================================================")
        iteration += 1
        if r == STATE_WAIT_ASLEEP:
            print_state(r, {}, {}, {}, {}, {})
            print("main_loop(): wait_asleep: not collecting state")
        else:
            r = collect_data(ge, let_sleep)
        print("main_loop(): iteration = " + str(iteration) + ", let_sleep = " + str(let_sleep) + ", time = " + str(time.ctime()) + ", r = " + str(r) + ": " + state_names[r])
        if r == STATE_CHARGING:
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        elif (r == STATE_CHARGING_COMPLETE) or (r == STATE_NOT_CHARGING) or (r == STATE_WAIT_ASLEEP):
            print("main_loop(): " + state_names[r])
            #
            # see if we need to let the vehicle go asleep/offline
            #
            if not_charging_last_time_timer == 0:
                not_charging_last_time_timer = int(time.time())
                print("main_loop: setting not_charging_last_time_timer: " + str(not_charging_last_time_timer))
            timer_elapsed = int(time.time()) - not_charging_last_time_timer
            print("main_loop: timer_elapsed = " + str(timer_elapsed) + ", WAIT_TO_GO_ASLEEP = " + str(WAIT_TO_GO_ASLEEP) + ", LET_SLEEP_TIMEOUT = " + str(LET_SLEEP_TIMEOUT))
            if timer_elapsed >= WAIT_TO_GO_ASLEEP:
                print("main_loop: timer_elapsed exceeded delay " + str(WAIT_TO_GO_ASLEEP) + ", letting car to go asleep")
                let_sleep = True
                r = STATE_WAIT_ASLEEP
            else:
                let_sleep = False
            #
            # if vehicle doesn't go asleep/offline, stop waiting.
            #
            if timer_elapsed >= WAIT_TO_GO_ASLEEP + LET_SLEEP_TIMEOUT:
                print("main_loop: timer_elapsed exceeded delay+timeout " + str(WAIT_TO_GO_ASLEEP) + "+" + str(LET_SLEEP_TIMEOUT) + ", cancelling let_sleep")
                not_charging_last_time_timer = 0
                r = STATE_UNKNOWN
                let_sleep = False
        elif (r == STATE_DRIVING) or (r == STATE_USER_PRESENT_NOT_DRIVING):
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        elif r == STATE_USER_NOT_PRESENT_NOT_LOCKED:
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        elif r == STATE_ASLEEP:
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        elif r == STATE_OFFLINE:
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        else:
            print("main_loop(): " + state_names[r])
            not_charging_last_time_timer = 0
            let_sleep = False
        sys.stderr.flush()
        sys.stdout.flush()
        if (r == STATE_DRIVING) or (r == STATE_USER_PRESENT_NOT_DRIVING):
            time.sleep(SLEEP_STATE_DRIVING)
        else:
            time.sleep(SLEEP_STATE_NOT_DRIVING)
        print("main_loop: done loop iteration " + str(iteration) + ", time = " + str(time.ctime()))

def load_token_info():
        fd = open("access_token.json", "r")
        s = fd.read()
        token_info = json.loads(s)
        fd.close()
        print("token_info = " + str(token_info))

if __name__ == "__main__":
        load_token_info()
        # doesn't work reliably
        # pidfile = lockfile.pidlockfile.PIDLockFile("/run/lock/tesla_collector")
        pidfile = None
        with daemon.DaemonContext(working_directory = "/tesla/logs", detach_process = True, stdin = None, pidfile = pidfile):
            log_redirect()
            print("__main__(): daemonized, entering main loop")
            main_loop()
