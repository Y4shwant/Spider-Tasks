import subprocess

def run(domain):
    print("[+] Detecting technologies using WhatWeb...")
    try:
        result = subprocess.run(
            ["whatweb", domain, "--colour=never"],
            capture_output=True, text=True, check=True
        )
        # Example output: example.com [HTTPServer] [X-Powered-By]
        return {"raw_output": result.stdout.strip()}
    except FileNotFoundError:
        return {"error": "WhatWeb not installed. Install it with 'sudo gem install whatweb'."}
    except subprocess.CalledProcessError as e:
        return {"error": f"WhatWeb failed: {e}"}
