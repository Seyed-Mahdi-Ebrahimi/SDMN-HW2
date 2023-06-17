from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import cgi

PORT = 8000
HOST_NAME = "0.0.0.0"

class Server(BaseHTTPRequestHandler):
    status = "OK"

    def do_GET(self):
        if self.path == "/api/v1/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(bytes(json.dumps({"status" : self.status}), 'utf-8'))

    def do_POST(self):
        if self.path == "/api/v1/status":
            content_length = 0
            content_length = int(self.headers['Content-Length'])
            if content_length != 0:  
                post_data = self.rfile.read(content_length)
                post_dict = json.loads(post_data.decode('utf-8'))
                Server.status = post_dict["status"]
                self.send_response(201)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(bytes(json.dumps({"status":self.status}), 'utf-8'))
                
                
server = HTTPServer((HOST_NAME, PORT), Server)

print("Server Now Running...")
server.serve_forever()

server.server_close()
print("Server Stopped...")
