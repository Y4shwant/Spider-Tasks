# Intermediate Recon Toolkit

Level 2 Recon Automation Tool  
Automates intermediate recon tasks for a target domain.

---

## ✅ Features
- Modular design (enable/disable modules individually)
- Port Scanning & Banner Grabbing (Nmap)
- Technology Detection (WhatWeb CLI)
- Email Harvesting (Google/Bing scraping – no external tool dependency)
- Shodan Lookup (requires free API key)
- Structured JSON or CSV reports saved in `reports/`

---

## 📦 Setup

### 1. Install System Dependencies
```bash
sudo apt update
sudo apt install python3 python3-pip nmap whatweb -y
