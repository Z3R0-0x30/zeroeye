# ZeroEye 👁️  
**Live Pastebin Cyber Threat Monitoring Tool**

ZeroEye is a lightweight threat-hunting utility designed to monitor **Pastebin in near-real time** and detect potential **cyber threats** such as phishing campaigns, malware lures, crypto scams, and leaked data.

It continuously scans newly published public pastes and flags suspicious content using keyword-based detection, helping security researchers and threat hunters stay ahead of emerging threats.

---

## 🚀 Features

- 🔴 **Live Pastebin monitoring** (polls the Pastebin archive continuously)
- ⏹️ **Graceful stop with Ctrl+C**
- 🔁 **No duplicate scanning** (already-seen pastes are skipped)
- 🕵️ **Threat detection categories**
  - Phishing & social engineering
  - Crypto scams
  - Malware lures
  - Data leaks & credential dumps
- 🔗 **Automatic URL extraction**
- 📝 **Persistent logging**
  - `threat_logs.txt` – detected threat content
  - `links.txt` – extracted URLs / IOCs
- 🎭 **User-Agent randomization** to reduce blocking
- 🧠 Simple, readable Python code (easy to extend)

---

## 📌 How It Works

1. Fetches the Pastebin **public archive**
2. Extracts paste IDs
3. Filters out previously processed pastes
4. Fetches raw paste content
5. Scans content against multiple threat wordlists
6. Logs and prints alerts when matches are found
7. Repeats until the user stops execution

---

## 🛠️ Requirements

- Python **3.8+**
- Internet connection

### Python Dependencies

Install required modules:

```bash
pip install requests beautifulsoup4
```

## ▶️ Usage

```bash
python zeroeye.py
```
You’ll see an interactive menu:
```bash
1. Pastebin
2. Clear logs
3. Help
0. Exit
```
**Start Live Monitoring**
Choose option **1** to begin real-time Pastebin scanning.

---

## 📂 Output Files

File	          Description
threat_logs.txt	Logged threat content with timestamps
links.txt	      Extracted URLs / indicators of compromise

---

## ⚠️ Disclaimer
This tool is intended for educational and defensive security research only.
- Do NOT use this tool for illegal activity
- Do NOT scrape aggressively or bypass platform protections
- The author is not responsible for misuse
Always comply with Pastebin’s Terms of Service and applicable laws.

---

## 🧩 Future Improvements
- Persistent state across restarts
- Threat scoring and confidence levels
- Regex-based detection
- IOC export (JSON / CSV / STIX)
- Multi-platform monitoring (GitHub Gists, Telegram, etc.)
- Async or threaded scanning
