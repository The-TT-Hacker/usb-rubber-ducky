import numpy as np
from PIL import ImageGrab
import cv2

def get_screenshot():    
    printscreen_pil   = ImageGrab.grab()
    printscreen_numpy = np.array(printscreen_pil.getdata(),dtype='uint8')\
    .reshape((printscreen_pil.size[1],printscreen_pil.size[0],3)) 
        
    cv2.imwrite("screenshot.png", printscreen_numpy)
        
    success = True
    
    return success

def screen_stealer(pipe):
    while True:
        while pipe.poll():
            command = pipe.recv()
            if command == "get_frame":
                success = get_screenshot()
                
                if success:
                    print("Got frame")
                    pipe.send("success")
                else:
                    pipe.send("fail")
                    
