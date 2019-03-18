#!/usr/bin/python3.4

import time
import sys
import threading
sys.path.append('/aux0/customer/containers/ockvsman/lib/')
from http_server_simple import myHandler,Http_server_simple
from kvs_manager import kvsManager


kvsman = kvsManager()