print("\n") # separate logs from default messages of editor

from machine import Pin, PWM
import time
from json import dumps, loads
import socket

from utils.create_web_page import create_web_page
from utils.connect_to_wifi import connect_to_wifi

MAX_DUTY_CYCLE = 65535

# Set up the LED pin with PWM
ceiling = PWM(Pin(26))
shop = PWM(Pin(33))

# Set the PWM frequency
ceiling.freq(1000)
shop.freq(1000)
# first turn off leds
ceiling.duty_u16(0)
shop.duty_u16(0)

def web_server():

    station = connect_to_wifi()


    # create web socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((station.ifconfig()[0], 80))
    s.listen(5) # max 5 socket connections // max possible should be 16


    # blink leds to signal its ready
    for _ in range(3):
        ceiling.duty_u16(MAX_DUTY_CYCLE)
        shop.duty_u16(MAX_DUTY_CYCLE)
        time.sleep(0.5)

        ceiling.duty_u16(0)
        shop.duty_u16(0)
        time.sleep(0.5)


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
                ceiling.duty_u16(
                    abs(ceiling.duty_u16() - MAX_DUTY_CYCLE) if ceiling.duty_u16() in [0, MAX_DUTY_CYCLE] else 0
                )
            if data.get("shop", False):
                shop.duty_u16(
                    abs(shop.duty_u16() - MAX_DUTY_CYCLE) if shop.duty_u16() in [0, MAX_DUTY_CYCLE] else 0
                )
            
            if data.get("ceiling-brightness", False):
                ceiling.duty_u16(MAX_DUTY_CYCLE // 100 * data["ceiling-brightness"])
            if data.get("shop-brightness", False):
                shop.duty_u16(MAX_DUTY_CYCLE // 100 * data["shop-brightness"])
            
            response = "hello"

        else:
            response = create_web_page()

        
        # Create a socket reply and close
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()


if __name__ == "__main__":    
    web_server()







