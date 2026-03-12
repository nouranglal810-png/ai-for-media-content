# 🛡️ AI URL Risk Analyzer

> **Advanced AI-Powered URL Security Scanner** — Detects phishing, malware, and fraudulent links in real-time using Machine Learning, VirusTotal API, and multi-layer heuristic analysis.

![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.0+-000000?style=for-the-badge&logo=flask&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white)
![VirusTotal](https://img.shields.io/badge/VirusTotal-API-394EFF?style=for-the-badge&logo=virustotal&logoColor=white)

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🧠 **ML Phishing Detection** | Random Forest classifier trained on URL pattern features |
| 🛡️ **VirusTotal Integration** | Scans URLs against 90+ antivirus engines |
| 🔍 **Heuristic Analysis** | URL entropy, suspicious keywords, TLD checking |
| 🎭 **Brand Impersonation** | Detects fake versions of known brands (g00gle, paypa1) |
| 🔄 **Redirect Chain Analysis** | Tracks multi-hop redirects and domain changes |
| 🌐 **Domain Reputation** | WHOIS-based domain age and registration analysis |
| 🔞 **Adult Content Detection** | Keyword-based adult domain identification |
| 📄 **PDF Security Report** | Download detailed analysis report as PDF |

---

## 🖥️ Screenshots

### Home Page
- Premium glassmorphism UI with animated background
- Feature cards highlighting ML, VirusTotal, Heuristics, PDF Report

### Analysis Results
- Animated circular risk gauge with verdict badge
- Sub-risk breakdown: Fraud, Adult, Domain, ML Confidence
- VirusTotal stats grid (Malicious / Suspicious / Safe)
- Detailed findings with color-coded severity icons

---

## 🏗️ Architecture

```
AI_URL_Risk_Analyzer/
├── app.py                    # Flask application & API routes
├── requirements.txt          # Python dependencies
├── models/
│   ├── train_model.py        # ML model training script
│   └── phishing_model.pkl    # Trained Random Forest model
├── utils/
│   ├── url_checker.py        # URL heuristic analysis engine
│   ├── ml_checker.py         # ML-based phishing prediction
│   ├── virustotal_checker.py # VirusTotal API integration
│   ├── adult_checker.py      # Adult content detection
│   └── report_generator.py   # PDF report generation
└── templates/
    └── index.html            # Frontend UI (glassmorphism design)
```

---

## 🔧 Tech Stack

- **Backend:** Python, Flask
- **ML Model:** scikit-learn (Random Forest Classifier)
- **APIs:** VirusTotal v3 API
- **Frontend:** HTML5, CSS3 (Glassmorphism), Vanilla JavaScript
- **Fonts:** Inter, JetBrains Mono (Google Fonts)
- **PDF:** ReportLab
- **Domain Analysis:** python-whois, tldextract

---

## ⚡ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/nouranglal810-png/AI-URL-Risk-Analyzer.git
cd AI-URL-Risk-Analyzer
```

### 2. Create virtual environment
```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
python app.py
```

### 5. Open in browser
```
http://127.0.0.1:5000
```

---

## 🧪 How It Works

1. **URL Input** → User pastes a URL
2. **Multi-Engine Scan** → Runs 7 analysis engines in parallel:
   - URL structure analysis (HTTPS, length, suspicious patterns)
   - URL entropy calculation (randomness detection)
   - Brand impersonation detection (character substitution)
   - Redirect chain tracking
   - ML model prediction (Random Forest)
   - VirusTotal API scan (90+ engines)
   - Domain WHOIS reputation check
3. **Risk Scoring** → Aggregates scores from all engines (0-100%)
4. **Results Dashboard** → Displays animated risk gauge, sub-risks, and detailed findings
5. **PDF Report** → Option to download comprehensive security report

---

## 📊 Risk Scoring

| Risk Level | Score | Color |
|-----------|-------|-------|
| 🟢 Low Risk | 0-29% | Green |
| 🟡 Moderate Risk | 30-69% | Yellow |
| 🔴 High Risk | 70-100% | Red |

---

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Norang Lal**

- GitHub: [@nouranglal810-png](https://github.com/nouranglal810-png)

---

> ⭐ If you found this useful, please give it a star!
