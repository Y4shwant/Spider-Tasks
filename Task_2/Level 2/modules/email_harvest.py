import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def scrape_search_engine(query, pages=2):
    emails = set()
    for page in range(pages):
        url = f"https://www.google.com/search?q={query}&start={page*10}"
        try:
            response = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(response.text, "html.parser")
            for link in soup.find_all("a"):
                href = link.get("href")
                if href and "http" in href:
                    try:
                        page_resp = requests.get(href, headers=HEADERS, timeout=10)
                        emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@" + re.escape(query.split('@')[-1]), page_resp.text, re.I))
                    except requests.RequestException:
                        continue
        except requests.RequestException:
            continue
    return emails

def run(domain):
    print(f"[+] Harvesting emails for {domain}...")
    emails = set()

    # Google
    print("  [-] Searching Google...")
    emails.update(scrape_search_engine(f"@{domain}"))

    # Bing
    print("  [-] Searching Bing...")
    bing_url = f"https://www.bing.com/search?q=%40{domain}"
    try:
        response = requests.get(bing_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        emails.update(re.findall(r"[a-zA-Z0-9._%+-]+@" + re.escape(domain), soup.text, re.I))
    except requests.RequestException:
        pass

    if emails:
        return list(emails)
    else:
        return ["No emails found"]
