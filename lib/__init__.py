import re
import time
import json
import sys
import os
import markdown
import datetime
from ast import literal_eval
from sqlalchemy import create_engine
from flask import Flask, g, request, jsonify
from flask_restful import Api, Resource, reqparse
###custom libs
sys.path.append('/aux0/customer/containers/ocpytools/lib/')
from etcd_client import EtcdManagement
from logger import Logger


app = Flask(__name__)
api = Api(app)

db_connect = create_engine('sqlite:///commands.db')
if not db_connect.dialect.has_table(db_connect, 'commands'):
	conn = db_connect.connect()
	conn.execute("""CREATE TABLE commands 
					(target varchar(255), 
					command_name varchar(255), 
					parameters varchar(255), 
					post_date varchar(255) )""")


@app.teardown_appcontext
def teardown_db(exception):
	db = getattr(g, '_database', None)
	if db is not None:
		db.close()


@app.route("/")
def index():

	with open(os.path.dirname(app.root_path) +  '/docs/' + 'README.md', 'r') as markdown_file:
		
		content = markdown_file.read()
		return markdown.markdown(content)



class CommandsList(Resource):
	def get(self):

		conn = db_connect.connect()
		query = conn.execute("select * from commands")
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

		#If the key does not exist in data store , will return 404

		if not result['data']:
			return {'message': "There aren't any commands for targets", \
					'data': {}}, 404

		return result, 200


	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('target', required=True)
		parser.add_argument('command_name', required=True)
		parser.add_argument('parameters', required=False)
		parser.add_argument('post_date', '{}'.format(datetime.datetime.now()))

		# Parse the arguments into an object
		args = parser.parse_args()
		###second way
		conn = db_connect.connect()
		conn.execute("""INSERT INTO commands 
					(target, command_name, parameters, post_date) 
					values ('{}', '{}', '{}', '{}')""".format(args['target'], \
															args['command_name'], \
															args['parameters'], \
															datetime.datetime.now()))

		return {'message': 'Command was registered successfully', 'data': args}



class Command(Resource):

	def get(self, target):

		conn = db_connect.connect()
		query = conn.execute("select * from commands where target='{}'".format(target))
		result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

		#If the key does not exist in data store , will return 404

		if not result['data']:
			return {'message': "Target wasn't found", 'data': {}}, 404

		return result, 200


	def delete(self, target):

		#If the key does not exist in data store , will return 404
		conn = db_connect.connect()
		query = conn.execute("DELETE FROM commands WHERE target='{}'".format(target))

		return '', 204


class Etcd_kvs(Resource):


	# def get(self):

	# 	conn = db_connect.connect()
	# 	query = conn.execute("select * from commands where target='{}'".format(target))
	# 	result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}

	# 	#If the key does not exist in data store , will return 404

	# 	if not result['data']:
	# 		return {'message': "Target wasn't found", 'data': {}}, 404

	# 	return result, 200

	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('micro_app', required=True)
		parser.add_argument('hostnames', required=True)
		parser.add_argument('import_type', required=True)
		parser.add_argument('key1', required=True)
		parser.add_argument('value1', required=True)
		parser.add_argument('key2', required=False)
		parser.add_argument('value2', required=False)
		# Parse the arguments into an object
		web_params = parser.parse_args()
		logger = Logger(filename = "kvs_wrapper", \
						logger_name = "myHandler do_POST", \
						dirname="/aux1/ockvsman/logs/")

		etcdman = EtcdManagement()
		logger.info("Handle params from web => {}".format(web_params))

		generated_id = self.generate_ids(web_params, etcdman)[web_params['micro_app']]
		logger.info("Generated id => {}".format(generated_id))
		etcdman.write(new_key="/platform/{}/general/confs/{}". \
					format(web_params['micro_app'], web_params['key1']), \
						value = web_params['value1'])

		logger.info("Write Key 1=> /platform/{}/general/confs/{}\tValue 2=> {}". \
				format(web_params['micro_app'], web_params['key1'], web_params['value1']))

		if web_params['import_type'] == 'connector':
			etcdman.write(new_key="/platform/{}/general/confs/{}". \
					format(web_params['micro_app'], web_params['key2']), \
							value = web_params['value2'])
			logger.info("Write Key 2=> /platform/{}/general/confs/{}\tValue 2=> {}". \
					format(web_params['micro_app'], web_params['key2'], web_params['value2']))

		etcdman.write(new_key="/platform/{}/general/ids/{}". \
				format(web_params['micro_app'], web_params['key1']), value=generated_id)
		logger.info("Write id => {} in ETCD => /platform/{}/general/ids/{}". \
				format(generated_id, web_params['micro_app'], web_params['key1']))
		time.sleep(1)

		status_results = {}
		hostnames = web_params['hostnames'].split(',')
		for i in range(1,5):
			for hostname in hostnames:
				taken_status = etcdman.get_config_statuses(hostname = hostname, \
														conf_name = web_params['key1'])
				if taken_status:
					returned_status = json.loads(taken_status)
					if int(returned_status['id']) == generated_id:
						status_results[hostname] = returned_status
						hostnames.remove(hostname)
			time.sleep(1)

		if hostnames:
			for hostname in hostnames:
				status_results[hostname] = {"id": generated_id, \
											"timestamp": '{}'.format(datetime.datetime.now()), \
											"status": "unknown"}

		logger.clear_handler()

		if web_params:
			return {'message': 'Config was registered successfully', 'data': status_results}, 200
		else:
			return {'message': "Config wasn't registered successfully"}, 401


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



