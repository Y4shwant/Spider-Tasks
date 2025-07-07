import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

def run(domain):
    print("[+] Scraping Shodan for open services...")
    url = f"https://www.shodan.io/search?query=hostname:{domain}"
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        if response.status_code != 200:
            return {"error": f"Shodan returned status code {response.status_code}"}

        soup = BeautifulSoup(response.text, "html.parser")
        results = []
        # Find each result block
        for result_block in soup.find_all("div", class_="result"):
            ip_port = result_block.find("div", class_="ip")
            data = result_block.find("div", class_="port")
            if ip_port and data:
                ip = ip_port.text.strip()
                port_service = data.text.strip().split("/")
                port = port_service[0] if len(port_service) > 0 else "N/A"
                service = port_service[1] if len(port_service) > 1 else "N/A"
                results.append({
                    "ip": ip,
                    "port": port,
                    "service": service
                })

        return results if results else ["No Shodan results found"]
    except Exception as e:
        return {"error": f"Shodan scraping failed: {str(e)}"}
