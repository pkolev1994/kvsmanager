import re
import time
import json
import sys
import os
# import markdown
import datetime
import subprocess
import secrets
from ast import literal_eval
# from subprocess import STDOUT, check_output
from flask_restful import Resource, reqparse
from flask import jsonify, make_response, Response, request

sys.path.append('/opt/containers/ocpytools/lib/')
from etcd3_client import EtcdManagement
from logger import Logger
from nodesxml import NodesXml
from registry import ServiceRegistry


class Etcd_kvs(Resource):


	def post(self):


		mod_revision = None
		parser = reqparse.RequestParser()

		parser.add_argument('key', required=True)
		parser.add_argument('value', required=True)

		args = parser.parse_args()
		logger = Logger(filename = "kvs_wrapper", \
				logger_name = "Etcd_kvs post", \
				dirname="/aux1/ockvsman/logs/")
		logger.info("Handle params from web.")
		etcd_manager = EtcdManagement()
		try:
			etcd_manager.write(new_key = args['key'], value = args['value'])
			mod_revision = etcd_manager.get_mod_revision(args['key'])
		except:
			logger.info("Request can't be executed, Error code => 1000")
			return {'message': "Request can't be registered", "code": 1000}, 500

		logger.info("Key was registered successfully, mod_revision => {}".format(mod_revision))
		logger.clear_handler()
		return {'message': 'Key was registered successfully', 
				'mod_revision': mod_revision}, 200



class EtcdAddKey(Resource):

	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('key', required=True)
		parser.add_argument('value', required=True)

		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		try:
			etcd_manager.write(new_key = args['key'], value = args['value'])
			mod_revision = etcd_manager.get_mod_revision(args['key'])
			return {'message': 'Key was registered successfully', 
					"mod_revision": mod_revision}, 200

		except:
			return {'message': "Request can't be executed", "code": 1000}, 500




class EtcdAddKeys(Resource):

	def post(self):

		parser = reqparse.RequestParser()
		data = request.get_json()
		etcdman = EtcdManagement()
		resp_list = []
		for dict_obj in data:
			try:
				etcdman.write(new_key=dict_obj["key"], value = dict_obj["value"])
			except:
				resp_list.append({"key": dict_obj["key"], "status": "failed", "code": 1000})
				continue
			resp_list.append({"key": dict_obj["key"], 
								"status": "success", 
								"mod_revision": etcdman.get_mod_revision(dict_obj['key'])})
		return jsonify(resp_list)



class EtcdGetKey(Resource):

	def post(self):

		parser = reqparse.RequestParser()
		parser.add_argument('etcd_key', required=True)
		args = parser.parse_args()

		etcd_manager = EtcdManagement()
		key_data = None
		try:
			key_data = etcd_manager.read_key(args['etcd_key'])
			return {"value": key_data, 
					"mod_revision": etcd_manager.get_mod_revision(args['etcd_key'])}, 200
		except:
			return {'message': "Key can't be get!!", "code": 1001}, 404






class EtcdGetKey2(Resource):

	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('etcd_key', type=str)
		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		key_data = None
		try:
			key_data = etcd_manager.read_key(args['etcd_key'])
			return jsonify({"value": key_data, 
					"mod_revision": etcd_manager.get_mod_revision(args['etcd_key'])})
		except:
			return {'message': "Key can't be get!!", "code": 1001}, 404


class EtcdGetKeysByPrefix(Resource):

	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('prefix', type=str)
		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		key_data = None
		try:
			key_data = etcd_manager.read_key_prefix(args['prefix'])
			return jsonify(key_data)

		except:
			return {'message': "Keys can't be get!!", "code": 1001}, 404


class EtcdGetNodesHostnames(Resource):

	def get(self):

		parser = reqparse.RequestParser()
		parser.add_argument('group', type=str)
		args = parser.parse_args()
		nodes_xml_obj = NodesXml()
		try:
			key_data = nodes_xml_obj.get_group_hostnames(
									nodes_xml_path="/configico123/{/home/ico/nodes.xml}/content", 
									group=args["group"])
			return jsonify(key_data)
		except:
			return {'message': "Group can't be get!", "code": 1001}, 404
			
class EtcdPlatformNodes(Resource):

	def get(self):
		parser = reqparse.RequestParser()
		parser.add_argument('platform', type=str)
		args = parser.parse_args()
		service_obj = ServiceRegistry()
		try:
			return jsonify(service_obj.get_nodes_json(args["platform"]))
		except:
			return {'message': "Key in etcd [{}] doesn't exist or can't be parsed".
						format("/platform/v1/{}/configs/aux0/customer/platform/nodes.xml".
							format(args["platform"])), 
					"code": 1001}, 404


class EtcdDeleteKey(Resource):

	def delete(self):
		parser = reqparse.RequestParser()
		parser.add_argument('key', type=str)
		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		deleted_flag = None
		try:
			deleted_flag = etcd_manager.remove_key(args["key"])
		except:
			return {'message': "Request can't be executed", "code": 1000}, 500

		if deleted_flag:
			return {'message': 'Key was deleted successfully'}, 200
		else:
			return {'message': "Key wasn't deleted successfully", "code": 1002}, 409

class EtcdDeleteKeys(Resource):

	def delete(self):
		parser = reqparse.RequestParser()
		data = request.get_json()
		resp_list = []
		etcd_manager = EtcdManagement()
		deleted_flag = None
		for key_path in data:
			try:
				deleted_flag = etcd_manager.remove_key(key_path)
			except:
				resp_list.append({"key": key_path, "status": "failed", "code": 1002})
				continue
			if deleted_flag:
				resp_list.append({"key": key_path, "status": "success"})
			else:
				resp_list.append({"key": key_path, "status": "failed", "code": 1002})
			deleted_flag = None
		return jsonify(resp_list)