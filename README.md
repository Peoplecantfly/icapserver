icapserver
==========

A barebone icap server written in python.
But mostly this is a framework to write your own ICAP servers.

I work as QA Engineer and wrote this just for my tests porpuses.

Installation
------------

Use `python seutp.py install` or simply copy icapserver.py file 
onto your PYTHON_PATH or the directory of your python module.
Also  you can install this module with pip: `pip install icapserver`.

Usage
-----
For more information check [Tutorial](https://github.com/Peoplecantfly/icapserver/blob/master/TUTORIAL.md)

Just import stuff from the icapserver package, extend the protocol handler 
class and start the server:

```python
# -*- coding: utf8 -*-

import time
import threading

from icapserver import *

class ExampleICAPHandler(BaseICAPRequestHandler):

	def example_OPTIONS(self):
		self.set_icap_response(200)
		self.set_icap_header('Methods', 'RESPMOD, REQMOD')
		self.set_icap_header('Service', 'ICAP Server 1.0')
		self.set_icap_header('Options-TTL', '3600')
		self.set_icap_header('Preview', '0')
		self.send_headers(False)

	def example_REQMOD(self):
		self.no_adaptation_required()

	def example_RESPMOD(self):
		self.no_adaptation_required()

class ExampleICAPServer():

	def __init__(self, addr='', port=13440):
		self.addr = addr
		self.port = port

	def start(self):
		self.server = ICAPServer((self.addr, self.port), ExampleICAPHandler)
		self.thread = threading.Thread(target=self.server.serve_forever)
		self.thread.start()
		return True

	def stop(self):
		self.server.shutdown()
		self.server.server_close()
		self.thread.join(2)
		return True


try:
	server = ExampleICAPServer()
	server.start()
	print 'Use Control-C to exit'
	while True:
		time.sleep(1)
except KeyboardInterrupt:
	server.stop()
	print "Finished"
```
For more information check [Tutorial](https://github.com/Peoplecantfly/icapserver/blob/master/TUTORIAL.md)
