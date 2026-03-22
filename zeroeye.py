import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
import json
import hashlib
import math
from urllib.parse import urlparse

### GLOBAL STORAGE ###

pasteids = []
git_links = []

seen_paste_ids = set()
seen_gist_links = set()
seen_hashes = set()

### USER AGENTS ###

user_agents = [
'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64)',
]

### SECRET PATTERNS ###

SECRET_PATTERNS = {
"AWS_ACCESS_KEY": r'AKIA[0-9A-Z]{16}',
"GOOGLE_API_KEY": r'AIza[0-9A-Za-z\-_]{35}',
"SLACK_TOKEN": r'xox[baprs]-[0-9a-zA-Z]{10,48}',
"GITHUB_TOKEN": r'gh[pousr]_[A-Za-z0-9]{36}',
"STRIPE_KEY": r'sk_live_[0-9a-zA-Z]{24}',
"PRODUCT_KEY_5X5": r'\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b',
"STEAM_KEY": r'\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b',
"ADOBE_KEY": r'\b[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}-[A-Z0-9]{6}\b',
"OFFICE_KEY": r'\b[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}-[A-Z0-9]{5}\b',
}

CREDENTIAL_PATTERNS = {
"EMAIL_PASSWORD": r'[\w\.-]+@[\w\.-]+\.\w+\s*[:|]\s*\S+',
"PASSWORD_ASSIGN": r'(?i)(password|passwd|pwd)\s*[:=]\s*\S+',
}

PRIVATE_KEY_PATTERNS = {
"RSA_PRIVATE_KEY": r'-----BEGIN RSA PRIVATE KEY-----',
"OPENSSH_KEY": r'-----BEGIN OPENSSH PRIVATE KEY-----',
"PGP_PRIVATE_KEY": r'-----BEGIN PGP PRIVATE KEY BLOCK-----',
}

IOC_PATTERNS = {
"URL": r'https?:\/\/[^\s"]+',
"IP": r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b',
"BTC_WALLET": r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b',
"ETH_WALLET": r'0x[a-fA-F0-9]{40}',
}

### CAMPAIGN DETECTION ###

CAMPAIGN_KEYWORDS = [
"leaked exploit",
"exploit documentation",
"crypto exploit",
"instant swap",
"tested and confirmed",
"verified method",
"cooldown",
"flagged for verification",
"profit",
"made $",
"guaranteed",
"working exploit",
"private exploit",
"exclusive method"
]

SUSPICIOUS_DOCS = [
"docs.google.com",
"drive.google.com",
"mega.nz",
"dropbox.com",
"anonfiles",
"gofile",
"transfer.sh"
]

### CONTEXT KEYWORDS ###

KEYWORDS = [
"vpn","internal","prod","staging","database",
"backup","admin","root","ssh","token","secret"
]

### THREAT SCORING ###

THREAT_SCORES = {
"AWS_ACCESS_KEY": 9,
"GOOGLE_API_KEY": 9,
"SLACK_TOKEN": 8,
"GITHUB_TOKEN": 8,
"STRIPE_KEY": 8,
"EMAIL_PASSWORD": 7,
"PASSWORD_ASSIGN": 6,
"RSA_PRIVATE_KEY": 10,
"OPENSSH_KEY": 10,
"PGP_PRIVATE_KEY": 10,
"BTC_WALLET": 6,
"ETH_WALLET": 6,
"PRODUCT_KEY_5X5": 7,
"STEAM_KEY": 5,
"ADOBE_KEY": 7,
"OFFICE_KEY": 7,
"POSSIBLE_SCAM_CAMPAIGN": 8
}

### UTIL FUNCTIONS ###

def hash_content(data):
    return hashlib.sha256(data.encode()).hexdigest()

def validate_product_key(key):
    raw = key.replace("-", "")

    if not re.match(r'^[A-Z0-9]+$', raw):
        return False

    if len(set(raw)) < 8:
        return False

    if entropy(raw) < 3.5:
        return False

    return True


def entropy(data):

    if not data:
        return 0

    ent = 0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        ent -= p_x * math.log2(p_x)

    return ent


def write_json_log(data):
    with open("threat_dataset.json", "a") as f:
        json.dump(data, f)
        f.write("\n")


def extract_domains(urls):

    domains = []

    for u in urls:
        try:
            parsed = urlparse(u)
            domains.append(parsed.netloc)
        except:
            pass

    return list(set(domains))


def classify_context(text):

    hits = []

    for k in KEYWORDS:
        if k in text.lower():
            hits.append(k)

    if "vpn" in hits or "ssh" in hits:
        return "corporate_access"
    if "database" in hits or "backup" in hits:
        return "data_exposure"
    if "token" in hits or "secret" in hits:
        return "api_secret"
    return "unknown"


