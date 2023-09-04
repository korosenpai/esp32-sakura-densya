print("\n") # separate logs from default messages of editor

from machine import Pin, PWM
from utime import sleep
from json import dumps, loads
import socket

from utils.create_web_page import create_web_page
from utils.connect_to_wifi import connect_to_wifi


def web_server(station, ceiling_led, shop_led):

    # create web socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((station.ifconfig()[0], 80))
    s.listen(5) # max 5 socket connections // max possible should be 16


    # blink leds to signal its ready
    for _ in range(3):
        ceiling_led.set(100)
        shop_led.set(100)
        sleep(0.5)

        ceiling_led.set(0)
        shop_led.set(0)
        sleep(0.5)


    while True:
        conn, addr = s.accept()
        # print(f"got a connection from '{addr}'")
        

        # recieve data
        response = None
        request = str(conn.recv(1024))

        
        method, path, protocol = request.split(r'\r\n')[0].split()
        headers = dict(x.split(': ') for x in request.split(r'\r\n')[1:-2])
        content_type = headers.get('Content-Type')
        
        
        if content_type == 'application/json':
            data = str(request).split('\\r\\n\\r\\n')[1][:-1] # :-1 to remove apices
            data = loads(data)
            print(data)
            
            if data.get("ceiling", False):
                ceiling_led.toggle()
            if data.get("shop", False):
                shop_led.toggle()
            
            if data.get("ceiling-brightness", False):
                ceiling_led.set(data["ceiling-brightness"])
            if data.get("shop-brightness", False):
                shop_led.set(data["shop-brightness"])

            response = "hello"

        else:
            response = create_web_page()

        
        # Create a socket reply and close
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()

        sleep(0.01)


if __name__ == "__main__":
    from utils.led import Led
    shop_led = Led(33)
    ceiling_led = Led(26)

    station = connect_to_wifi()
    web_server(station, ceiling_led, shop_led)








