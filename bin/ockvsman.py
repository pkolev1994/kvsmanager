#!/usr/bin/env /usr/bin/python3.4
import sys
import os
import signal

option = sys.argv[1]
if len(sys.argv) > 2:
	print("====================================================")
	print("Usage of kvs_manager : ")
	print("kvs_manager start/stop/status")
	print("====================================================")


def main():

	if option == "start":
		print("Starting kvs_manager ...")
		os.chdir("/aux0/customer/containers/ockvsman/bin/")
		os.system("/usr/bin/python3.4 kvs_wrapper.py >/dev/null &")
	elif option == "stop":
		pstring = "kvs_wrapper.py"
		for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
			fields = line.split()
			pid = fields[0]
		print("Stopping kvs_wrapper ...")
		os.kill(int(pid), signal.SIGKILL)
	elif option == 'status':
		pstring = "kvs_wrapper.py"
		pid = None
		for line in os.popen("ps ax | grep " + pstring + " | grep -v grep"):
			fields = line.split()
			pid = fields[0]
		if not pid:
			print("kvs_wrapper is not running: NO PID")
			return
		else:
			print("kvs_wrapper is running: {}".format(pid))	
	else:
		print("====================================================")
		print("Usage of kvs_wrapper : ")
		print("kvs_manager start/stop/status")
		print("====================================================")

main()