def detect_language(text):

    if "import " in text:
        return "python"
    if "function(" in text or "console.log" in text:
        return "javascript"
    if "package.json" in text:
        return "nodejs"
    if "apiVersion:" in text:
        return "kubernetes"
    return "unknown"


def generate_campaign_id(iocs):
    combined = "".join([ioc[1] for ioc in iocs])
    if not combined:
        return None
    return hashlib.md5(combined.encode()).hexdigest()


### CAMPAIGN DETECTOR ###

def detect_campaign(text, iocs):

    score = 0
    text_l = text.lower()

    for k in CAMPAIGN_KEYWORDS:
        if k in text_l:
            score += 2

    for ioc in iocs:
        if ioc[0] == "URL":
            for d in SUSPICIOUS_DOCS:
                if d in ioc[1]:
                    score += 3
    if "made $" in text_l:
        score += 3
    if score >= 6:
        return True
    return False


### ANALYSIS ENGINE ###

def analyze_content(text, source_url, platform):

    findings = []
    iocs = []

    ### SECRET DETECTION ###

    for name, pattern in SECRET_PATTERNS.items():
        matches = re.findall(pattern, text)
        for m in matches:
            findings.append((name, m))


    for name, pattern in CREDENTIAL_PATTERNS.items():
        matches = re.findall(pattern, text)
        for m in matches:
            findings.append((name, m))

    for name, pattern in PRIVATE_KEY_PATTERNS.items():
        if re.search(pattern, text):
            findings.append((name, "PRIVATE_KEY_FOUND"))


    ### IOC EXTRACTION ###

    for name, pattern in IOC_PATTERNS.items():
        matches = re.findall(pattern, text)
        for m in matches:
            iocs.append((name, m))


    ### ENTROPY ###
    words = re.findall(r'[A-Za-z0-9+/=]{20,}', text)

    for w in words:
        if entropy(w) > 4.5:
            findings.append(("HIGH_ENTROPY_STRING", w))


    ### CAMPAIGN DETECTION ###
    if detect_campaign(text, iocs):
        findings.append(("POSSIBLE_SCAM_CAMPAIGN", "social_engineering"))

    ### REGISTRATION KEYS ###
    for name, pattern in SECRET_PATTERNS.items():
        matches = re.findall(pattern, text)
        for m in matches:
            # Extra validation for product keys to reduce false positives
            if name in ("PRODUCT_KEY_5X5", "OFFICE_KEY", "STEAM_KEY", "ADOBE_KEY"):
                if not validate_product_key(m):
                    continue
            findings.append((name, m))

    ### THREAT SCORING ###

    score = 0

    for f in findings:
        score += THREAT_SCORES.get(f[0], 2)

    severity = "LOW"

    if score >= 10:
        severity = "CRITICAL"
    elif score >= 7:
        severity = "HIGH"
    elif score >= 4:
        severity = "MEDIUM"

    domains = extract_domains([ioc[1] for ioc in iocs if ioc[0] == "URL"])
    context = classify_context(text)
    language = detect_language(text)
    campaign = generate_campaign_id(iocs)
    now = datetime.datetime.now()

    return {
        "timestamp": str(now),
        "platform": platform,
        "url": source_url,
        "domains": domains,
        "campaign_id": campaign,
        "context": context,
        "language": language,
        "severity": severity,
        "score": score,
        "findings": findings,
        "iocs": iocs
    }

### BANNER ###

def banner():

    print("""
███████╗███████╗██████╗  ██████╗ ███████╗██╗   ██╗███████╗
╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔════╝╚██╗ ██╔╝██╔════╝
  ███╔╝ █████╗  ██████╔╝██║   ██║█████╗   ╚████╔╝ █████╗
 ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██╔══╝    ╚██╔╝  ██╔══╝
███████╗███████╗██║  ██║╚██████╔╝███████╗   ██║   ███████╗
╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
        ZeroEye Threat Monitor
""")


### PASTEBIN ###

