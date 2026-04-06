import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 5000

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('templates/user/login.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.wfile.write(b'<h1>Login Page</h1><p>Server is running!</p>')
        elif self.path == '/admin_login':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('templates/admin/admin_login.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.wfile.write(b'<h1>Admin Login</h1><p>Server is running!</p>')
        elif self.path == '/admin_dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('templates/admin/admin_dashboard.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.wfile.write(b'<h1>Admin Dashboard</h1><p>Server is running!</p>')
        elif self.path == '/dashboard':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            try:
                with open('templates/user/dashboard.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.wfile.write(content.encode('utf-8'))
            except:
                self.wfile.write(b'<h1>User Dashboard</h1><p>Server is running!</p>')
        elif self.path.startswith('/static/'):
            try:
                with open(self.path[1:], 'rb') as f:
                    content = f.read()
                    self.send_response(200)
                    self.send_header('Content-type', 'text/css' if self.path.endswith('.css') else 'application/octet-stream')
                    self.end_headers()
                    self.wfile.write(content)
            except:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'File not found')
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>404 Not Found</h1>')

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

print("""
╔════════════════════════════════════════════════════════════╗
║                    🚀 MOBILE ENGINEER WEBSITE                 ║
║                                                              ║
║  ✅ SERVER IS STARTING...                                       ║
║  📍 Your website: http://localhost:5000                        ║
║  🔍 Google Search: "localhost 5000"                             ║
║  🌐 Your website will open automatically!                      ║
║                                                              ║
║  ⚠️  Press Ctrl+C to stop the server                          ║
╚══════════════════════════════════════════════════════════════╝
""")

os.chdir(r'c:\xampp\htdocs\mobile engineer')

threading.Thread(target=open_browser, daemon=True).start()

try:
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"🚀 Server running on http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n🛑 Server stopped!")
except Exception as e:
    print(f"❌ Error: {e}")
    print("🔧 Try closing other programs using port 5000")
