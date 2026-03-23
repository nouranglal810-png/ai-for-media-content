"""
Shared trusted domains list used by all analysis engines.
"""
import tldextract

# ── Trusted registered domains (any subdomain is auto-trusted) ──
KNOWN_LEGIT_DOMAINS = [
    # Big Tech
    "google.com", "google.co.in", "google.co.uk", "google.co.jp",
    "youtube.com", "gmail.com",
    "microsoft.com", "live.com", "outlook.com", "office.com", "bing.com",
    "apple.com", "icloud.com",
    "facebook.com", "meta.com",
    "instagram.com",
    "twitter.com", "x.com",
    "linkedin.com",
    "amazon.com", "amazon.in", "amazon.co.uk", "amazon.co.jp",
    "github.com", "gitlab.com", "bitbucket.org",

    # Popular Services
    "wikipedia.org", "wikimedia.org", "wiktionary.org",
    "reddit.com",
    "netflix.com",
    "spotify.com",
    "whatsapp.com",
    "telegram.org",
    "discord.com",
    "zoom.us",
    "slack.com",
    "paypal.com",
    "ebay.com",
    "dropbox.com",
    "airbnb.com",
    "uber.com",
    "pinterest.com",
    "tumblr.com",
    "quora.com",
    "medium.com",
    "stackoverflow.com", "stackexchange.com",
    "twitch.tv",

    # E-Commerce
    "flipkart.com",
    "myntra.com",
    "snapdeal.com",
    "meesho.com",
    "ajio.com",
    "nykaa.com",
    "jiomart.com",
    "tatacliq.com",
    "shopify.com",
    "walmart.com",
    "aliexpress.com",
    "alibaba.com",

    # News & Media
    "bbc.com", "bbc.co.uk",
    "cnn.com",
    "nytimes.com",
    "reuters.com",
    "forbes.com",
    "theguardian.com",
    "washingtonpost.com",
    "ndtv.com",
    "aajtak.in",
    "thehindu.com",
    "hindustantimes.com",
    "indianexpress.com",
    "news18.com",
    "aljazeera.com",
    "imdb.com",

    # Education
    "khanacademy.org",
    "coursera.org",
    "udemy.com",
    "edx.org",
    "w3schools.com",
    "geeksforgeeks.org",
    "leetcode.com",
    "hackerrank.com",
    "codechef.com",
    "codeforces.com",
    "freecodecamp.org",

    # Tools & Productivity
    "notion.so",
    "figma.com",
    "canva.com",
    "trello.com",
    "adobe.com",
    "cloudflare.com",
    "vercel.com",
    "netlify.com",

    # Finance & Banking (India)
    "onlinesbi.sbi",
    "hdfcbank.com",
    "icicibank.com",
    "axisbank.com",
    "kotak.com",
    "paytm.com",
    "phonepe.com",

    # Finance & Banking (Global)
    "chase.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "hsbc.com",

    # Search & Browsers
    "yahoo.com",
    "duckduckgo.com",
    "brave.com",
    "mozilla.org",
    "opera.com",

    # Indian Government
    "india.gov.in",
    "mygov.in",
    "digitalindia.gov.in",
    "uidai.gov.in",
    "incometax.gov.in",
    "irctc.co.in",
    "digilocker.gov.in",
    "npci.org.in",

    # International Government
    "usa.gov",
    "nasa.gov",
    "nih.gov",
    "cdc.gov",
    "gov.uk",
    "un.org",
    "who.int",
    "worldbank.org",
]

# ── Trusted TLD suffixes ──
TRUSTED_GOVT_TLDS = [
    "gov.in", "gov.uk", "gov.us", "gov.au", "gov.ca", "gov.sg",
    "gov", "mil",
    "ac.in", "edu.in", "res.in",
    "edu", "ac.uk", "ac.jp",
    "nic.in",
]


def is_domain_trusted(url):
    """Check if a URL belongs to a trusted domain."""
    ext = tldextract.extract(url)
    registered_domain = f"{ext.domain}.{ext.suffix}".lower()

    # 1) Exact registered domain match
    if registered_domain in KNOWN_LEGIT_DOMAINS:
        return True

    # 2) Check if TLD is a trusted government/educational suffix
    suffix = ext.suffix.lower()
    for trusted_tld in TRUSTED_GOVT_TLDS:
        if suffix == trusted_tld or suffix.endswith("." + trusted_tld):
            return True

    return False
