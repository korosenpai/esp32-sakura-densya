import _thread

from utils.led import Led
from utils.connect_to_wifi import connect_to_wifi
from utils.web_server import web_server

print("preparing leds...")
shop_led = Led(33)
ceiling_led = Led(26)

# calculate time and sleep on other thread


print("connecting to wifi...")
station = connect_to_wifi()
web_server(station, ceiling_led, shop_led)