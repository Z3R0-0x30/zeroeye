# ZeroEye 👁️  
**Live Pastebin & GitHub Gist Cyber Threat Monitoring Tool**

ZeroEye is a lightweight threat-hunting utility designed to monitor **Pastebin and GitHub Gists in near real time** and detect potential **cyber threats** such as phishing campaigns, malware lures, crypto scams, and leaked data.

It continuously scans newly published public content and flags suspicious indicators using keyword-based detection — helping security researchers and blue teams stay ahead of emerging threats.

---

## 🚀 Features

### 🔴 Live Platform Monitoring
- **Pastebin** – Continuous polling of the public archive
- **GitHub Gists** – Continuous monitoring of newly created public gists
- ⏹️ Graceful stop with **Ctrl+C**
- 🔁 **No duplicate scanning** (already-seen items are skipped)

### 🕵️ Threat Detection Categories
- Phishing & social engineering
- Crypto scams & fake giveaways
- Malware lures & cracked software
- Data leaks & credential dumps

### 🔍 Analysis & Logging
- 🔗 Automatic **URL / IOC extraction**
- 📝 Persistent logging
  - `threat_logs.txt` – Pastebin detections
  - `links.txt` – Pastebin extracted URLs
  - `git_threat_logs.txt` – GitHub Gist detections
  - `git_links.txt` – Gist extracted URLs
- 🎭 **User-Agent randomization** to reduce blocking
- 🧠 Simple, readable Python code (easy to extend)

---

## 📌 How It Works

### Pastebin Flow
1. Fetches the Pastebin **public archive**
2. Extracts paste IDs
3. Filters out previously processed pastes
4. Fetches raw paste content
5. Scans content against multiple threat wordlists
6. Logs and prints alerts when matches are found
7. Repeats continuously

### GitHub Gist Flow
1. Fetches the **public Gist feed**
2. Extracts newly published gist URLs
3. Filters out previously processed gists
4. Fetches raw gist content
5. Scans content against the same threat wordlists
6. Logs and prints alerts when matches are found
7. Repeats continuously

---

## 🛠️ Requirements

- Python **3.8+**
- Internet connection

### Python Dependencies

Install required modules:

```bash
pip install requests beautifulsoup4
```

---

## ▶️ Usage
Run the tool:
```bash
python3 zeroeye.py
```
You will see an interactive menu
```
0. Exit
1. Pastebin
2. Gist
3. Clear logs
4. Help
```

### Live monitoring options
- **Option 1:** Live Pastebin monitoring
- **Option 2:** Live Github Gist monitoring

---

## 📂 Output Files
File                |     Description
threat_logs.txt	          Detected Pastebin threat content
links.txt	                Extracted URLs / IOCs from Pastebin
git_threat_logs.txt	      Detected GitHub Gist threat content
git_links.txt             Extracted URLs / IOCs from Gists

---

## ⚠️ Disclaimer
This tool is intended for educational and defensive security research only.
- ❌ Do NOT use this tool for illegal activity
- ❌ Do NOT scrape aggressively or bypass platform protections
- ⚠️ GitHub and Pastebin enforce rate limits
The author is not responsible for misuse.
Always comply with platform Terms of Service and applicable laws.
