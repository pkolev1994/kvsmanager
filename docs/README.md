###Python RestFul api for commands and configs send by web

###Description 

Listens on port 9002

For commands :::

	GET http://0.0.0.0:9002/commands 
	Returns json format of all received commands

	GET http://0.0.0.0:9002/commands/target 
	Returns json format of all received commands for the specific target

	POST http://0.0.0.0:9002/commands 
	Accept json format for the post request:: { "target": "10.102.7.125", "command_name": "mkdir", "parameters": "/aux0/platform/ocorchestrator/" }

	DELETE http://0.0.0.0:9002/commands/target

For confs :::

	POST http://0.0.0.0:9002/etcd/confs
	Accept json format for the post request :: 
	{
	   "key1":"HTTP_CLIENT-22222-GG.xml",
	   "value1":"<?xml version=\"1.0\" encoding=\"utf-8\"?>\r\n<!-- Copyright 2007-2018. Opencode Systems Ltd.-->\r\n<connector>\r\n  <enabled>Y<\/enabled><\/connector> \r\n",
	   "import_type":"connector",
	   "micro_app":"smsc_conn_http_client",
	   "hostnames":"smsc_conn_http_client_1,smsc_conn_http_client_5,smsc_conn_http_client_2,smsc_conn_http_client_4",
	   "key2":"GG.xml",
	   "value2":"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\r\n<\/cross_plugin> \r\n"
	}

#NOTE::

	key2 and value2 are not mendatory
	They are only for connectors configs

#NOTE::