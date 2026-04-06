# 📱 Mobile Engineer - Permanent Web Server Setup

## 🚀 Quick Start (Permanent Fix)

### Method 1: Auto-Start on Windows Login (Recommended)
1. **Double-click**: `setup_autostart.bat`
2. **Restart your PC** - The web server will start automatically
3. **Access**: http://127.0.0.1:5000

### Method 2: Manual Start
1. **Double-click**: `start_server.bat`
2. **Wait** for server to start (shows "Running on http://127.0.0.1:5000")
3. **Access**: http://127.0.0.1:5000

### Method 3: Web Launcher
1. **Open**: `web_launcher.html` in your browser
2. **Click**: "Start Server" button
3. **Click**: "Open Web Application"

---

## 📁 Files Created

| File | Purpose |
|------|---------|
| `start_server.bat` | Starts the Flask web server |
| `setup_autostart.bat` | Sets up automatic startup on Windows login |
| `web_launcher.html` | Web-based launcher with status checking |

---

## 🔧 Troubleshooting

### Server Not Starting?
1. **Check Python Installation**:
   - Open Command Prompt
   - Type: `python --version`
   - If not found, install Python from https://python.org

2. **Check Flask Installation**:
   - Open Command Prompt
   - Type: `pip install flask`

3. **Manual Start**:
   ```cmd
   cd "c:\xampp\htdocs\mobile engineer"
   python app.py
   ```

### Port Already in Use?
1. **Kill existing process**:
   ```cmd
   netstat -ano | findstr :5000
   taskkill /PID [PID_NUMBER] /F
   ```

2. **Or change port in app.py**:
   - Change `app.run(debug=True)` to `app.run(debug=True, port=5001)`

---

## 🛠️ Advanced Setup

### Create Windows Service (Optional)
For more robust setup, you can create a Windows service:

1. **Install NSSM** (Non-Sucking Service Manager):
   - Download from https://nssm.cc/download
   - Extract to C:\nssm

2. **Create Service**:
   ```cmd
   cd C:\nssm
   nssm install MobileEngineer "python" "c:\xampp\htdocs\mobile engineer\app.py"
   nssm set MobileEngineer AppDirectory "c:\xampp\htdocs\mobile engineer"
   nssm set MobileEngineer DisplayName "Mobile Engineer Web Server"
   nssm set MobileEngineer Description "Mobile Engineer Management System"
   nssm start MobileEngineer
   ```

### Remove Auto-Start
To remove automatic startup:
1. **Delete shortcut**: `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\Mobile Engineer Web Server.lnk`
2. **Or run**: `setup_autostart.bat` and delete the mentioned file

---

## 🌐 Access URLs

- **Main Application**: http://127.0.0.1:5000
- **Products**: http://127.0.0.1:5000/products
- **Dashboard**: http://127.0.0.1:5000/dashboard
- **Web Launcher**: Open `web_launcher.html` file

---

## 📞 Support

If you still face issues:
1. Check Python is installed: `python --version`
2. Check Flask is installed: `pip show flask`
3. Check port availability: `netstat -ano | findstr :5000`
4. Try manual start with `start_server.bat`

---

## ✅ Verification

After setup, verify:
- [ ] Server starts automatically after PC restart
- [ ] Can access http://127.0.0.1:5000
- [ ] All features work (products, repairs, billing)
- [ ] No error messages in server console

**Your web server is now permanently fixed!** 🎉
