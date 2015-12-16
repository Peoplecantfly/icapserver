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
		if self.has_body:
			while True:
				if self.read_chunk() == '':
					break
		self.set_icap_response(200)
		self.set_enc_status('HTTP/1.1 307 Temporary Redirect')
		self.set_enc_header('Location', 'http://example.com/')
		self.send_headers(False)

port = 13440

server = ThreadingSimpleServer(('', port), ICAPHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print "Finished"
