import http.server
import socketserver
import webbrowser
import threading
import time
import os

PORT = 5000

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Map routes to actual HTML files
        if self.path == '/' or self.path == '/login':
            self.serve_file('templates/login.html')
        elif self.path == '/userlogin':
            self.serve_file('templates/user/login.html')
        elif self.path == '/dashboard':
            self.serve_file('templates/dashboard.html')
        elif self.path == '/mobiles':
            self.serve_file('templates/mobiles.html')
        elif self.path == '/accessories':
            self.serve_file('templates/accessories.html')
        elif self.path == '/basic_service':
            self.serve_file('templates/basic_service.html')
        elif self.path == '/chip_level_service':
            self.serve_file('templates/chip_level_service.html')
        elif self.path == '/cart':
            self.serve_file('templates/cart.html')
        elif self.path == '/checkout':
            self.serve_file('templates/checkout.html')
        elif self.path == '/admin_login':
            self.serve_file('templates/admin/admin_login.html')
        elif self.path == '/admin_dashboard':
            self.serve_file('templates/admin/admin_dashboard.html')
        else:
            # Try to serve the file directly
            try:
                super().do_GET()
            except:
                self.send_error(404, "Page Not Found")
    
    def serve_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(content.encode())
        except FileNotFoundError:
            self.send_error(404, f"File not found: {filepath}")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

def open_browser():
    time.sleep(1)
    webbrowser.open(f'http://localhost:{PORT}/dashboard')

def start_server():
    with socketserver.TCPServer(("", PORT), CustomHandler) as httpd:
        print(f"Server running at http://localhost:{PORT}/")
        print(f"Dashboard: http://localhost:{PORT}/dashboard")
        print(f"Mobiles: http://localhost:{PORT}/mobiles")
        print(f"Cart: http://localhost:{PORT}/cart")
        print(f"Checkout: http://localhost:{PORT}/checkout")
        print(f"Accessories: http://localhost:{PORT}/accessories")
        print(f"Basic Service: http://localhost:{PORT}/basic_service")
        print(f"Chip Level Service: http://localhost:{PORT}/chip_level_service")
        print("Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped by user")

if __name__ == "__main__":
    # Start browser in a separate thread
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    start_server()
