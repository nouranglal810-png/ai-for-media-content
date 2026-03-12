from flask import Flask, render_template, request, jsonify, send_file

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

# Trusted domains whitelist
TRUSTED_DOMAINS = [
    "amazon.com",
    "google.com",
    "microsoft.com",
    "facebook.com",
    "github.com",
    "youtube.com",
    "linkedin.com",
    "apple.com"
]


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

        domain = url.split("//")[-1].split("/")[0].replace("www.","")

        # Trusted domain override
        if domain in TRUSTED_DOMAINS:
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