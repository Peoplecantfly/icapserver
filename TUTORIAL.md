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
### The OPTIONS method
### The REQMOD method
### The RESPMOD method
### 204 No Content
### Preview
Examples
========
### Example 0: Using the framework
### Example 1: 
### Example 2: 
### Example 3: 