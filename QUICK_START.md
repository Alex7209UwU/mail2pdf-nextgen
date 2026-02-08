# Mail2PDF NextGen - QUICK START GUIDE

## 🚀 30 Second Start

### Windows Users:
1. Double-click: `START_SERVER.bat`
2. Open browser: `http://localhost:5000`
3. Done! ✅

### Linux/Mac Users:
```bash
pip install -r requirements.txt
python app.py
# Open: http://localhost:5000
```

---

## 📍 Important URLs

| Feature | URL |
|---------|-----|
| **Main Page** | `http://localhost:5000` |
| **Settings** | `http://localhost:5000/configure` |
| **About** | `http://localhost:5000/about` |
| **Docs** | `http://localhost:5000/documentation` |

---

## ⚙️ Configure Page Features

At `http://localhost:5000/configure` you can:

✅ **Change Language**
- French (Français)
- English

✅ **Customize Colors**
- Primary color (main branding)
- Secondary color (accents)
- Accent color (highlights)
- Background color
- Text color

✅ **Upload Logo**
- PNG, JPG, or GIF
- Max 2MB
- Auto-integrated into interface

✅ **Save Settings**
- All changes saved immediately
- Persistent across restarts
- Stored in `data/config_dynamic.json`

---

## 📤 How to Use

### Step 1: Upload Emails
- Go to main page: `http://localhost:5000`
- Drag & drop email files OR click "Browse"
- Supported: EML, MSG, MBOX, ZIP

### Step 2: Options (Optional)
- Extract attachments
- Choose page size (A4, Letter, etc.)
- Choose orientation (Portrait/Landscape)

### Step 3: Convert
- Click "Convert to PDF"
- Wait for processing

### Step 4: Download
- Click "Download PDF (ZIP)"
- Get all converted PDFs in one file

---

## 📊 API Endpoints

**For advanced users/developers:**

```
POST /api/upload           → Convert emails
GET /api/status/<ID>      → Check progress
GET /api/download/<ID>    → Download results
GET /api/history          → View past conversions
```

---

## 🔧 System Requirements

- **Python**: 3.8 or higher
- **Port**: 5000 (must be available)
- **RAM**: 512 MB minimum
- **Disk**: 100 MB free space
- **Upload Size**: Up to 100 MB per file

---

## ⚠️ Troubleshooting

### Port 5000 in use?
Edit `app.py` line 590:
```python
app.run(host='0.0.0.0', port=8000)  # Change 5000 → 8000
```

### Dependencies missing?
```bash
pip install -r requirements.txt
```

### Permission errors?
Check `data/` folder has read/write permissions

### Still having issues?
See `COMPLETE_VERIFICATION_REPORT.md` or `README.md`

---

## 📁 Project Files

- **app.py** - Main application (Flask server)
- **main.py** - Email processing logic
- **templates/** - HTML pages
- **data/** - Configuration & files
- **tests/** - Test suite
- **RUN_COMPLETE_TESTS.py** - Full testing script
- **START_SERVER.bat** - Quick start (Windows)

---

## ✅ Verification Status

**Status: 🟢 FULLY VERIFIED & READY**

All 9 routes working:
- [x] `/` - Home page
- [x] `/configure` - Settings
- [x] `/about` - Info
- [x] `/documentation` - Docs
- [x] `/api/upload` - Upload
- [x] `/api/download/<id>` - Download
- [x] `/api/status/<id>` - Status check
- [x] `/api/history` - History
- [x] `/api/preview` - Preview

---

## 📞 Quick Help

| Problem | Solution |
|---------|----------|
| Python not found | Install Python 3.8+ and add to PATH |
| Module not found | Run `pip install -r requirements.txt` |
| Port in use | Change port in `app.py` line 590 |
| Settings won't save | Check `data/` folder permissions |
| Templates not found | Ensure `templates/` folder exists |

---

## 🎯 What You Get

✅ **Web Interface**
- Upload emails (drag & drop)
- Real-time conversion
- Batch processing
- ZIP downloading

✅ **Configuration**
- Customize appearance
- Change language
- Upload custom logo
- Save preferences

✅ **Email Formats**
- EML files
- MSG files (Outlook)
- MBOX archives
- ZIP files

✅ **Advanced Features**
- Extraction of attachments
- Multiple page formats
- Character encoding detection
- Session history

---

## 🌐 Network Access

### Local Machine
```
http://localhost:5000
```

### Another Computer (same network)
```
http://YOUR_IP_ADDRESS:5000
```

Replace `YOUR_IP_ADDRESS` with your computer's IP (find with `ipconfig`)

### Remote Access (needs VPN/firewall config)
```
Configure firewall to allow port 5000
Then use http://YOUR_IP:5000
```

---

## 📝 Configuration File

Location: `data/config_dynamic.json`

Default content:
```json
{
    "language": "fr",
    "colors": {
        "primary": "#0088CC",
        "secondary": "#00AA66",
        "accent": "#FFD700",
        "background": "#f5f5f5",
        "text": "#333333"
    },
    "logo_path": null
}
```

Automatically updated when you save settings via `/configure`

---

## 🚀 Commands Cheat Sheet

```bash
# Install dependencies
pip install -r requirements.txt

# Start server
python app.py

# Run tests
python RUN_COMPLETE_TESTS.py

# Run specific test
python -m pytest tests/test_full_suite.py -v

# Check Python version
python --version

# Check installed packages
pip list
```

---

## 💡 Tips & Tricks

**Tip 1:** Access configuration immediately after starting
```
Server starts → Go to /configure → Customize → Saved permanently
```

**Tip 2:** Check upload history anytime
```
API: /api/history
Shows all past conversions
```

**Tip 3:** Use in network
```
Share URL: http://YOUR_IP:5000
Others can access from their computers
```

**Tip 4:** Custom port
```
Edit app.py line 590 to use different port
Then access via http://localhost:NEW_PORT
```

---

## 🔐 Security

- ✅ File size limit: 100 MB
- ✅ Only email files accepted
- ✅ Automatic file cleanup (7 days)
- ✅ Session isolation
- ✅ Error logging
- ✅ Safe filename handling

---

## 📖 Full Documentation

- **COMPLETE_VERIFICATION_REPORT.md** - Detailed verification
- **VERIFICATION_CHECKLIST.md** - What's been checked
- **README.md** - Full documentation
- **DEPLOYMENT_DOCKER.md** - Docker setup
- **DEPLOYMENT_SERVER.md** - Server deployment

---

## 🎯 One-Minute Test

```bash
# 1. Start server
python app.py

# 2. Open browser, visit:
http://localhost:5000

# 3. Go to configure:
http://localhost:5000/configure

# 4. Change a color and save

# 5. Return home - color changed ✅

# Success!
```

---

**Application Status: 🟢 READY TO RUN**

Questions? Check the documentation files or the full README.md

*Last Updated: 2026-02-08*
