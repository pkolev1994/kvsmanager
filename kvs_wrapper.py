#!/usr/bin/python3.6

import time
import sys
import threading
from lib.http_server_simple import myHandler,Http_server_simple
from lib.kvs_manager import kvsManager


kvsman = kvsManager()