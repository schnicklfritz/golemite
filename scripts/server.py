import os
import json
import http.server
import socketserver
import urllib.parse
import sys

PORT = 8000
DIRECTORY = "/workspace"

# Grandmaster Fix: Ensure directory exists so it doesn't crash
if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY, exist_ok=True)

class GolemHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Fix: Add CORS to allow requests from anywhere
        self.send_header('Access-Control-Allow-Origin', '*')
        http.server.SimpleHTTPRequestHandler.end_headers(self)

    def do_GET(self):
        # API: Latest File
        if self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                # Get files, sort by time, ignore hidden/.tmp
                files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)]
                files = [f for f in files if os.path.isfile(f) and not f.endswith('.tmp') and not os.path.basename(f).startswith('.')]
                
                if not files:
                    self.wfile.write(json.dumps({"error": "No files found in workspace"}).encode())
                else:
                    newest = max(files, key=os.path.getmtime)
                    filename = os.path.basename(newest)
                    self.wfile.write(json.dumps({"filename": filename}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # Normal File Serving
        self.directory = DIRECTORY
        return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"🚀 Golem Server active. Root: {DIRECTORY}, Port: {PORT}")
os.chdir(DIRECTORY)
# Fix: Allow reuse of address to prevent "Port already in use" on restarts
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), GolemHandler) as httpd:
    httpd.serve_forever()
