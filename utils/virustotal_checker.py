import requests
import base64

API_KEY = "PASTE_YOUR_API_KEY_HERE4ddb44fd4d199092cdc225dcb4d09b351b83cd4ec9599d9cb4a1e455e1f05822"

def check_virustotal(url):
    score = 0
    reasons = []
    vt_stats = {"malicious":0,"suspicious":0,"harmless":0}

    try:
        url_bytes = url.encode("utf-8")
        url_id = base64.urlsafe_b64encode(url_bytes).decode().strip("=")

        vt_url = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {"x-apikey": API_KEY}

        response = requests.get(vt_url, headers=headers)
        data = response.json()

        stats = data["data"]["attributes"]["last_analysis_stats"]
        vt_stats = stats

        if stats["malicious"] > 0:
            score += 50
            reasons.append("VirusTotal engines flagged as malicious")

        elif stats["suspicious"] > 0:
            score += 25
            reasons.append("VirusTotal engines flagged as suspicious")

        else:
            reasons.append("VirusTotal found no threats")

    except:
        reasons.append("VirusTotal check unavailable")

    return score, reasons, vt_stats