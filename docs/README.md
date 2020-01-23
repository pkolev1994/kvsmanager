###Python RestFul api for commands and configs send by web

###Description 

Listens on port 9002

#For commands :::

	GET http://0.0.0.0:9002/commands 
	Returns json format of all received commands

	GET http://0.0.0.0:9002/commands/<target> 
	Returns json format of all received commands for the specific target

	POST http://0.0.0.0:9002/commands 
	Accept json format for the post request:: { "target": "10.102.7.125", "command_name": "mkdir", "parameters": "/aux0/platform/ocorchestrator/" }

	DELETE http://0.0.0.0:9002/commands/<target>

#For main application confs [browsers, gateways, connectors]:::

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

####NOTE::
	key2 and value2 are not mendatory parameters
	They are only for connectors configs
####NOTE::

#For rest application confs :::

	POST http://0.0.0.0:9002/pushconfs
	Accept json format for the post request :: 
{
	"hostnames": "smsc_ocpm_1",
	"key": "/platform/smsc_ocpm/general/confs/aaa.json",
	"file_path": "/aux0/customer/containers/occonfman/",
	"file_value": "{'312312312': 'fwdw'}",
	"return_result": "True",
	"regex": "occonfman",
	"command": "occonfman status"
}
####NOTE::
	regex and command are not mendatory parameters
	They are only when you want set return_result to be True
####NOTE::


#For adding only key in etcd key value store :::

	POST http://0.0.0.0:9002/addkey

{
	"key": "/platform/smsc_ocpm/general/confs/aaa.json",
	"value": "{'gosho': '12', 'pesho': '25'}"
}



#For get value of a  key in etcd key value store :::

	POST http://0.0.0.0:9002/getkey

{
	"key": "/platform/ussdc_br/general/confs/ocbrowser.xml"
}