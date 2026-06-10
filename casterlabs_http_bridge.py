from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import socket
import json

def send_to_minecraft(platform, user, message):
    payload = json.dumps({
        "platform": platform,
        "user": user,
        "message": message
    }, ensure_ascii=False)

    s = socket.socket()
    s.connect(("localhost", 4567))
    s.sendall((payload + "\n").encode("utf-8"))
    s.close()

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)

        platform = query.get("platform", ["Caffeinated"])[0]
        user = query.get("user", ["Unknown"])[0]
        message = query.get("message", [""])[0]

        if message:
            send_to_minecraft(platform, user, message)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"ok")

server = HTTPServer(("127.0.0.1", 8787), Handler)
print("Casterlabs HTTP bridge running on http://127.0.0.1:8787")
server.serve_forever()

def do_POST(self):
    if self.path != "/minecraft":
        self.send_response(404)
        self.end_headers()
        return

    length = int(self.headers.get("Content-Length", 0))
    body = self.rfile.read(length).decode("utf-8")

    print("Minecraft -> Stream:", body)

    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"ok")