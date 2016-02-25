icapserver
==========

A barebone icap server written in python and framework
to write your own simple icap servers.

Installation
------------

Just copy icap_server.py file onto your PYTHON_PATH, 
or the directory of your python module.

TODO: add setup.py

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

Just import stuff from the icap_server package, extend the protocol handler 
class and start the server:

```python
# -*- coding: utf8 -*-

import SocketServer
from icap_server import *

class SimpleServer(SocketServer.ThreadingMixIn, ICAPServer):
	pass

class ICAPHandler(BaseICAPRequestHandler):

	def echo_OPTIONS(self):
		self.set_icap_response(200)
		self.set_icap_header('Methods', 'RESPMOD')
		self.set_icap_header('Preview', '0')
		self.send_headers(False)

	def echo_RESPMOD(self):
		self.no_adaptation_required()

port = 13440

server = SimpleServer(('', port), ICAPHandler)
try:
	while 1:
		server.handle_request()
except KeyboardInterrupt:
	print "Finished"
```

ICAP defines three HTTP-like methods: OPTIONS, REQMOD and RESPMOD.

OPTIONS must be handled in every case. An endpoint has to support either
REQMOD or RESPMOD, but not both. However, this is not enforced, and
according to the squid 3 documentation, such overloading will even work
with squid.

REQMOD is called, when a HTTP request must be modified - like checking
access to an URL, stripping or adding query string parameters or POST
data, modifying headers or otherwise mangling the request.

RESPMOD is called when a HTTP response must be modified - such as
checking to-be-downloaded files for viruses, watermarking images or
audio files, placing ad banners, or otherwise modifying the content
and/or the headers of the request.

Various information can be extracted from the ICAP request by examining
certain fields of the handler object:

* command: the current ICAP command
* enc_req: encapsulated request line, list with 3 elements
* enc_req_headers: encapsulated request headers, dictionary of lists
* enc_res_status: encapsulated response status
* enc_res_headers: encapsulated response headers
* has_body: True, if the ICAP request has a body
* encapsulated: contains the "Encapsulated:" header's content as a dict
* ieof: True, if read_chunk() encounters an ieof chunk extension
* request_uri: contains the full request URI of the ICAP request
* preview: None, or an integer that arrived in the Preview header
* allow: Contains a set() of Allow:-ed stuff
* icap_response_code: contains the response code.

There are several helper methods that can be called while serving a
requests:

* send_error(error_code): Sends and entire ICAP error response
* no_adaptation_required(): Sends 204 No adaptation to the client.
* cont(): Sends an ICAP 100 Continue response to the client.
* read_chunk(): Reads a chunk from the client. Be aware that this call  
	blocks. If there is no available data on the line, and Connection: 
	keep-alive is used, it will cause the server to hang.
* set_icap_response(code): Sets the ICAP response.
* set_enc_status(status): Sets the encapsulated status line.
* set_enc_request(request): Sets the encapsulated request line.
* set_enc_header(header, value): Set an encapsulated header.
* set_icap_header(header, value): Set an ICAP header.
* send_chunk(data): writes a chunk to the client.