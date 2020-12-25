# Tesla Scripts

Only scripts/ should be looked at. The rest of the code is in development.

# How to use

* use ./teslatoken.py to generate an access token and other information in tesla_info.json
* use ./tesla_command.py to make simply queries

* teslatoken.py takes the user email and password as arguments and gets the access token, so that tesla_command.py can run without having to supply a password. teslatoken.py does not save the passwd, but it's recommended to clear your shell history. example:
```
[fio@linux-oel77 scripts]$ ./teslatokenapi.py foobar@gmail.com 12345
Writing User email, Token and API info to ./access_info.json
```

* ./tesla_command.py vehicles: (show all vehicles)
```
[fcattane@linux-oel77 scripts]$ ./tesla_command.py vehicles
....
....
                        "display_name": "HAL9000",
                        "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0",
                        "color": null,
                        "access_type": "OWNER",
                        "state": "online",
                        "in_service": false,
....
....
```
* the option codes will tell you everything about your car, from your tire configuration, to installed features.
* in the above example, my Model 3 is called HAL9000. the option code is displayed incorrectly however, probably because the car was upgraded later and they didn't update the option codes -- i need to ask customer support
         * Hardware 2.5 option code is APH3
         * Hardware 3 option code is APH4
* option codes are listed here: https://tesla-api.timdorr.com/vehicle/optioncodes

* ./tesla_command.py vehicle: (shows first vehicle)

* ./tesla_command.py wakeup: (wakeup vehicle)

* ./tesla_command.py data: (show vehicle data)
	* note that this command will fail if the vehicle is asleep. in this case do a wakeup before
