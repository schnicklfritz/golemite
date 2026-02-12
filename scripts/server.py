import os
import json
import http.server
import socketserver
import urllib.parse
from pathlib import Path

PORT = 8000
DIRECTORY = "/workspace"

class GolemHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 1. API: Get Latest File
        if self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            try:
                # Find newest file in workspace (excluding hidden/.tmp)
                files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)]
                files = [f for f in files if os.path.isfile(f) and not f.endswith('.tmp') and not os.path.basename(f).startswith('.')]
                
                if not files:
                    self.wfile.write(json.dumps({"error": "No files found"}).encode())
                    return

                newest = max(files, key=os.path.getmtime)
                filename = os.path.basename(newest)
                
                response = {"filename": filename}
                self.wfile.write(json.dumps(response).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return

        # 2. Standard Download
        # Ensure we serve from workspace
        if self.path.startswith('/'):
            # Security: Prevent traversing up
            safe_path = os.path.normpath(DIRECTORY + urllib.parse.unquote(self.path))
            if not safe_path.startswith(DIRECTORY):
                self.send_error(403, "Access Denied")
                return
            
            # Map request to directory
            self.directory = DIRECTORY
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

print(f"🚀 Golem Smart Server running on port {PORT}")
os.chdir(DIRECTORY)
with socketserver.TCPServer(("", PORT), GolemHandler) as httpd:
    httpd.serve_forever()
