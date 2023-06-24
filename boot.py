import network
from machine import Pin
from utime import sleep
from usocket import socket, AF_INET, SOCK_STREAM

import json
from time import sleep


with open("wifi.json", "r") as wififile:
    WIFI_DATA = json.load(wififile) # (SSID, PASSWORD)

for wifi in WIFI_DATA:
    
    # Connect to Wi-Fi
    station = network.WLAN(network.STA_IF)
    station.active(True)
    try:
        station.connect(wifi, WIFI_DATA[wifi])
        # Wait for the Wi-Fi connection
        while not station.isconnected():
            sleep(0.1)

        break

    except OSError as e:
        # this is only to ignore impossibility to connect to wifi
        if e.args[0] != "Wifi Internal Error":
            raise e
        
        print(f"cannot connect to '{wifi}'")
        

