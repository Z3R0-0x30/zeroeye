# Import necessary modules
import requests
from bs4 import BeautifulSoup
import re
import time
import datetime
import random
import os 

# Declare variables, not war
pasteids = []
paste_urls = []
raw_links = []
content_links = []
seen_paste_ids = set()

# Shared headers (avoid recreating dict every request)
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
]

### WORDLISTS ###

HIGH_RISK_PHRASES = [
    "instant money", "guaranteed profit", "risk free", "no risk",
    "limited time offer", "act now", "urgent action required",
    "your account will be closed", "verify your account",
    "confirm your identity", "suspended account",
    "unauthorized login", "security alert",
    "unusual activity detected", "click the link below",
    "download the attachment", "reset your password",
    "free crypto", "instant crypto", "double your crypto",
    "airdrop reward", "claim your reward", "exclusive offer",
    "leaked database", "database dump", "credentials leaked",
    "private data exposed",
]

CRYPTO_SCAM_WORDS = [
    "crypto giveaway", "btc giveaway", "eth giveaway",
    "send and receive", "double your coins",
    "investment opportunity", "high yield",
    "guaranteed returns", "passive income",
    "staking rewards", "mining bonus",
    "wallet verification", "seed phrase",
    "private key", "connect your wallet",
    "smart contract reward", "airdrop claim",
]

MALWARE_LURE_WORDS = [
    "cracked version", "free download", "license bypass",
    "key generator", "keygen", "activation patch",
    "破解版", "full version unlocked",
    "no activation required", "premium unlocked",
    "mod apk", "installer package",
    "payload", "executable file",
]

DATA_LEAK_SCAM_WORDS = [
    "leaked", "leaked database", "leaked passwords",
    "credential dump", "data breach", "user dump",
    "account list", "email password combo",
    "fullz", "combo list", "sql dump", "exposed records",
]

SOCIAL_ENGINEERING_WORDS = [
    "law enforcement", "tax department", "irs notice",
    "legal action", "court order", "final warning",
    "immediate response required", "failure to comply",
    "account under review", "compliance required",
    "this is not a scam",
]

EMOTIONAL_TRIGGER_WORDS = [
    "congratulations", "you have been selected", "winner",
    "exclusive", "once in a lifetime", "don't miss out",
    "last chance", "act fast", "only today",
]

### FUNCTIONS ###

def banner():
    R, G, B = 146, 255, 12
    print(f'''\033[38;2;{R};{G};{B}m
    ███████╗███████╗██████╗  ██████╗ ███████╗██╗   ██╗███████╗
    ╚══███╔╝██╔════╝██╔══██╗██╔═══██╗██╔════╝╚██╗ ██╔╝██╔════╝
      ███╔╝ █████╗  ██████╔╝██║   ██║█████╗   ╚████╔╝ █████╗  
     ███╔╝  ██╔══╝  ██╔══██╗██║   ██║██╔══╝    ╚██╔╝  ██╔══╝  
    ███████╗███████╗██║  ██║╚██████╔╝███████╗   ██║   ███████╗
    ╚══════╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚══════╝
    BY Z3R0!
    ----------------------------------------------------------
    Options:
    0. Exit
    1. Pastebin
    2. Clear logs
    3. help

          \033[0m''')

def helpme():
    print(f'''\033[38;2;146;255;12m\n
        ZeroEye is a program to monitor public platforms to identify live cyber threats - Which makes a threat hunter's life simpler!
        Options:
        1. Pastebin - Monitor pastebin platform and detect live cyber threats (phishing campaigns, malware campaign or data breaches)
        2. Clear logs - Removes the log files (links.txt & threat_logs.txt)
        3. help - prints this menu

    \033[0m''')