class PasteBIN:
    def __init__(self, url):
        self.url = url

    def grab_pastebinid(self):
        headers = {'User-Agent': random.choice(user_agents)}
        r = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        for link in soup.select('tr td a'):
            href = link.get('href')

            if href:
                pasteids.append(href)

    def grab_comments(self, pasteurl):
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            r = requests.get(pasteurl, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            comment_blocks = soup.select("div.comments")

            for block in comment_blocks:
                lines = []

                # Correct path: div.source > ol > li > div.de1
                for line in block.select("div.source ol li div.de1"):
                    text_line = line.get_text(separator=" ", strip=True)
                    if text_line and text_line.strip() != "\xa0":
                        lines.append(text_line.strip())

                comment_text = "\n".join(lines)

                if not comment_text.strip():
                    continue

                h = hash_content(comment_text)

                if h in seen_hashes:
                    continue

                seen_hashes.add(h)
                analysis = analyze_content(comment_text, pasteurl, "pastebin_comment")

                if analysis["severity"] != "LOW":
                    write_json_log(analysis)
                    print("\n[!] COMMENT THREAT DETECTED")
                    print(json.dumps(analysis, indent=2))

        except Exception as e:
            print("[comment error]", e)

    def grab_raw(self, pasteurls):
        for pasteurl in pasteurls:
            try:
                headers = {'User-Agent': random.choice(user_agents)}
                r = requests.get(pasteurl, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                raw = soup.select_one('a[href^="/raw/"]')
                clean_url = pasteurl.split("?")[0]
                self.grab_comments(clean_url)

                if raw:
                    raw_url = "https://pastebin.com" + raw['href']
                    raw_content = requests.get(raw_url, headers=headers).text
                    h = hash_content(raw_content)
                    if h in seen_hashes:
                        continue

                    seen_hashes.add(h)
                    analysis = analyze_content(raw_content, raw_url, "pastebin")

                    if analysis["severity"] != "LOW":
                        write_json_log(analysis)
                        print("\n[!] THREAT DETECTED")
                        print(json.dumps(analysis, indent=2))
            except:
                continue


### GIST ###

class GistBIN:
    def __init__(self, url):
        self.url = url


    def grab_git(self):
        headers = {'User-Agent': random.choice(user_agents)}
        r = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')
        links = [a['href'] for a in soup.select(".gist-snippet a[href]")]

        for link in links:

            if link.startswith("/"):
                parts = link.strip().split("/")

                if len(parts) == 3:
                    git_links.append(link)


    def grab_comments(self, gist_id):
        try:
            headers = {'User-Agent': random.choice(user_agents)}

            # Scrape the gist page directly instead of using the API
            gist_url = f"https://gist.github.com/{gist_id}#comments"
            r = requests.get(gist_url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            # Filter out known junk paragraphs GitHub injects
            JUNK = {
                "sorry, something went wrong.",
                "there was an error while loading.please reload this page.",
                "there was an error while loading. please reload this page.",
            }

            paragraphs = soup.find_all('p')

            for p in paragraphs:
                text = p.get_text(strip=True)

                if not text:
                    continue

                # Skip GitHub error/noise paragraphs
                if text.lower() in JUNK:
                    continue

                h = hash_content(text)

                if h in seen_hashes:
                    continue

                seen_hashes.add(h)
                analysis = analyze_content(text, gist_url, "gist_comment")

                if analysis["severity"] != "LOW":
                    write_json_log(analysis)
                    print("\n[!] GIST COMMENT THREAT DETECTED")
                    print(json.dumps(analysis, indent=2))

        except Exception as e:
            print("[gist comment error]", e)


    def grab_raw(self, gitlinks):
        for link in gitlinks:
            try:
                url = self.url + link
                headers = {'User-Agent': random.choice(user_agents)}
                r = requests.get(url, headers=headers)
                soup = BeautifulSoup(r.content, 'html.parser')
                raw = soup.find('a', href=lambda h: h and "/raw" in h)

                # link is like /username/gist_id — pass the full path
                gist_path = link.strip("/")  # "username/gist_id"
                self.grab_comments(gist_path)

                if raw:
                    raw_url = self.url + raw['href']
                    raw_content = requests.get(raw_url, headers=headers).text
                    h = hash_content(raw_content)

                    if h in seen_hashes:
                        continue

                    seen_hashes.add(h)
                    analysis = analyze_content(raw_content, raw_url, "gist")

                    if analysis["severity"] != "LOW":
                        write_json_log(analysis)
                        print("\n[!] THREAT DETECTED")
                        print(json.dumps(analysis, indent=2))
            except:
                continue


### MAIN ###

def main():
    banner()
    while True:
        print("""
1. Monitor Pastebin
2. Monitor Gist
0. Exit
""")
        choice = input("[zero]~$ ")

        if choice == "0":
            exit()

        elif choice == "1":
            monitor = PasteBIN("https://pastebin.com/archive")
            print("[+] Monitoring Pastebin...")

            while True:
                monitor.grab_pastebinid()
                new_ids = [pid for pid in pasteids if pid not in seen_paste_ids]

                if new_ids:
                    urls = ['https://pastebin.com' + pid for pid in new_ids]
                    monitor.grab_raw(urls)
                    seen_paste_ids.update(new_ids)

                time.sleep(15)

        elif choice == "2":
            monitor = GistBIN("https://gist.github.com")
            print("[+] Monitoring Gist...")

            while True:
                monitor.grab_git()
                new = [g for g in git_links if g not in seen_gist_links]

                if new:
                    monitor.grab_raw(new)
                    seen_gist_links.update(new)

                time.sleep(20)

if __name__ == "__main__":
    main()
