import re
import whois
import datetime
import requests
import math
from urllib.parse import urlparse

# suspicious phishing keywords
SUSPICIOUS_WORDS = [
    "login","verify","update","bank","secure",
    "account","free","bonus","win","password",
    "confirm","click","urgent","support","help",
    "service","webscr","paypal","ebay","amazon","apple","google","microsoft"
]

SUSPICIOUS_TLDS = ["tk","ml","ga","cf","xyz","top","work",
                   "click","online","site","club","info","biz",
                   "pw","icu","loan","win","date","review",
                   "gq","cf","ga","ml","tk"]

SHORTENERS = [
    "bit.ly","tinyurl","goo.gl","t.co","rebrand.ly",
    "cutt.ly","shorturl","ow.ly","is.gd",
    "buff.ly","adf.ly","bit.do","shorte.st","tr.im"
]

BRANDS = [
    "google","paypal","amazon","facebook",
    "instagram","bank","apple","microsoft",
    "netflix","twitter","linkedin","ebay",
    "dropbox","spotify","airbnb","uber",
    "zoom","slack","github","gitlab","bitbucket"
]

import math
from collections import Counter

def calculate_entropy(text):

    if not text:
        return 0

    length = len(text)
    counts = Counter(text)

    entropy = 0

    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)

    return entropy

def check_url_risk(url):
    score = 0
    reasons = []

    parsed = urlparse(url)

    # 1️⃣ Check HTTPS
    if parsed.scheme != "https":
        score += 20
        reasons.append("Website not using HTTPS")

    # 2️⃣ Check URL length
    if len(url) > 75:
        score += 15
        reasons.append("URL is too long")

    # 3️⃣ Check IP address in URL
    if re.match(r"\d+\.\d+\.\d+\.\d+", parsed.netloc):
        score += 25
        reasons.append("URL uses IP address instead of domain")

    # 4️⃣ Suspicious words in URL
    for word in SUSPICIOUS_WORDS:
        if word in url.lower():
            score += 10
            reasons.append(f"Suspicious keyword found: {word}")
            # 5️⃣ Multiple subdomains
    if parsed.netloc.count('.') > 3:
        score += 20
        reasons.append("Too many subdomains (phishing pattern)")

    # 6️⃣ '@' symbol trick
    if "@" in url:
        score += 30
        reasons.append("Contains @ symbol (phishing trick)")

    # 7️⃣ Double slash trick
    if url.count("//") > 1:
        score += 15
        reasons.append("Multiple // detected")

    # 8️⃣ Too many hyphens
    if parsed.netloc.count('-') > 2:
        score += 15
        reasons.append("Too many hyphens in domain")

    # 9️⃣ Suspicious TLD
    tld = parsed.netloc.split('.')[-1]
    if tld in SUSPICIOUS_TLDS:
        score += 25
        reasons.append(f"Suspicious domain extension: .{tld}")

        # URL shortener detection
    for short in SHORTENERS:
        if short in url:
            score += 30
            reasons.append("URL shortener used (common phishing trick)")

    return score, reasons

def check_domain_reputation(url):
    score = 5   # small baseline risk
    reasons = ["Internet baseline risk"]

    try:
        domain_info = whois.whois(url)
        creation_date = domain_info.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            age_days = (datetime.datetime.now() - creation_date).days

            # NEW DOMAIN = BIG RISK
            if age_days < 180:
                score += 40
                reasons.append("Very new domain (possible phishing)")

            elif age_days < 365:
                score += 20
                reasons.append("Recently registered domain")

            else:
                score -= 5
                reasons.append("Old trusted domain")

    except:
        # WHOIS hidden is normal → do NOT add risk
        reasons.append("WHOIS privacy enabled")

    return max(score,0), reasons
def check_brand_impersonation(url):
    score = 0
    reasons = []

    lowered = url.lower()

    SUSPICIOUS_BRAND_WORDS = [
        "login","secure","verify","account","update","bank","signin"
    ]

    for brand in BRANDS:
        if brand in lowered:
            # Check if suspicious word also exists
            for word in SUSPICIOUS_BRAND_WORDS:
                if word in lowered:
                    score += 40
                    reasons.append(f"Possible {brand} phishing page")
                    break

        # character swap detection (g00gle, paypa1)
        fake_versions = [
            brand.replace("o","0"),
            brand.replace("l","1"),
            brand.replace("a","@"),
            brand.replace("e","3")
        ]

        for fake in fake_versions:
            if fake in lowered and fake != brand:
                score += 50
                reasons.append(f"Brand impersonation detected ({brand})")

    return score, reasons
def check_redirects(url):
    score = 0
    reasons = []

    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        redirects = len(response.history)

        if redirects > 2:
            score += 20
            reasons.append(f"Multiple redirects ({redirects})")

        # compare main domain only (ignore www)
        def get_domain(u):
            return u.replace("https://","").replace("http://","").split("/")[0].replace("www.","")

        original_domain = get_domain(url)
        final_domain = get_domain(response.url)

        if original_domain != final_domain:
            score += 30
            reasons.append("Redirects to different domain")

    except:
        score += 10
        reasons.append("Unable to verify redirects")

    return score, reasons


def check_url_entropy(url):
    score = 0
    reasons = []

    domain = url.split("//")[-1].split("/")[0]
    entropy = calculate_entropy(domain)

    if entropy > 4.0:
        score += 30
        reasons.append("Domain looks randomly generated")

    elif entropy > 3.5:
        score += 15
        reasons.append("Domain has unusual randomness")

    return score, reasons