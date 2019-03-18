#!/usr/bin/python3.4

import os
import re
import socket
import sys
#custom libs
sys.path.append('/aux0/customer/containers/ockvsman/')
from lib.http_server_simple import Http_server_simple
sys.path.append('/aux0/customer/containers/ocpytools/lib/')
from etcd_client import EtcdManagement

class kvsManager(Http_server_simple):


	def __init__(self):

		super().__init__()
		"""
		Constructor
		Inheritate Http_server_simple constructor
		"""
		self.etcdman = EtcdManagement()



	def getRequest(self):
		super().getRequest()



	def get_config_statuses(self):
		"""
		Takes all config statuses for the 
		specific hostname
		Each kvsManager will get statuses
		for his hostname
		Args:
			None
		Returns:
			self.etcdman.get_config_statuses(self.hostname)(dict)
		"""
		
		return self.etcdman.get_config_statuses(self.hostname)