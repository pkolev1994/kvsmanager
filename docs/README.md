###Description 

Listens on port 9002

#For main application configs and commands update :::
POST /etcd/confs

URL Params:
	command_key[str] => key path in etcd for command (mandatory)
	command_value[json] => commands to be executed on specific hostname or group from nodes.xml (mandatory)
	content_key[str] => key path in etcd for config content (not mandatory)
	content_value[str] => config's content value (not mandatory)
	markers_key[str] => key path in etcd for markers (not mandatory)
	markers_value[json] => markers which should be replaced with value on specific hostnames (not mandatory)

Success Response:

	Code: 200
	Content: 	{
				    "message": "Request was registered successfully",
				    "status": "success"
				}

Error Response:
	Code: 400
	Content:	{
				    "message": {
				        "command_key": "Missing required parameter in the JSON body or the post body or the query string"
				    }
				}

Example:
	POST /etcd/confs 
	Content-Type: application/json
	Body:	{
				"command_key": "/pesho/{/home/ico/test1.xml}/command",
				"command_value": "{'g3':'date','OCBROWSER':'df -h','DB':'df','USSDGW':'ls'}",
				"content_key": "/pesho/{/home/ico/test1.xml}/content",
				"content_value": "<xml> adfsdfgsd </xml>",
				"markers_key": "/pesho/{/home/ico/test.xml}/markers",
				"markers_value": "{'ico':{'g3':'ON','server2':'OFF','server3':'OFF'},'ivan':{'g3':'1234','server2':'2','server3':'3'}}"
			}


#For Adding key value in etcd
POST /addkey

URL Params:
	key[str] => key path in etcd
	value[str] => value of the key in etcd

Success Response:
	Code: 200
	Content:	{
				    "message": "Key was registered successfully"
				}
Error Response:
	Code: 401
	Content:	{
					"message": "Key wasn't registered successfully"
				}

Example:
	POST /addkey
	Content-Type: application/json
	Body:	{
				"key": "/pesho/{/home/ico/test1.xml}/command",
				"value": "{'g3':'date','GW':'df -h','DB':'df','USSDGW':'ls'}"

			}


#For Get key value in etcd
POST /getkey

URL Params:
	etcd_key[str] => key path in etcd

Success Response:
	Code: 200
	Content:	{
				    "g3": "date",
				    "OCBROWSER": "df -h",
				    "DB": "df",
				    "USSDGW": "ls"
				}

Error Response:
	Code: 401
	Content:	{
				    "message": "Key can't be get!!"
				}

Example:
	POST /get_key
	Content-Type: application/json
	Body:	{
				"etcd_key": "/pesho/{/home/ico/test.xml}/maarkers"
			}




GET /addkey

URL Params:
	etcd_key[str] => key path in etcd

Success Response:
	Code: 200
	Content:	{
				    "g3": "date",
				    "OCBROWSER": "df -h",
				    "DB": "df",
				    "USSDGW": "ls"
				}

Error Response:
	Code: 401
	Content:	{
				    "message": "Key can't be get!!"
				}

Example:
	GET getkey?etcd_key=/configico123/{/home/ico/test2.xml}/command
	Body:	{
				"etcd_key": "/pesho/{/home/ico/test.xml}/maarkers"
			}


#For nodes_manager commands requests :::
POST /nodes_manager

URL Params:
	command[str] => nodes_manager command that should be executed (mandatory)
	return_result[str] => api will return output from command if it is set to True (not mandatory)

Success Response:

	Code: 200
	Content: 	{
				    "message": "nodes_manager command was executed!",
				    "output": "some data for the file\n"
				}


Example:
	POST /nodes_manager 
	Content-Type: application/json
	Body:	{
				"command":"nodes_manager vf-eg-sm.scelab.opencode.com dusage",
				"return_result": "True"
			}
