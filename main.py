import _thread
from time import sleep

from utils.led import ceiling_led, shop_led
from utils.connect_to_wifi import connect_to_wifi
from utils.web_server import web_server

print("testing leds...")
ceiling_led.set(100)
shop_led.set(100)
sleep(2)
ceiling_led.set(0)
shop_led.set(0)



print("connecting to wifi...")
station = connect_to_wifi()
web_server(station)

