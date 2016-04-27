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
		if self.enc_req[0] != "POST":
			self.no_adaptation_required()
		else:
			self.set_icap_response(200)
			if not self.has_body:
				self.set_enc_request(' '.join(self.enc_req))
				for h in self.enc_req_headers:
					for v in self.enc_req_headers[h]:
						self.set_enc_header(h, v)
				self.send_headers(False)
				return
			
			buff = ''
			while True:
				chunk = self.read_chunk()
				if chunk == '':
					break
				buff += chunk

			buff += "&TestKey=TestValue"
			self.set_enc_request(' '.join(self.enc_req))
			for h in self.enc_req_headers:
				for v in self.enc_req_headers[h]:
					if h.lower() == 'content-length':
						v = str(len(buff))
					self.set_enc_header(h, v)

			self.send_headers(True)
			self.send_chunk(buff)

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
