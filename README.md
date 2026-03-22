# 👁️ ZeroEye

### Large-Scale OSINT Monitoring for Credential Leaks & Phishing Detection

---

## 🚀 Overview

**ZeroEye** is an automated threat intelligence tool designed to monitor public paste platforms (e.g., Pastebin) for **credential leaks, phishing indicators, and adversarial infrastructure signals** in real time.

It leverages a combination of **pattern-based detection, heuristic analysis, and OSINT techniques** to identify sensitive data exposure and malicious activity at scale.

---

## ⚡ Features

* 🔍 **Real-time Paste Monitoring**

  * Continuously scrapes public paste platforms

* 🔐 **Credential Leak Detection**

  * Detects exposed:

    * Emails / usernames
    * Passwords
    * API keys / tokens

* 🎣 **Phishing Indicator Detection**

  * Identifies:

    * Suspicious URLs
    * Fake login pages
    * Credential harvesting patterns

* 🧠 **Heuristic + Pattern Matching Engine**

  * Regex-based + contextual detection

* 🌐 **Adversarial Infrastructure Analysis**

  * Extracts domains, IPs, and endpoints used by attackers

* 📊 **Structured Output**

  * JSON / logs for further analysis

* ⚙️ **Modular Design**

  * Easily extend detection modules

---

## 🛠️ Tech Stack

* **Python 3**
* `requests` / `aiohttp`
* `BeautifulSoup4`
* Regex engine
* Optional: threat intel APIs

---

## 📦 Installation

```bash
git clone https://github.com/Z3R0space/zeroeye.git
cd zeroeye
pip3 install -r requirements.txt
```

---

## ▶️ Usage

```bash
python3 zeroeye.py
```

---

## 📁 Project Structure

```
zeroeye/
│── zeroeye.py
│── requirements.txt
│── README.md
```

---

## 🧪 Example Output

```json
{
  "timestamp": "2026-03-20 11:58:21.405639",
  "platform": "gist_comment",
  "url": "https://gist.github.com/<git-id>/<gist-id>",
  "domains": [],
  "campaign_id": null,
  "context": "unknown",
  "language": "unknown",
  "severity": "CRITICAL",
  "score": 13,
  "findings": [
    [
      "EMAIL_PASSWORD",
      "[email]: <password>"
    ],
    [
      "PASSWORD_ASSIGN",
      "password"
    ]
  ],
  "iocs": [URLs, IPs, APIs]
}
```

---

## ⚠️ Disclaimer

This tool is intended for **educational and defensive cybersecurity purposes only**.

* Do NOT use ZeroEye for unauthorized monitoring or data collection
* Respect platform terms of service
* Use responsibly in accordance with applicable laws

---

## 🧠 Use Cases

* Threat intelligence gathering
* SOC monitoring
* Red team reconnaissance
* Security research
* Credential exposure tracking

---

## 🗺️ Roadmap

* [ ] Machine Learning-based classification
* [ ] Telegram / Discord alerts
* [ ] Dashboard UI
* [ ] Multi-source ingestion (GitHub, forums, dark web)
* [ ] IOC enrichment (VirusTotal, AbuseIPDB)

---

## 📜 License

MIT License

---

## 👤 Author

**Prince A. Patel**
Cybersecurity Researcher | OSINT | Exploit Development

---

## ⭐ Support

If you find this project useful, consider giving it a ⭐ on GitHub!
