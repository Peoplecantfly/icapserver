icapserver
==========

A Python framework for writing ICAP servers

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