class EtcdAddKey(Resource):

	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('key', required=True)
		parser.add_argument('value', required=True)
		# parser.add_argument('post_date', '{}'.format(datetime.datetime.now()))


		# Parse the arguments into an object
		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		try:
			etcd_manager.write(new_key = args['key'], value = args['value'])
		except:
			return {'message': "Key wasn't registered successfully"}, 401

		return {'message': 'Key was registered successfully'}, 200


class EtcdPushConfs(Resource):

	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('hostnames', required=True)
		parser.add_argument('key', required=True)
		parser.add_argument('file_value', required=True)
		parser.add_argument('file_path', required=True)
		parser.add_argument('return_result', required=True)
		parser.add_argument('regex', required=False)
		parser.add_argument('command', required=False)
		# parser.add_argument('post_date', '{}'.format(datetime.datetime.now()))


		# Parse the arguments into an object
		args = parser.parse_args()
		etcd_manager = EtcdManagement()

		try:
			key_value = literal_eval(etcd_manager.read_key(key = args['key']))
			curr_id = int(key_value['id']) + 1
		except:
			curr_id = 1

		conf_name = re.search(r".*\/(.*?$)", args['key'], re.I|re.S).group(1)
		json_key = {
					"hostnames": args['hostnames'], \
					"file_path": args['file_path'], \
					"file_value": args['file_value'], \
					"return_result": args['return_result'], \
					"regex": args['regex'],
					"command": args['command'],
					"id": curr_id}
		try:
			if re.search(r"False", args['return_result'], re.I|re.S): 
				etcd_manager.write(new_key = args['key'], value = json_key)
				return {'message': 'Config was registered successfully'}, 200
			elif re.search(r"True", args['return_result'], re.I|re.S):
				etcd_manager.write(new_key = args['key'], value = json_key)
				status_results = {}
				hostnames = args['hostnames'].split(',')
				for i in range(1,5):
					for hostname in hostnames:
						taken_status = etcd_manager.get_config_statuses(hostname = hostname, \
																conf_name = conf_name)
						if taken_status:
							returned_status = json.loads(taken_status)
							if int(returned_status['id']) == curr_id:
								status_results[hostname] = returned_status
								hostnames.remove(hostname)
					time.sleep(1)

				if hostnames:
					for hostname in hostnames:
						status_results[hostname] = {"id": curr_id, \
													"timestamp": '{}'.format(datetime.datetime.now()), \
													"status": "unknown"}
				return {'message': 'Config was registered successfully', 'data': status_results}, 200
		except:
			return {'message': "Something went wrong"}, 401



class EtcdGetKey(Resource):

	def post(self):

		parser = reqparse.RequestParser()

		parser.add_argument('key', required=True)
		# parser.add_argument('post_date', '{}'.format(datetime.datetime.now()))


		# Parse the arguments into an object
		args = parser.parse_args()
		etcd_manager = EtcdManagement()
		key_data = None
		try:
			key_data = etcd_manager.read_key(args['key'])
		except:
			return {'message': "Key can't be get!!"}, 401

		return {'message': 'Key was get successfully', 'data' : key_data}, 200


api.add_resource(CommandsList, '/commands')
api.add_resource(Command, '/commands/<string:target>')
api.add_resource(Etcd_kvs, '/etcd/confs')
api.add_resource(EtcdAddKey, '/addkey')
api.add_resource(EtcdPushConfs, '/pushconfs')
api.add_resource(EtcdGetKey, '/getkey')