# -*- coding: utf8 -*-

import time
import threading

from icapserver import *

class ExampleICAPHandler(BaseICAPRequestHandler):

	def example_OPTIONS(self):
		self.set_icap_response(200)
		self.set_icap_header('Methods', 'RESPMOD')
		self.set_icap_header('Service', 'ICAP Server 1.0')
		self.set_icap_header('Options-TTL', '3600')
		self.set_icap_header('Preview', '0')
		self.send_headers(False)

	def example_REQMOD(self):
		self.no_adaptation_required()

	def example_RESPMOD(self):
		self.set_icap_response(200)

		self.set_enc_status(' '.join(self.enc_res_status))
		for h in self.enc_res_headers:
			for v in self.enc_res_headers[h]:
				self.set_enc_header(h, v)

		if not self.has_body:
			self.send_headers(False)
			return
		if self.preview:
			prevbuf = ''
			while True:
				chunk = self.read_chunk()
				if chunk == '':
					break
				prevbuf += chunk
			if self.ieof:
				self.send_headers(True)
				if len(prevbuf) > 0:
					self.write_chunk(prevbuf)
				self.write_chunk('')
				return
			self.cont()
			self.send_headers(True)
			if len(prevbuf) > 0:
				self.write_chunk(prevbuf)
			while True:
				chunk = self.read_chunk()
				self.write_chunk(chunk)
				if chunk == '':
					break
		else:
			self.send_headers(True)
			while True:
				chunk = self.read_chunk()
				self.write_chunk(chunk)
				if chunk == '':
					break

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
