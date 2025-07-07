#!/usr/bin/env python3

import argparse
import requests
import subprocess
import socket
import whois
import dns.resolver
import json
import os
from datetime import datetime

def banner():
    print("=" * 50)
    print("      Basic Recon Automation Tool")
    print("=" * 50)

def save_output(domain, content):
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/basic_{domain}.txt"
    with open(filename, "w") as f:
        f.write(content)
    print(f"\n[+] Results saved to {filename}")

def get_domain():
    parser = argparse.ArgumentParser(description="Find basic information about a domain")
    parser.add_argument("domain", nargs="?", help="Target domain (e.g., example.com)")
    args = parser.parse_args()
    if args.domain:
        return args.domain.strip()
    return input("Enter the domain name (e.g., example.com): ").strip()


def subdomains_crtsh(domain):
    print("[+] Gathering subdomains from crt.sh...")
    try:
        url = f"https://crt.sh/?q=%25.{domain}&output=json"
        resp = requests.get(url, timeout=10)
        data = resp.json()
        subdomains = sorted(set(entry['name_value'] for entry in data))
        return "\n".join(subdomains) if subdomains else "No subdomains found."
    except Exception as e:
        return f"crt.sh lookup failed: {e}"

def subdomains_sublist3r(domain):
    print("[+] Gathering subdomains from Sublist3r...")
    try:
        from sublist3r import main as sublist3r_main
        subdomains = sublist3r_main(domain, 40, None, ports=None, silent=True, verbose=False, enable_bruteforce=False, engines=None)
        return "\n".join(subdomains) if subdomains else "No subdomains found."
    except Exception as e:
        return f"Sublist3r lookup failed: {e}"


def dns_lookup(domain):
    print("[+] Performing DNS lookup...")
    records = ""
    resolver = dns.resolver.Resolver()
    for rtype in ["A", "NS", "MX"]:
        try:
            answers = resolver.resolve(domain, rtype)
            records += f"{rtype} Records:\n" + "\n".join(str(r) for r in answers) + "\n\n"
        except Exception:
            records += f"{rtype} Records: Not found.\n\n"
    return records.strip()

def whois_lookup(domain):
    print("[+] Fetching WHOIS info...")
    try:
        info = whois.whois(domain)
        if info and any(info.values()):
            return str(info)
        else:
            raise ValueError("Empty WHOIS data")
    except Exception as e:
        print("[!] python-whois failed, trying system whois...")
        try:
            result = subprocess.check_output(
                ["whois", domain], stderr=subprocess.STDOUT, text=True
            )
            return result
        except subprocess.CalledProcessError as e2:
            return f"WHOIS lookup failed: {e2.output}"
        except FileNotFoundError:
            return "System 'whois' command not found."


def http_headers(domain):
    print("[+] Fetching HTTP headers...")
    try:
        resp = requests.head(f"http://{domain}", timeout=10, allow_redirects=True)
        return "\n".join(f"{k}: {v}" for k, v in resp.headers.items())
    except Exception as e:
        print("[!] requests failed. Trying curl...")
        try:
            result = subprocess.check_output(["curl", "-I", f"http://{domain}"], stderr=subprocess.STDOUT, text=True)
            return result
        except Exception as e2:
            return f"HTTP header fetch failed: {e2}"

def fetch_file(domain, path):
    print(f"[+] Checking for {path}...")
    try:
        resp = requests.get(f"http://{domain}{path}", timeout=5)
        if resp.status_code == 200:
            return resp.text
        else:
            return f"{path} not found (HTTP {resp.status_code})"
    except Exception as e:
        return f"{path} fetch failed: {e}"


def geoip_lookup(domain):
    print("[+] Performing GeoIP lookup...")
    try:
        ip = socket.gethostbyname(domain)
        resp = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = resp.json()
        return f"{data.get('country', 'Unknown')}, {data.get('regionName', '')}, {data.get('city', '')} (ISP: {data.get('isp', 'N/A')})"
    except Exception as e:
        return f"GeoIP lookup failed: {e}"


def main():
    banner()
    domain = get_domain()
    report = f"=== Basic Recon Report for {domain} ===\nGenerated: {datetime.now()}\n\n"

    report += "--- Subdomains (crt.sh) ---\n" + subdomains_crtsh(domain) + "\n\n"
    report += "--- Subdomains (Sublist3r) ---\n" + subdomains_sublist3r(domain) + "\n\n"
    report += "--- DNS Records ---\n" + dns_lookup(domain) + "\n\n"
    report += "--- WHOIS Info ---\n" + whois_lookup(domain) + "\n\n"
    report += "--- HTTP Headers ---\n" + http_headers(domain) + "\n\n"
    report += "--- robots.txt ---\n" + fetch_file(domain, "/robots.txt") + "\n\n"
    report += "--- sitemap.xml ---\n" + fetch_file(domain, "/sitemap.xml") + "\n\n"
    report += "--- GeoIP Lookup ---\n" + geoip_lookup(domain) + "\n"

    print("\n" + report)
    save_output(domain, report)

if __name__ == "__main__":
    main()
