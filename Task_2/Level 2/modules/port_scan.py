import nmap

def run(domain):
    print("[+] Running port scan with Nmap...")
    nm = nmap.PortScanner()
    result = {}
    try:
        nm.scan(domain, arguments="-T4 -F --script=banner")
        for host in nm.all_hosts():
            result[host] = {}
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                result[host][proto] = {}
                for port in ports:
                    service = nm[host][proto][port]
                    result[host][proto][port] = {
                        "state": service['state'],
                        "name": service['name'],
                        "banner": service.get('script', {}).get('banner', 'N/A')
                    }
    except Exception as e:
        return {"error": str(e)}
    return result
