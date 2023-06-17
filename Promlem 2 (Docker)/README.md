# Problem 3 (Docker)

A simple server is defined in `MySimpleHttpServer.py` that hold the status.

To get the status, we should send a GET request to the `localhost:8000/api/v1/status` address.

The server responds to `GET` requests with code 200 and also gives a json file as follows.

**{ "status" : "OK" } OR { "status" : "not OK" }**

To set status ("OK" or "not OK"), we must send a `POST` requests to the server. The request body should contain one of the following json value.

**{ "status" : "OK" } OR { "status" : "not OK" }**

The server's response to POST requests is 201, and also gives a json file containing the status as follows.

**{ "status" : "OK" } OR { "status" : "not OK" }**
