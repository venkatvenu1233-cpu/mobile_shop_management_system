import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 5000

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if self.path == '/' or self.path == '/login':
            html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Login</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); 
               display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-card { background: white; padding: 2rem; border-radius: 15px; 
                     box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; }
        h1 { color: #333; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #667eea; color: white; padding: 0.5rem 1rem; border: none; 
                border-radius: 5px; cursor: pointer; margin: 0.5rem; }
        button:hover { background: #764ba2; }
        .admin-btn { position: fixed; top: 20px; right: 20px; background: #ff6b35; 
                     color: white; padding: 0.5rem 1rem; border: none; border-radius: 20px; 
                     cursor: pointer; text-decoration: none; }
    </style>
</head>
<body>
    <a href="/admin_login" class="admin-btn">Admin Login</a>
    <div class="login-card">
        <h1>MOBILE ENGINEER</h1>
        <h2>User Login</h2>
        <form action="/login" method="post">
            <input type="text" placeholder="Username" required>
            <input type="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
        <p>Don't have an account? <a href="/register">Register</a></p>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode())
        elif self.path == '/admin_login':
            html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Admin Login</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #1e3c72, #667eea); 
               display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-card { background: white; padding: 2rem; border-radius: 15px; 
                     box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; }
        h1 { color: #1e3c72; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; }
        button { background: #1e3c72; color: white; padding: 0.5rem 1rem; border: none; 
                border-radius: 5px; cursor: pointer; margin: 0.5rem; }
        button:hover { background: #667eea; }
        .back-btn { position: fixed; top: 20px; left: 20px; background: rgba(255,255,255,0.2); 
                    color: white; padding: 0.5rem 1rem; border: none; border-radius: 20px; 
                    cursor: pointer; text-decoration: none; }
    </style>
</head>
<body>
    <a href="/" class="back-btn">Back</a>
    <div class="login-card">
        <h1>Admin Portal</h1>
        <h2>Administrator Login</h2>
        <form action="/admin_login" method="post">
            <input type="text" placeholder="Admin Username" required>
            <input type="password" placeholder="Admin Password" required>
            <button type="submit">Login as Admin</button>
        </form>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode())
        elif self.path == '/dashboard':
            html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Dashboard</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; margin: 0; }
        .header { background: #667eea; color: white; padding: 1rem; text-align: center; }
        .content { padding: 2rem; text-align: center; }
        .card { background: white; padding: 1rem; margin: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { margin: 0; }
    </style>
</head>
<body>
    <div class="header">
        <h1>User Dashboard</h1>
    </div>
    <div class="content">
        <div class="card">
            <h2>Welcome to MOBILE ENGINEER!</h2>
            <p>Your user dashboard is working perfectly!</p>
            <p><a href="/">Back to Login</a></p>
        </div>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode())
        elif self.path == '/admin_dashboard':
            html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Admin Dashboard</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; margin: 0; }
        .header { background: #1e3c72; color: white; padding: 1rem; text-align: center; }
        .content { padding: 2rem; text-align: center; }
        .card { background: white; padding: 1rem; margin: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { margin: 0; }
        .stats { display: flex; justify-content: space-around; margin: 2rem 0; }
        .stat { text-align: center; }
        .stat-number { font-size: 2rem; font-weight: bold; color: #1e3c72; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Admin Dashboard</h1>
    </div>
    <div class="content">
        <div class="card">
            <h2>Welcome Admin!</h2>
            <p>Your admin dashboard is working perfectly!</p>
        </div>
        <div class="card">
            <h3>Statistics</h3>
            <div class="stats">
                <div class="stat">
                    <div class="stat-number">150</div>
                    <div>Total Products</div>
                </div>
                <div class="stat">
                    <div class="stat-number">25</div>
                    <div>Low Stock Items</div>
                </div>
                <div class="stat">
                    <div class="stat-number">50000</div>
                    <div>Today's Sales (Rs)</div>
                </div>
            </div>
        </div>
        <p><a href="/admin_login">Back to Admin Login</a></p>
    </div>
</body>
</html>"""
            self.wfile.write(html.encode())
        else:
            self.wfile.write(b'<h1>404 - Page Not Found</h1><p><a href="/">Go Home</a></p>')

def open_browser():
    time.sleep(2)
    webbrowser.open('http://localhost:5000')

print("""
====================================================
                MOBILE ENGINEER WEBSITE
====================================================
    SERVER IS STARTING...
    Your website: http://localhost:5000
    Google Search: "localhost 5000"
    Your website will open automatically!
    
    Press Ctrl+C to stop the server
====================================================
""")

os.chdir(r'c:\xampp\htdocs\mobile engineer')

threading.Thread(target=open_browser, daemon=True).start()

try:
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped!")
except Exception as e:
    print(f"Error: {e}")
    print("Try closing other programs using port 5000")
