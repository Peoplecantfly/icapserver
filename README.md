icapserver
==========

A barebone icap server written in python.

Installation
------------

Use `python seutp.py install` or simply copy icapserver.py file 
onto your PYTHON_PATH or the directory of your python module.
Also  you can install this module with pip: `pip install icapserver`.

What is ICAP?
-------------

Internet Content Adaptation Protocol (ICAP)

From RFC 3507  
ICAP, the Internet Content Adaption Protocol, is a protocol aimed at
providing simple object-based content vectoring for HTTP services.
ICAP is, in essence, a lightweight protocol for executing a "remote
procedure call" on HTTP messages.  It allows ICAP clients to pass
HTTP messages to ICAP servers for some sort of transformation or
other processing ("adaptation").  The server executes its
transformation service on messages and sends back responses to the
client, usually with modified messages.  Typically, the adapted
messages are either HTTP requests or HTTP responses.

For more infromation see [RFC 3507](https://tools.ietf.org/html/rfc3507)

Usage
-----
For more info check [Tutorial](https://github.com/Peoplecantfly/icapserver/blob/master/TUTORIAL.md)

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
For more info check [Tutorial](https://github.com/Peoplecantfly/icapserver/blob/master/TUTORIAL.md)
