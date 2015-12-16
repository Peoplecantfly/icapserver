# -*- coding: utf8 -*-

import random
import SocketServer

from icap_server import *

class ThreadingSimpleServer(SocketServer.ThreadingMixIn, ICAPServer):
	pass

class ICAPHandler(BaseICAPRequestHandler):

	def test_OPTIONS(self):
		self.set_icap_response(200)
		self.set_icap_header('Methods', 'RESPMOD, REQMOD')
		self.set_icap_header('Service', 'ICAP Server 1.0')
		self.set_icap_header('Options-TTL', '3600')
		self.send_headers(False)

	def test_REQMOD(self):
		self.set_icap_response(200)

		if self.enc_req[0] != "POST":
			self.set_enc_request(' '.join(self.enc_req))
			for h in self.enc_req_headers:
				for v in self.enc_req_headers[h]:
					self.set_enc_header(h, v)
			if not self.has_body:
				self.send_headers(False)
				return

			while True:
				chunk = self.read_chunk()
				if chunk == '':
					break
		else:
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
						v = len(buff)
					self.set_enc_header(h, v)

			self.send_headers(True)
			self.write_chunk(buff)

	def test_RESPMOD(self):
		self.no_adaptation_required()

port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print "Finished"
