import joblib
import textdistance
import whois
import datetime
import os
# LOAD MODEL 
try:
    url_model = joblib.load('url_model.pkl')
except:
    url_model = None

def load_safe_brands():
   # Loads a whitelist of trusted domains from a file  
    file_path = 'top_websites.txt'
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return [line.strip().lower() for line in f if line.strip()]
        except:
            # Default trusted brands if file is missing
            pass
    return ['google.com', 'facebook.com', 'amazon.com', 'wikipedia.org', 'netflix.com', 
            'ebay.com', 'paypal.com', 'microsoft.com', 'apple.com', 'instagram.com', 'twitter.com']

DYNAMIC_SAFE_BRANDS = load_safe_brands()

def normalize_string(s):
    s = s.lower()
    # Converts leetspeak characters (e.g., @, 0, 1) to standard letters for analysis
    replacements = {'@': 'a', '0': 'o', '1': 'i', '3': 'e', '4': 'a', '5': 's', '8': 'b', '$': 's', '!': 'i'}
    for char, replacement in replacements.items():
        s = s.replace(char, replacement)
    return s

def analyze_url_security(url):
    # Core function to detect phishing, typo-squatting, and domain age risks
    # Clean URL to extract the base domain
    clean_url = url.lower().replace("https://", "").replace("http://", "").replace("www.", "")
    domain = clean_url.split('/')[0]
    
    results = {
        "url": url,
        "domain": domain,
        "ai_prediction": "Safe",
        "typo_warning": "None",
        "age_info": "Checking...",
        "risk_score": 0
    }
    # --- FIX: TRUSTED DOMAIN CHECK ---
    # Agar domain google.com par khatam ho ya .google par, toh ye safe hai
    trusted_suffixes = ['google.com', '.google', 'facebook.com', 'microsoft.com', 'apple.com']
    for suffix in trusted_suffixes:
        if domain.endswith(suffix):
            results["ai_prediction"] = "Safe (Verified Brand)"
            results["risk_score"] = 0
            results["typo_warning"] = "None"
            return results # Yahin se wapis bhej dein, mazeed check ki zaroorat nahi
# Immediate pass for whitelisted domains
    if domain in DYNAMIC_SAFE_BRANDS:
        results["ai_prediction"] = "Safe"
        return results
# AI Model Prediction
    if url_model:
        try:
            pred = url_model.predict([url])[0]
            if pred == "Phishing":
                results["ai_prediction"] = "Phishing"
                results["risk_score"] += 50
        except:
            pass
# --- TYPO-SQUATTING & SIMILARITY DETECTION ---
    # --- FIXED BEST MATCH LOGIC ---
    user_base = domain.split('.')[0]
    normalized_user = normalize_string(user_base)

    best_sim = 0
    best_brand = ""

    for brand in DYNAMIC_SAFE_BRANDS:
        brand_base = brand.split('.')[0]
        # Check similarity for both original and normalized (leetspeak) versions
        sim_orig = textdistance.jaro_winkler(user_base, brand_base)
        sim_norm = textdistance.jaro_winkler(normalized_user, brand_base)
        current_sim = max(sim_orig, sim_norm)
        
        # Flag if symbols are used to mimic a brand (e.g., p@ypal)
        is_leetspeak = (normalized_user == brand_base and user_base != brand_base)
        # High similarity threshold (82% to 99%)
        if is_leetspeak or (0.82 < current_sim < 1.0):
            if current_sim > best_sim or is_leetspeak:
                best_sim = 1.0 if is_leetspeak else current_sim
                best_brand = brand_base.upper()
 # --- DOMAIN AGE ANALYSIS (WHOIS) ---
    # Final Result Check
    if best_brand != "": 
        results["typo_warning"] = f"Suspicious Similarity to {best_brand}"
        results["risk_score"] += 45
        results["ai_prediction"] = "Phishing (High Risk)"
    try:
        w = whois.whois(domain)
        if w.creation_date:
            c_date = w.creation_date[0] if isinstance(w.creation_date, list) else w.creation_date
            age_days = (datetime.datetime.now() - c_date).days
            results["age_info"] = f"New Domain ({age_days} days old)" if age_days < 182 else "Established Domain"
            # Flag domains younger than 6 months (182 days)
            if age_days < 182: results["risk_score"] += 20
        else:
            results["age_info"] = "Age Not Found"
    except:
        results["age_info"] = "Private/Invalid Domain"
# Final Risk Assessment
    if results["risk_score"] >= 60:
        results["ai_prediction"] = "Phishing (High Risk)"

    return results