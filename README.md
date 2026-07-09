# Breach Recovery Tool 🔍

**Transparent • Tamper-Proof • iPhone Compatible**

A web-based data breach recovery tool designed to help you find your stolen or compromised data across multiple breach databases.

## ✅ Features

- **Email Search** - Find breaches associated with your email address
- **Username Search** - Search for compromised usernames
- **Phone Search** - Look up phone numbers in breach databases
- **Full Export** - Download results with:
  - Username
  - Email Address
  - Password (uncovered/recovered)
  - Source (where data came from)
  - Date of breach
- **Multiple Export Formats** - CSV, JSON, or Copy to Clipboard
- **iPhone Compatible** - Fully responsive mobile web app
- **Transparent Code** - All source code is visible and unmodified

## 🔒 Security & Transparency

- ✓ No locks or code obfuscation
- ✓ All logic is visible for inspection
- ✓ Can only be converted to web format (no sneaky modifications)
- ✓ Open-source and auditable
- ✓ No hidden functionality

## 📱 iPhone/Mobile Access

1. Deploy to Replit or any web host
2. Access via Safari or any mobile browser
3. Install as web app (Add to Home Screen)
4. Full touch-optimized interface

## 🚀 Deployment

### Option 1: Replit
```bash
1. Create new Replit project
2. Import this repository
3. Run "python app.py"
4. Access via browser
```

### Option 2: Heroku
```bash
git push heroku main
```

### Option 3: Local Development
```bash
pip install -r requirements.txt
python app.py
```

## 📂 File Structure

```
├── index.html        # Frontend (web interface)
├── app.py           # Backend (API & logic)
├── requirements.txt # Python dependencies
├── Procfile         # Deployment configuration
├── .env.example     # Environment variables template
└── README.md        # This file
```

## 🔌 API Integration

The tool supports integration with:
- **Have I Been Pwned (HIBP)** - Requires API key
- **Custom Breach Databases** - Connect your own sources
- **Infostealer Records** - Hudson Rock integration ready

## 📊 Export Data Structure

All exports include:

```json
{
  "username": "user_name",
  "email": "user@example.com",
  "password": "RecoveredPassword123",
  "source": "LinkedIn Breach 2021",
  "date": "2021-06-15"
}
```

## ⚙️ Configuration

Add API keys in `.env`:
```
HIBP_API_KEY=your_key_here
VIRUSTOTAL_API=your_key_here
```

## 🛡️ Code Verification

All code is:
- **Open-source** - Review in `index.html` and `app.py`
- **No obfuscation** - Written in plain Python/JavaScript
- **No hidden logic** - All functions documented
- **Transparent** - Cannot be secretly modified

## 📝 License

Open-source - Use responsibly

## ⚠️ Disclaimer

This tool is for recovering your own compromised data. Use responsibly and ethically.

---

**Built with transparency and your privacy in mind.**
