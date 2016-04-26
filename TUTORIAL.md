Tutorial
========

This is a tutorial on how to use icapserver.
Required:
* A basic knowledge of the HTTP protocol [RFC 2616](https://tools.ietf.org/html/rfc2616)
* A basic knowledge of the ICAP protocol [RFC 3507](https://tools.ietf.org/html/rfc3507)

ICAP in a nutshell
==================
### Introduction
The Internet Content Adaptation Protocol (ICAP) is a lightweight HTTP-like protocol 
specified in [RFC 3507](https://tools.ietf.org/html/rfc3507) which is used to extend 
transparent proxy servers, thereby freeing up resources and standardizing the way 
in which new features are implemented. ICAP is generally used to implement 
virus scanning and content filters in transparent HTTP proxy caches. Content adaptation 
refers to performing the particular value added service (content manipulation) 
for the associated client request/response.
### ICAP headers
Most of all headers that used in ICAP are similar to their HTTP analogue:
`Cache-Control, Connection, Date, Expires, Pragma, Trailer, Upgrade` and some specific 
headers like `Encapsulated`.
The ICAP encapsulation model is a lightweight means of packaging any number of HTTP message 
sections into an encapsulating ICAP message-body, in order to allow the vectoring of requests, 
responses, and request/response pairs to an ICAP server. This is accomplished by concatenating 
interesting message parts (encapsulatED sections) into a single ICAP message-body 
(the encapsulatING message).  The encapsulated sections may be the headers or bodies of HTTP messages.

The offset of each encapsulated section's start relative to the start of the encapsulating 
message's body is noted using the "Encapsulated" header.  This header MUST be included in every ICAP message.
For example, the header 
```
Encapsulated: req-hdr=0, res-hdr=45, res-body=100
``` 
indicates a message that encapsulates a group of request headers, a group of response headers, 
and then a response body.  Each of these is included at the byte-offsets listed.  The byte-offsets are in
decimal notation for consistency with HTTP's Content-Length header. The special entity `null-body` 
indicates there is no encapsulated body in the ICAP message.

Also there are some specific ICAP headers but less important such as:
* ISTag - ICAP server tag.
* Options-TTL - how often to call ICAP server for options.
* Methods - allowed ICAP server methods (without OPTIONS)
* etc.

Also, anyone can add their own headers, that shoud starts with `X-ICAP-`.
For example: `X-ICAP-USERNAME`.

Methods
-------
All usefull info about all method you can read in RFC 3507, so there is just an example how it looks like:
### The OPTIONS method
```
OPTIONS icap://icap.server.net/sample-service ICAP/1.0
Host: icap.server.net
User-Agent: ICAP-Client-Library/2.3
-------------------------------------------------------------------------------------------
ICAP/1.0 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Methods: RESPMOD
Service: FOO Tech Server 1.0
ISTag: "W3E4R7U9-L2E4-2"
Encapsulated: null-body=0
Max-Connections: 1000
Options-TTL: 7200
Allow: 204
Preview: 2048
Transfer-Complete: asp, bat, exe, com
Transfer-Ignore: html
Transfer-Preview: *
```
### The REQMOD method
```
REQMOD icap://icap-server.net/server?arg=87 ICAP/1.0
Host: icap-server.net
Encapsulated: req-hdr=0, null-body=170

GET / HTTP/1.1
Host: www.origin-server.com
Accept: text/html, text/plain
Accept-Encoding: compress
Cookie: ff39fk3jur@4ii0e02i
If-None-Match: "xyzzy", "r2d2xxxx"
-------------------------------------------------------------------------------------------
ICAP/1.0 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Server: ICAP-Server-Software/1.0
Connection: close
ISTag: "W3E4R7U9-L2E4-2"
Encapsulated: req-hdr=0, null-body=231

GET /modified-path HTTP/1.1
Host: www.origin-server.com
Via: 1.0 icap-server.net (ICAP Example ReqMod Service 1.1)
Accept: text/html, text/plain, image/gif
Accept-Encoding: gzip, compress
If-None-Match: "xyzzy", "r2d2xxxx"   
```
```
REQMOD icap://icap-server.net/server?arg=87 ICAP/1.0
Host: icap-server.net
Encapsulated: req-hdr=0, req-body=147

POST /origin-resource/form.pl HTTP/1.1
Host: www.origin-server.com
Accept: text/html, text/plain
Accept-Encoding: compress
Pragma: no-cache

1e
I am posting this information.
0
-------------------------------------------------------------------------------------------
ICAP/1.0 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Server: ICAP-Server-Software/1.0
Connection: close
ISTag: "W3E4R7U9-L2E4-2"
Encapsulated: req-hdr=0, req-body=244

POST /origin-resource/form.pl HTTP/1.1
Host: www.origin-server.com
Via: 1.0 icap-server.net (ICAP Example ReqMod Service 1.1)
Accept: text/html, text/plain, image/gif
Accept-Encoding: gzip, compress
Pragma: no-cache
Content-Length: 45

2d
I am posting this information.  ICAP powered!
0
```
```
REQMOD icap://icap-server.net/content-filter ICAP/1.0
Host: icap-server.net
Encapsulated: req-hdr=0, null-body=119

GET /naughty-content HTTP/1.1
Host: www.naughty-site.com
Accept: text/html, text/plain
Accept-Encoding: compress
-------------------------------------------------------------------------------------------
ICAP/1.0 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Server: ICAP-Server-Software/1.0
Connection: close
ISTag: "W3E4R7U9-L2E4-2"
Encapsulated: res-hdr=0, res-body=213

HTTP/1.1 403 Forbidden
Date: Wed, 08 Nov 2000 16:02:10 GMT
Server: Apache/1.3.12 (Unix)
Last-Modified: Thu, 02 Nov 2000 13:51:37 GMT
ETag: "63600-1989-3a017169"
Content-Length: 58
Content-Type: text/html

3a
Sorry, you are not allowed to access that naughty content.
0
```
### The RESPMOD method
```
RESPMOD icap://icap.example.org/satisf ICAP/1.0
Host: icap.example.org
Encapsulated: req-hdr=0, res-hdr=137, res-body=296

GET /origin-resource HTTP/1.1
Host: www.origin-server.com
Accept: text/html, text/plain, image/gif
Accept-Encoding: gzip, compress

HTTP/1.1 200 OK
Date: Mon, 10 Jan 2000 09:52:22 GMT
Server: Apache/1.3.6 (Unix)
ETag: "63840-1ab7-378d415b"
Content-Type: text/html
Content-Length: 51
33
This is data that was returned by an origin server.
0
-------------------------------------------------------------------------------------------
ICAP/1.0 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Server: ICAP-Server-Software/1.0
Connection: close
ISTag: "W3E4R7U9-L2E4-2"
Encapsulated: res-hdr=0, res-body=222

HTTP/1.1 200 OK
Date: Mon, 10 Jan 2000  09:55:21 GMT
Via: 1.0 icap.example.org (ICAP Example RespMod Service 1.1)
Server: Apache/1.3.6 (Unix)
ETag: "63840-1ab7-378d415b"
Content-Type: text/html
Content-Length: 92

5c
This is data that was returned by an origin server, but with
value added by an ICAP server.
0
```
### Preview
ICAP REQMOD or RESPMOD requests sent by the ICAP client to the ICAP server may include a "preview". 
This feature allows an ICAP server to see the beginning of a transaction, then decide if it wants to 
opt-out of the transaction early instead of receiving the remainder of the request message. 
Previewing can yield significant performance improvements in a variety of situations.

ICAP servers SHOULD use the OPTIONS method tospecify how many bytes of preview are needed for a particular ICAP
application on a per-resource basis. Clients SHOULD be able to provide Previews of at least 4096 bytes.


Examples
========
For more examples you can check [examples](https://github.com/Peoplecantfly/icapserver/tree/master/examples) folder.  
*NB! In this realization of ICAP server you should use one "service name" for all methods, 
but basicly it depends on ICAP client realization.*
### Example 1: 204 No content
204 No content is for No content adaptation required.  
So this example sends 204 No content for both REQMOD and RESPMOD.
```
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
### Example 2: Simple POST Data changing
```
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
			self.write_chunk(buff)

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
### Example 3: Encapsulated 451 Error
```
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
		if self.has_body:
			while True:
				if self.read_chunk() == '':
					break
		self.set_icap_response(200)
		self.set_enc_status('HTTP/1.1 451 Unavailable For Legal Reasons')
		self.send_headers(False)

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