def grab_pastebinid(url):
    global pasteids
    try:
        chosen_user_agent = random.choice(user_agents)
        headers = {
            'User-Agent': chosen_user_agent
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        local_ids = []

        for link in soup.select('tr td a'):
            href = link.get('href')
            if href:
                local_ids.append(href)

        pasteids.extend(local_ids)

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def grab_pasteurl(pasteids_list):
    global paste_urls
    paste_urls.extend(['https://pastebin.com' + pid for pid in pasteids_list])

def grab_links(content):
    global content_links
    if 'http' in content:
        URL_PATTERN = r'https?://\S+'
        content_links = re.findall(URL_PATTERN, content)
        with open("links.txt",'a') as f:
            for link in content_links:
                f.write(f">>> {link}\n\n")

def write_logs(content):
    with open("threat_logs.txt","a") as f:
        f.write(content)

def remove_logs(file1, file2):
    try:
        os.remove(file1)
        os.remove(file2)
        print(f"\033[38;2;146;255;12mFile {file1} has been removed...\033[0m")
        print(f"\033[38;2;146;255;12mFile {file2} has been removed...\033[0m")
    except FileNotFoundError:
        print(f"Following files does not exist: {file1} & {file2}")
    except PermissionError:
        print(f"Invalid permissions in following files: {file1} & {file2}")
    except Exception as e:
        print(f"Error occurred: {e}")


def grab_raw(pasteurls):
    global raw_links
    global HEADERS

    for pasteurl in pasteurls:
        try:
            chosen_user_agent = random.choice(user_agents)
            headers = {
                'User-Agent': chosen_user_agent
            }

            response = requests.get(pasteurl, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            for a in soup.select('a[href^="/raw/"]'):
                raw_link = 'https://pastebin.com' + a['href']
                response = requests.get(raw_link, headers=headers)
                response.raise_for_status()

                soup = BeautifulSoup(response.content, 'html.parser')
                soup_text = str(soup)
                soup_lower = soup_text.lower()

                for word in HIGH_RISK_PHRASES:
                    if word in soup_lower:
                        content = "\n===== HIGH RISK ALERT =====\n" + str(datetime.datetime.now()) + "\n" + "Rank link: " + raw_link + "\n" + soup_text + "\n"
                        write_logs(content)
                        print("\033[31m===== HIGH RISK ALERT =====\n", soup_text, "\n", "=" * 20, "\033[0m")
                        grab_links(soup_text)

                for word in CRYPTO_SCAM_WORDS:
                    if word in soup_lower:
                        content = "\n===== CRYPT SCAM ALERT =====\n" + str(datetime.datetime.now()) + "\n" + "Rank link: " + raw_link + "\n" + soup_text + "\n"
                        write_logs(content)
                        print("\033[31m===== CRYPT SCAM ALERT =====\n", soup_text, "\n", "=" * 20, "\033[0m")
                        grab_links(soup_text)

                for word in MALWARE_LURE_WORDS:
                    if word in soup_lower:
                        content = "\n===== MALWARE SCAM ALERT =====\n" + str(datetime.datetime.now()) + "\n" + "Rank link: " + raw_link + "\n" + soup_text + "\n"
                        write_logs(content)
                        print("\033[31m===== MALWARE SCAM ALERT =====\n", soup_text, "\n", "=" * 20, "\033[0m")
                        grab_links(soup_text)

                for word in DATA_LEAK_SCAM_WORDS:
                    if word in soup_lower:
                        content = "\n===== DATA LEAK ALERT =====\n" + str(datetime.datetime.now()) + "\n" + "Rank link: " + raw_link + "\n" + soup_text + "\n"
                        write_logs(content)
                        print("\033[31m===== DATA LEAK ALERT =====\n", soup_text, "\n", "=" * 20, "\033[0m")
                        grab_links(soup_text)

                for word in SOCIAL_ENGINEERING_WORDS:
                        content = "\n===== SOCIAL ENGINEERING ALERT =====\n" + str(datetime.datetime.now()) + "\n" + "Rank link: " + raw_link + "\n" + soup_text + "\n"
                        write_logs(content)
                        print("\033[31m===== SOCIAL ENGINEERING ALERT =====\n", soup_text, "\n", "=" * 20, "\033[0m")
                        grab_links(soup_text)

        except requests.exceptions.RequestException:
            continue

### MAIN ###

def main():
    banner()
    while True:
        choice0 = int(input(f"\033[38;2;146;255;12m[zero]~$ \033[0m"))
        if choice0 == 0:
            exit()
        elif choice0 == 1:
            URL = "https://pastebin.com/archive"
            print("\033[38;2;146;255;12m[+] Live Pastebin monitoring started (Ctrl+C to stop)\033[0m")
            try:
                while True:
                    grab_pastebinid(URL)

                    # gets only new paste ids
                    new_paste_ids = [pid for pid in pasteids if pid not in seen_paste_ids]
                    if new_paste_ids:
                        grab_pasteurl(new_paste_ids)
                        grab_raw(['https://pastebin.com' + pid for pid in new_paste_ids])
                        seen_paste_ids.update(new_paste_ids)
                    time.sleep(15)  # polling interval (important)
            except KeyboardInterrupt:
                print("\n\033[31m[!] Monitoring stopped by user (Ctrl+C)\033[0m")
        elif choice0 == 2:
            remove_logs("links.txt","threat_logs.txt")
        elif choice0 == 3:
            helpme()
        else:
            print("\033[31mInvalid Option\033[0m")

main()