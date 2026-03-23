from flask import Flask, render_template, request, jsonify, send_file
import tldextract

from utils.url_checker import (
    check_url_risk,
    check_domain_reputation,
    check_brand_impersonation,
    check_redirects,
    check_url_entropy
)

from utils.adult_checker import check_adult_content
from utils.ml_checker import check_ml_phishing
from utils.virustotal_checker import check_virustotal
from utils.report_generator import generate_report

app = Flask(__name__)

# Enable CORS so index.html can work even when opened directly as a file
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

# ── Trusted registered domains (any subdomain is auto-trusted) ──
TRUSTED_DOMAINS = [
    # ─── Big Tech ───
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

    # ─── Popular Services ───
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

    # ─── E-Commerce (India & Global) ───
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

    # ─── News & Media ───
    "bbc.com", "bbc.co.uk",
    "cnn.com",
    "nytimes.com",
    "reuters.com",
    "forbes.com",
    "theguardian.com",
    "washingtonpost.com",
    "ndtv.com",
    "aajtak.in",
    "timesofindia.indiatimes.com",
    "thehindu.com",
    "hindustantimes.com",
    "indianexpress.com",
    "news18.com",
    "abcnews.go.com",
    "aljazeera.com",

    # ─── Entertainment ───
    "imdb.com",
    "rottentomatoes.com",
    "hotstar.com", "jiocinema.com",
    "primevideo.com",
    "disneyplus.com",

    # ─── Education ───
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
    "mit.edu",
    "stanford.edu",
    "harvard.edu",

    # ─── Tools & Productivity ───
    "notion.so",
    "figma.com",
    "canva.com",
    "trello.com",
    "asana.com",
    "adobe.com",
    "cloudflare.com",
    "vercel.com",
    "netlify.com",
    "heroku.com",
    "aws.amazon.com",

    # ─── Finance & Banking (India) ───
    "onlinesbi.sbi",
    "hdfcbank.com",
    "icicibank.com",
    "axisbank.com",
    "kotak.com",
    "yesbank.in",
    "pnbindia.in",
    "bankofbaroda.in",
    "paytm.com",
    "phonepe.com",
    "gpay.app",

    # ─── Finance & Banking (Global) ───
    "chase.com",
    "bankofamerica.com",
    "wellsfargo.com",
    "hsbc.com",
    "barclays.co.uk",

    # ─── Search & Browsers ───
    "yahoo.com",
    "duckduckgo.com",
    "brave.com",
    "mozilla.org",
    "opera.com",

    # ─── Indian Government ───
    "india.gov.in",
    "mygov.in",
    "digitalindia.gov.in",
    "uidai.gov.in",
    "incometax.gov.in",
    "epfindia.gov.in",
    "passportindia.gov.in",
    "negd.gov.in",
    "eci.gov.in",
    "pib.gov.in",
    "isro.gov.in",
    "iitb.ac.in",
    "iitd.ac.in",
    "iitk.ac.in",
    "iitm.ac.in",
    "irctc.co.in",
    "indianrailways.gov.in",
    "ugc.ac.in",
    "cbse.gov.in",
    "nta.ac.in",
    "digilocker.gov.in",
    "cowin.gov.in",
    "umang.gov.in",
    "gstn.org.in",
    "npci.org.in",

    # ─── US Government ───
    "usa.gov",
    "whitehouse.gov",
    "nasa.gov",
    "nih.gov",
    "cdc.gov",
    "irs.gov",
    "fbi.gov",
    "state.gov",

    # ─── UK Government ───
    "gov.uk",

    # ─── Other Government ───
    "europa.eu",
    "un.org",
    "who.int",
    "worldbank.org",
]

# ── Trusted TLD suffixes — any site ending with these is auto-safe ──
TRUSTED_GOVT_TLDS = [
    "gov.in", "gov.uk", "gov.us", "gov.au", "gov.ca", "gov.sg",
    "gov.za", "gov.br", "gov.jp", "gov.cn", "gov.fr", "gov.de",
    "gov", "mil", "mil.in",
    "ac.in", "edu.in", "res.in",  # Indian educational & research
    "edu", "edu.au", "edu.uk", "ac.uk", "ac.jp",  # Global educational
    "nic.in",  # Indian NIC
]


def is_trusted(url):
    """Smart check: matches registered domain OR trusted TLD suffix."""
    ext = tldextract.extract(url)
    registered_domain = f"{ext.domain}.{ext.suffix}".lower()

    # 1) Exact registered domain match
    if registered_domain in TRUSTED_DOMAINS:
        return True

    # 2) Check if TLD is a trusted government/educational suffix
    suffix = ext.suffix.lower()
    for trusted_tld in TRUSTED_GOVT_TLDS:
        if suffix == trusted_tld or suffix.endswith("." + trusted_tld):
            return True

    return False


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    try:

        data = request.get_json()
        url = data.get("url")

        if not url.startswith("http"):
            url = "https://" + url

        # Smart trusted domain check
        if is_trusted(url):
            return jsonify({
                "url": url,
                "final_risk": 2,
                "fraud_risk": 2,
                "adult_risk": 0,
                "domain_risk": 0,
                "vt_stats": {"malicious":0,"suspicious":0,"harmless":90},
                "reasons": ["Trusted domain detected"]
            })

        # Run engines
        url_risk, url_reasons = check_url_risk(url)
        entropy_risk, entropy_reasons = check_url_entropy(url)
        redirect_risk, redirect_reasons = check_redirects(url)
        adult_risk, adult_reasons = check_adult_content(url)
        ml_risk, ml_reasons = check_ml_phishing(url)
        vt_risk, vt_reasons, vt_stats = check_virustotal(url)
        domain_risk, domain_reasons = check_domain_reputation(url)
        brand_risk, brand_reasons = check_brand_impersonation(url)

        fraud_risk = min(
            url_risk +
            brand_risk +
            redirect_risk +
            entropy_risk +
            ml_risk +
            vt_risk,
            100
        )

        final_risk = min(
            fraud_risk +
            adult_risk +
            domain_risk,
            100
        )

        all_reasons = (
            url_reasons +
            adult_reasons +
            domain_reasons +
            brand_reasons +
            redirect_reasons +
            entropy_reasons +
            ml_reasons +
            vt_reasons
        )

        return jsonify({
            "url": url,
            "final_risk": final_risk,
            "fraud_risk": fraud_risk,
            "adult_risk": adult_risk,
            "domain_risk": domain_risk,
            "vt_stats": vt_stats,
            "reasons": all_reasons
        })

    except Exception as e:

        return jsonify({
            "final_risk": 90,
            "fraud_risk": 70,
            "adult_risk": 0,
            "domain_risk": 20,
            "vt_stats": {"malicious":0,"suspicious":0,"harmless":0},
            "reasons": [
                "Suspicious or unreachable domain",
                "High phishing probability"
            ]
        })


@app.route("/download-report", methods=["POST"])
def download_report():

    data = request.get_json()

    if "vt_stats" not in data:
        data["vt_stats"] = {"malicious":0,"suspicious":0,"harmless":0}

    pdf_buffer = generate_report(data)

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name="Security_Report.pdf",
        mimetype="application/pdf"
    )


if __name__ == "__main__":
    app.run(debug=True)