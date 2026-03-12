import tldextract

ADULT_DOMAINS = [
    "pornhub","xhamster","xnxx","redtube","youporn",
    "sex","adult","xxx","porn","escort","dating"
]

def check_adult_content(url):
    score = 0
    reasons = []

    extracted = tldextract.extract(url)
    domain = extracted.domain.lower()

    # check domain name
    for word in ADULT_DOMAINS:
        if word in domain:
            score += 40
            reasons.append("Adult domain detected")

    # check full URL text
    for word in ADULT_DOMAINS:
        if word in url.lower():
            score += 10
            reasons.append(f"Adult keyword in URL: {word}")

    return score, reasons