import os
import json
import http.server
import socketserver

PORT = 8000
DIRECTORY = "/workspace"

if not os.path.exists(DIRECTORY):
    os.makedirs(DIRECTORY, exist_ok=True)

class GolemHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 1. ULTIMATE CORS: Allow all headers and methods for Proxy-thru
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type')
        super().end_headers()

    def do_OPTIONS(self):
        # 2. Pre-flight handshake for strict proxies
        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        # 3. API: Latest File Discovery
        if self.path == '/api/latest':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            try:
                files = [os.path.join(DIRECTORY, f) for f in os.listdir(DIRECTORY)]
                # Filter out hidden files and temp downloads (.crdownload / .tmp)
                files = [f for f in files if os.path.isfile(f) and not f.endswith(('.tmp', '.crdownload')) and not os.path.basename(f).startswith('.')]
                
                if not files:
                    self.wfile.write(json.dumps({"error": "No files found in workspace"}).encode())
                else:
                    newest = max(files, key=os.path.getmtime)
                    self.wfile.write(json.dumps({"filename": os.path.basename(newest)}).encode())
            except Exception as e:
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
            
        return super().do_GET()

# 4. TRICK: Change working directory to ensure SimpleHTTPRequestHandler finds files
os.chdir(DIRECTORY)
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), GolemHandler) as httpd:
    print(f"¿ Golem Server active on Port {PORT}")
    httpd.serve_forever()
