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
		self.no_adaptation_required()

	def test_RESPMOD(self):
		self.set_icap_response(200)
		self.set_enc_status(' '.join(self.enc_res_status))
		for h in self.enc_res_headers:
			for v in self.enc_res_headers[h]:
				if h.lower() == "server":
					v = "ICAP POWERED SERVER!"
				self.set_enc_header(h, v)
		self.set_enc_header("ICAP", "POWERED")
		
		self.send_headers(True)
		while True:
			chunk = self.read_chunk()
			self.write_chunk(chunk)
			if chunk == '':
				break

port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print "Finished"
