🛡️ AI-Powered Cyber Threat Analyzer (Cyber Shield)

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Framework](https://img.shields.io/badge/Framework-Flask-red.svg)
![ML](https://img.shields.io/badge/ML-Scikit--Learn-orange.svg)
![Status](https://img.shields.io/badge/Status-Production--Ready-green.svg)

An industry-grade cybersecurity intelligence platform integrating Machine Learning and Static Heuristic Forensics to identify, classify, and mitigate digital threats. This project features a centralized web-based security dashboard and a real-time Manifest V3 Chrome Extension for proactive threat detection.

---

##  Key Features

## 1. Intelligent Password Auditor
 ML-Based Classification: Implements a Logistic Regression model with character-level TF-IDF vectorization to determine password complexity.
Breach Intelligence: Utilizes K-Anonymity with SHA-1 hashing to securely query global breach databases (HaveIBeenPwned API).
Predictive Heuristics: Detects high-risk patterns using NLP-based regex auditing.

## 2. Phishing & Typo-Squatting Scanner
Ensemble Detection: Driven by a Random Forest Classification trained on balanced phishing datasets for high-precision classification.                                                                                                       Deception Analysis:Employs Jaro-Winkler Distance and Leetspeak Normalization to identify typo-squatting domains.
Metadata Forensics: Integrated WHOIS lookup to analyze domain age and registration anomalies.

### 3. Malware PE Forensics
Static Binary Analysis: Parses Windows Portable Executable (PE) structures using `pefile` to extract headers and metadata without execution risk.
Entropy Auditing: Calculates mathematical entropy to detect packed, encrypted, or obfuscated malicious payloads.

---

##  Technical Stack
Backend: Flask (Python) Micro-framework
AI/ML: Scikit-learn (Logistic Regression, Random Forest), Pandas, Joblib
Security Tools: SHA-1 Hashing, WHOIS Intelligence, PE-Header Forensics
Database: SQLAlchemy (SQLite) for encrypted user session management
Extension: JavaScript (Manifest V3 API)
Documentation: Automated PDF Security Report generation via FPDF

---

##  Installation & Deployment

### 1. Environment Setup
Clone the repository and install the required dependencies:

```bash
git clone https://github.com/malik-muneeb-dev/AI-Powered-Cyber-Threat-Analyzer.git
cd AI-Powered-Cyber-Threat-Analyzer
pip install -r requirements.txt
2. Download Pre-trained Models (Important)
Due to the large file size, the trained Machine Learning models (.pkl files) are hosted in the GitHub Releases section.
Go to the Releases tab of this repository.
Download the url_model.pkl (and any other available models).
Place the downloaded .pkl files directly in the root directory of the project.
3. Launch Application
Initialize the database and run the Flask server:
code
Bash
python app.py
Access the security dashboard at: http://127.0.0.1:5000
📊 Performance Metrics
URL Detection Accuracy: ~92.03% (Random Forest Classifier)
API Latency: ~800ms for real-time Chrome Extension alerts
Static Forensics: Zero-execution risk analysis of .exe headers
👤 Developer
Malik Muneeb
Computer Science Graduate | AI & Cybersecurity Enthusiast
📍 Wah Cantt, Pakistan
📧 itsmuneeb22520@gmail.com
🔗 LinkedIn www.linkedin.com/in/malik-muneeb-dev

Note: This project was developed as a Final Year Project (FYP) and secured a top position for its technical execution and innovative approach
