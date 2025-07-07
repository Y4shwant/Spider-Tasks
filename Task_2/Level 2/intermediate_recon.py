#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime

# Import feature modules
from modules import port_scan, tech_detect, email_harvest, shodan_lookup

def banner():
    print("=" * 60)
    print("         Intermediate Recon Toolkit - Level 2")
    print("=" * 60)

def save_report(domain, data, fmt):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/{domain}_report.{fmt}"
    if fmt == "json":
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
    elif fmt == "csv":
        import csv
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Key", "Value"])
            for key, value in data.items():
                writer.writerow([key, value])
    print(f"\n[+] Report saved to {filename}")

def main():
    banner()
    parser = argparse.ArgumentParser(description="Intermediate Recon Toolkit")
    parser.add_argument("domain", help="Target domain (e.g., example.com)")
    parser.add_argument("--ports", action="store_true", help="Enable port scanning & banner grabbing")
    parser.add_argument("--tech", action="store_true", help="Enable technology detection")
    parser.add_argument("--emails", action="store_true", help="Enable email harvesting")
    parser.add_argument("--shodan", action="store_true", help="Enable Shodan lookup")
    parser.add_argument("--output", choices=["json", "csv"], default="json", help="Report format")
    args = parser.parse_args()

    report = {
        "domain": args.domain,
        "scanned_at": datetime.now().isoformat()
    }

    if args.ports:
        report["port_scan"] = port_scan.run(args.domain)
    if args.tech:
        report["technology_detection"] = tech_detect.run(args.domain)
    if args.emails:
        report["email_harvesting"] = email_harvest.run(args.domain)
    if args.shodan:
        report["shodan_lookup"] = shodan_lookup.run(args.domain)

    save_report(args.domain, report, args.output)

if __name__ == "__main__":
    main()
