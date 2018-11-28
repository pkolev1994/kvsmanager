#!/usr/bin/python3.6

from http.server import BaseHTTPRequestHandler,HTTPServer
import urllib
import re
import threading
import time
import datetime
from ast import literal_eval
import json
###custom libs
from lib.etcd_client import EtcdManagement
PORT_NUMBER = 6667





class Http_server_simple(threading.Thread):
# class http_server_simple():


	def __init__(self):
		"""
		Constructor
		Initializing a thread
		"""
		
#        try:
		threading.Thread.__init__(self)
		self.buffer = []
		self.server = HTTPServer(('', PORT_NUMBER), myHandler)
		self.server.timeout = 3
		self.server.request_queue_size = 1000
		self.start()
#        except KeyboardInterrupt:
#            self.server.socket.close()



	def run(self):
		# pass
		while True:
			self.server.handle_request()


	def getRequest(self):


		self.server.handle_request()

		# now = time.time()
		# while_t = time.time()
		# while int(while_t - now) < 3:
		# 	while_t = time.time()
		# 	# try:
		# 	print("Handling requeset")
		# 	self.server.handle_request()
			# except:
			# 	print("Caught in exception timepout")
			# 	return



class myHandler(BaseHTTPRequestHandler):


	def do_HEAD(self):
		self.send_response(200)
		self.send_header("Content-type", "text/html")
		self.end_headers()

	def do_GET(self):
		"""
		Handles get request
		from web
		Args:
			None
		Returns:
			None
		"""
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		print(self.path)
		if "?" in self.path:
			for key,value in dict(urllib.parse.parse_qsl(self.path.split("?")[1], True)).items():
				# print(key + " = " + value)
#		self.wfile.write("Hello World !")
		return

	def handle_web(self):
		"""
		Handles the web post params
		and set them to parsed dict
		Args:
			None
		Returns:
			etcd_kv(dict)
		"""

		etcd_kv = dict()
		if self.rfile:
			length = int(self.headers.get('Content-Length'))
			parsed_dict = json.loads(self.rfile.read(length).decode('utf-8'))
			hostname = parsed_dict['hostname']
			host_values = hostname.split(",")
			clean_hosts = []
			for host in host_values:
				parsed_host = re.sub('\_\d+$', '', host)
				if not parsed_host in clean_hosts:
					clean_hosts.append(parsed_host)
			value = list(set(clean_hosts))[0]
			
			etcd_kv['key1'] = parsed_dict['key1']
			etcd_kv['value1'] = parsed_dict['value1']
			etcd_kv['import_type'] = parsed_dict['import_type']
			etcd_kv['micro_app'] = value
			etcd_kv['hostnames'] = parsed_dict['hostname']
			if parsed_dict['import_type'] == 'connector':
				etcd_kv['key2'] = parsed_dict['key2']
				etcd_kv['value2'] = parsed_dict['value2']

		return etcd_kv


	def generate_ids(self,web_hostnames, etcd_manager):
		"""
		Generates the id for the specific
		hostname and writes it in the 
		etcd
		Args:
			web_hostnames(dict)
			etcd_manager(EtcdObject)
		Returns
			host_ids(dict)
		"""
		host_ids = {}
		if etcd_manager.CheckKeyPerAppType(web_hostnames['micro_app'], web_hostnames['key1']):
			host_ids[web_hostnames['micro_app']] = int(etcd_manager. \
													get_current_id(web_hostnames['micro_app'], \
																	web_hostnames['key1'])) + 1
		else:
			host_ids[web_hostnames['micro_app']] = 1

		return host_ids


	def do_POST(self):
		"""
		Parse the post request 
		and returns response to web
		Args:
			None
		Returns:
			None
		"""
		etcdman = EtcdManagement()
		web_params = self.handle_web()

		generated_id = self.generate_ids(web_params, etcdman)[web_params['micro_app']]
		etcdman.write(new_key="/platform/{}/general/confs/{}". \
					format(web_params['micro_app'], web_params['key1']), \
						value = web_params['value1'])

		if web_params['import_type'] == 'connector':
			etcdman.write(new_key="/platform/{}/general/confs/{}". \
					format(web_params['micro_app'], web_params['key2']), \
							value = web_params['value2'])
		etcdman.write(new_key="/platform/{}/general/ids/{}". \
				format(web_params['micro_app'], web_params['key1']), value=generated_id)

		time.sleep(1)

		status_results = {}
		hostnames = web_params['hostnames'].split(',')
		for i in range(1,5):
			for hostname in hostnames:
				taken_status = etcdman.get_config_statuses(hostname)
				if taken_status:
					returned_status = json.loads(taken_status)
					if int(returned_status['id']) == generated_id:
						status_results[hostname] = returned_status
						hostnames.remove(hostname)
			time.sleep(1)

		if hostnames:
			for hostname in hostnames:
				status_results[hostname] = {"id": generated_id, \
											"timestamp": datetime.datetime.now(), \
											"status": "unknown"}

		if web_params:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write((str(status_results).encode('utf-8')))
		else:
			self.send_response(401)


