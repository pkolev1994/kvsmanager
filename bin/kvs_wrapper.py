import sys
sys.path.append('/aux0/customer/containers/ockvsman/')
from lib import app


app.run('0.0.0.0', port = 9002, debug = True)