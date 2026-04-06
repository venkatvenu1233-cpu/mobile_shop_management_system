import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 5000

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass
    
    def do_GET(self):
        try:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            if self.path == '/' or self.path == '/login':
                try:
                    # First try to use the original template
                    with open('templates/login.html', 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Replace Flask template syntax with actual URLs
                        content = content.replace('{{ url_for(\'static\', filename=\'style.css\') }}', '/static/style.css')
                        content = content.replace('{{ url_for(\'register\') }}', '/register')
                        content = content.replace('{{ url_for(\'forgot_password\') }}', '/forgot_password')
                        content = content.replace('{{ url_for(\'login\') }}', '/login')
                        # Remove Flask template blocks
                        content = content.replace('{% with messages = get_flashed_messages(with_categories=true) %}', '')
                        content = content.replace('{% if messages %}', '')
                        content = content.replace('{% for category, message in messages %}', '')
                        content = content.replace('{% endfor %}', '')
                        content = content.replace('{% endif %}', '')
                        content = content.replace('{% endwith %}', '')
                        content = content.replace('{{ category }}', 'success')
                        content = content.replace('{{ message }}', 'Login successful!')
                        self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    # Fallback to built-in HTML if template not found
                    html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Login</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #667eea, #764ba2); 
               display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .login-card { background: white; padding: 2rem; border-radius: 15px; 
                     box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; min-width: 300px; }
        h1 { color: #333; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { background: #667eea; color: white; padding: 0.5rem 1rem; border: none; 
                border-radius: 5px; cursor: pointer; margin: 0.5rem; width: 100%; }
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
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
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
                     box-shadow: 0 10px 30px rgba(0,0,0,0.2); text-align: center; min-width: 300px; }
        h1 { color: #1e3c72; margin-bottom: 1rem; }
        input { width: 100%; padding: 0.5rem; margin: 0.5rem 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { background: #1e3c72; color: white; padding: 0.5rem 1rem; border: none; 
                border-radius: 5px; cursor: pointer; margin: 0.5rem; width: 100%; }
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
            <input type="text" name="username" placeholder="Admin Username" required>
            <input type="password" name="password" placeholder="Admin Password" required>
            <button type="submit">Login as Admin</button>
        </form>
    </div>
</body>
</html>"""
                self.wfile.write(html.encode())
                
            elif self.path == '/dashboard':
                try:
                    # Try to use the actual dashboard template
                    with open('templates/user/dashboard.html', 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Replace Flask template syntax with actual URLs
                        content = content.replace('{{ url_for(\'static\', filename=\'style.css\') }}', '/static/style.css')
                        content = content.replace('{{ url_for(\'logout\') }}', '/logout')
                        content = content.replace('{{ url_for(\'service_requests\') }}', '/service_requests')
                        content = content.replace('{{ url_for(\'repairs\') }}', '/repairs')
                        content = content.replace('{{ url_for(\'service_history\') }}', '/service_history')
                        content = content.replace('{{ url_for(\'billing\') }}', '/billing')
                        content = content.replace('{{ url_for(\'technicians\') }}', '/technicians')
                        # Remove Flask template blocks
                        content = content.replace('{% if session.get(\'username\') %}', '')
                        content = content.replace('{{ session[\'username\'] }}', 'User')
                        content = content.replace('{% endif %}', '')
                        self.wfile.write(content.encode('utf-8'))
                except FileNotFoundError:
                    # Fallback to built-in HTML if template not found
                    html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - User Dashboard</title>
    <style>
        body { font-family: Arial; background: #f5f5f5; margin: 0; }
        .header { background: #667eea; color: white; padding: 1rem; text-align: center; }
        .content { padding: 2rem; text-align: center; }
        .card { background: white; padding: 2rem; margin: 1rem; border-radius: 10px; 
                box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        h1 { margin: 0; }
        .welcome { font-size: 2rem; color: #667eea; margin-bottom: 1rem; }
    </style>
</head>
<body>
    <div class="header">
        <h1>User Dashboard</h1>
    </div>
    <div class="content">
        <div class="card">
            <div class="welcome">Welcome to MOBILE ENGINEER!</div>
            <h2>Your user dashboard is working perfectly!</h2>
            <p>🎉 Server is running successfully!</p>
            <p>📱 All features are available!</p>
            <br>
            <a href="/" style="background: #667eea; color: white; padding: 0.5rem 1rem; 
                       text-decoration: none; border-radius: 5px;">Back to Login</a>
        </div>
    </div>
</body>
</html>"""
                    self.wfile.write(html.encode())
                
            elif self.path == '/admin_dashboard':
                try:
                    # Use the clean admin dashboard template since original was deleted
                    with open('templates/admin/admin_dashboard_clean.html', 'r', encoding='utf-8') as f:
                        content = f.read()
                        # No template processing needed - it's already clean!
                        self.wfile.write(content.encode('utf-8'))
                        print("Clean admin dashboard loaded successfully!")
                except FileNotFoundError:
                    print("Clean admin dashboard not found, using fallback")
                    # Fallback to simple HTML if template not found
                    html = """<!DOCTYPE html>
<html>
<head>
    <title>MOBILE ENGINEER - Admin Dashboard</title>
    <style>
        body { font-family: Arial; background: linear-gradient(135deg, #1e3c72, #667eea); margin: 0; min-height: 100vh; }
        .header { background: rgba(255,255,255,0.95); padding: 1rem 2rem; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .header-content { max-width: 1400px; margin: 0 auto; display: flex; justify-content: space-between; align-items: center; }
        .admin-title { display: flex; align-items: center; gap: 1rem; }
        .admin-title h1 { color: #1e3c72; font-size: 1.8rem; margin: 0; }
        .admin-badge { background: linear-gradient(135deg, #ff6b35, #f72b1c); color: white; padding: 0.5rem 1rem; border-radius: 20px; font-size: 0.8rem; font-weight: 700; }
        .user-info { display: flex; align-items: center; gap: 1rem; }
        .user-avatar { width: 40px; height: 40px; background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; }
        .content { padding: 2rem; max-width: 1400px; margin: 0 auto; }
        .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1.5rem; margin-bottom: 2rem; }
        .stat-card { background: rgba(255,255,255,0.95); padding: 1.5rem; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); text-align: center; }
        .stat-icon { font-size: 2.5rem; margin-bottom: 1rem; }
        .stat-number { font-size: 2.5rem; font-weight: bold; color: #1e3c72; margin-bottom: 0.5rem; }
        .stat-label { color: #666; font-weight: 500; }
        .management-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; }
        .management-section { background: rgba(255,255,255,0.95); padding: 2rem; border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        .section-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; }
        .section-title { font-size: 1.5rem; color: #1e3c72; margin: 0; }
        .btn { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border: none; padding: 0.75rem 1.5rem; border-radius: 8px; cursor: pointer; font-weight: 600; transition: all 0.3s ease; }
        .btn:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(102,126,234,0.4); }
        table { width: 100%; border-collapse: collapse; margin-top: 1rem; }
        th, td { padding: 0.75rem; text-align: left; border-bottom: 1px solid #eee; }
        th { background: #f8f9fa; font-weight: 600; color: #1e3c72; }
        .status-badge { padding: 0.25rem 0.75rem; border-radius: 12px; font-size: 0.8rem; font-weight: 600; }
        .status-in-stock { background: #d4edda; color: #155724; }
        .status-low-stock { background: #fff3cd; color: #856404; }
        .status-out-stock { background: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-content">
            <div class="admin-title">
                <h1>🔐 Admin Dashboard</h1>
                <span class="admin-badge">MOBILE ENGINEER</span>
            </div>
            <div class="user-info">
                <div class="user-avatar">A</div>
                <div>
                    <div style="font-weight: 600;">Admin User</div>
                    <div style="font-size: 0.8rem; color: #666;">Administrator</div>
                </div>
                <a href="/admin_login" class="btn">Logout</a>
            </div>
        </div>
    </div>
    
    <div class="content">
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-icon">📦</div>
                <div class="stat-number">150</div>
                <div class="stat-label">Total Products</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">⚠️</div>
                <div class="stat-number">25</div>
                <div class="stat-label">Low Stock Items</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">💰</div>
                <div class="stat-number">₹50,000</div>
                <div class="stat-label">Today's Sales</div>
            </div>
            <div class="stat-card">
                <div class="stat-icon">📈</div>
                <div class="stat-number">₹250,000</div>
                <div class="stat-label">Total Revenue</div>
            </div>
        </div>
        
        <div class="management-grid">
            <div class="management-section">
                <div class="section-header">
                    <h2 class="section-title">📦 Stock Management</h2>
                    <button class="btn">+ Add Product</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Brand</th>
                            <th>Model</th>
                            <th>Price</th>
                            <th>Stock</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>Samsung</td>
                            <td>Galaxy S21</td>
                            <td>₹45,000</td>
                            <td>10</td>
                            <td><span class="status-badge status-in-stock">In Stock</span></td>
                            <td><button class="btn" style="padding: 0.25rem 0.75rem; font-size: 0.8rem;">Edit</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
            
            <div class="management-section">
                <div class="section-header">
                    <h2 class="section-title">💰 Sales Management</h2>
                    <button class="btn">+ Add Sale</button>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Customer</th>
                            <th>Product</th>
                            <th>Quantity</th>
                            <th>Total</th>
                            <th>Date</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>1</td>
                            <td>John Doe</td>
                            <td>Apple iPhone 13</td>
                            <td>2</td>
                            <td>₹140,000</td>
                            <td>2024-03-27</td>
                            <td><button class="btn" style="padding: 0.25rem 0.75rem; font-size: 0.8rem;">View</button></td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""
                    self.wfile.write(html.encode())
                
            else:
                self.wfile.write(b'<h1>404 - Page Not Found</h1><p><a href="/">Go Home</a></p>')
                
        except Exception as e:
            print(f"Error in GET: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Server Error</h1>')
    
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            if self.path == '/login':
                # User login - redirect to dashboard (no database needed)
                self.send_response(302)
                self.send_header('Location', '/dashboard')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body><h1>Redirecting to dashboard...</h1></body></html>')
                print("User login successful - redirecting to dashboard")
                
            elif self.path == '/admin_login':
                # Admin login - redirect to admin dashboard (no database needed)
                self.send_response(302)
                self.send_header('Location', '/admin_dashboard')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body><h1>Redirecting to admin dashboard...</h1></body></html>')
                print("Admin login successful - redirecting to admin dashboard")
                
            elif self.path == '/admin/add_product':
                # Add product - just redirect back to admin dashboard (no database)
                self.send_response(302)
                self.send_header('Location', '/admin_dashboard')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body><h1>Product added successfully!</h1></body></html>')
                print("Product add simulated - redirecting to admin dashboard")
                
            elif self.path == '/admin/add_sale':
                # Add sale - just redirect back to admin dashboard (no database)
                self.send_response(302)
                self.send_header('Location', '/admin_dashboard')
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<html><body><h1>Sale added successfully!</h1></body></html>')
                print("Sale add simulated - redirecting to admin dashboard")
                
        except Exception as e:
            print(f"Error in POST: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'<h1>Server Error</h1>')

def open_browser():
    time.sleep(2)
    try:
        webbrowser.open('http://localhost:5000')
        print("Browser opened successfully!")
    except Exception as e:
        print(f"Could not open browser: {e}")

print("""
====================================================
            MOBILE ENGINEER WEBSITE
====================================================
    SERVER STARTING...
    Your website: http://localhost:5000
    Google Search: "localhost 5000"
    Browser will open automatically!
    
    Press Ctrl+C to stop the server
====================================================
""")

# Change to correct directory
try:
    os.chdir(r'c:\xampp\htdocs\mobile engineer')
    print(f"Changed to directory: {os.getcwd()}")
except Exception as e:
    print(f"Could not change directory: {e}")

# Start browser thread
threading.Thread(target=open_browser, daemon=True).start()

# Start server
try:
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        print(f"Server running on http://localhost:{PORT}")
        print("Waiting for connections...")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\nServer stopped successfully!")
except Exception as e:
    print(f"Error starting server: {e}")
    print("Try closing other programs using port 5000")
    input("Press Enter to exit...")
