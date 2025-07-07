# Basic Recon Automation Tool

This Python script automates basic reconnaissance tasks for a given domain.

## Features
- Subdomain enumeration (crt.sh, Sublist3r)
- DNS records (A, NS, MX)
- WHOIS information
- HTTP headers
- robots.txt and sitemap.xml
- GeoIP lookup
- Outputs results to terminal and `outputs/basic_<domain>.txt`

## Setup
1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
2. Ensure system tools `whois` and `curl` are installed:
    ```bash
    sudo apt install whois curl
    ```

## Usage
```bash
python3 basic_recon.py example.com
