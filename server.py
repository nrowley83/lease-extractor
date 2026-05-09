#!/usr/bin/env python3
"""Static file server + Anthropic API proxy to avoid browser CORS restrictions."""
import http.server, json, urllib.request, urllib.error, os, sys

PORT = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))
MIME = {'.html':'text/html','.css':'text/css','.js':'application/javascript',
        '.json':'application/json','.png':'image/png','.ico':'image/x-icon'}

class Handler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self._cors(200)

    def do_GET(self):
        path = self.path.split('?')[0]
        if path == '/': path = '/index.html'
        fp = os.path.join(ROOT, path.lstrip('/'))
        try:
            with open(fp, 'rb') as f: body = f.read()
            ext = os.path.splitext(fp)[1]
            self._cors(200, MIME.get(ext, 'application/octet-stream'))
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_response(404); self.end_headers()

    def do_POST(self):
        if self.path != '/api/anthropic':
            self.send_response(404); self.end_headers(); return
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        api_key = self.headers.get('X-Api-Key', '')
        req = urllib.request.Request(
            'https://api.anthropic.com/v1/messages', data=body,
            headers={'x-api-key': api_key, 'anthropic-version': '2023-06-01',
                     'content-type': 'application/json'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                rb = r.read()
                self._cors(r.status, 'application/json')
                self.wfile.write(rb)
        except urllib.error.HTTPError as e:
            rb = e.read()
            self._cors(e.code, 'application/json')
            self.wfile.write(rb)

    def _cors(self, code, ct=None):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, X-Api-Key')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        if ct: self.send_header('Content-Type', ct)
        self.end_headers()

    def log_message(self, *_): pass  # silence request logs

if __name__ == '__main__':
    with http.server.HTTPServer(('', PORT), Handler) as s:
        print(f'Lease Extractor running at http://localhost:{PORT}', flush=True)
        s.serve_forever()
