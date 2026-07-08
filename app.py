from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True) # Yeh line extension ko ijazat degi data bhejne ki
import joblib
import os
from report_generator import generate_pdf_report
from flask import send_file
import io
# Custom Modules 
from nlp import check_nlp_patterns 
from breach import check_breach #,load_breach_database 
from crack_time import calculate_crack_time
from generator import generate_strong_passwords 
from url_analyzer import analyze_url_security
# app.py mein top par check karein ke 'send_from_directory' import hai ya nahi
from flask import send_from_directory
app.secret_key = "fyp-secret-key"

# 1. SIMPLE DATABASE CONFIG 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
# Create 'uploads' folder if it doesn't exist
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# 2. DATABASE TABLES 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(300), nullable=False)
    extension_enabled = db.Column(db.Boolean, default=True)
class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename_or_url = db.Column(db.String(500), nullable=False)
    scan_type = db.Column(db.String(50), nullable=False) 
    result = db.Column(db.String(500), nullable=False)   
    timestamp = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

# 3. LOAD AI MODELS 
# AI Model load 
MODEL_FILE = 'model_feature1.pkl'
if os.path.exists(MODEL_FILE):
    ai_model = joblib.load(MODEL_FILE)
else:
    ai_model = None

# Breach database load kar rahe hain
# load_breach_database()

# 4. HELPER FUNCTION 
@app.context_processor
def inject_user():
    user = None
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
       # user = User.query.get(session['user_id'])
    return dict(current_user=user)
# Ye naya route end mein add karein
@app.route('/download-extension')
def download_extension():
    # Ye 'static' folder se zip file utha kar user ko bhej dega
    return send_from_directory('static', 'Cyber_Shield.zip', as_attachment=True)
# @app.route('/')
# def home():
#     return render_template('index.html')
@app.route('/toggle-extension', methods=['POST'])
def toggle_extension():
    if 'user_id' not in session:
        return jsonify({"error": "Login required"}), 401
    
    user = db.session.get(User, session['user_id'])
    # Switch logic: Agar True hai toh False kar do, agar False hai toh True
    user.extension_enabled = not user.extension_enabled
    db.session.commit()
    
    return jsonify({
        "is_enabled": user.extension_enabled,
        "message": "Extension " + ("Enabled" if user.extension_enabled else "Disabled")
    })
@app.route('/download-report/<int:scan_id>')
def download_report(scan_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Database se data lena
    scan = db.session.get(ScanHistory, scan_id)
    user = db.session.get(User, session['user_id'])
    
    if not scan or scan.user_id != user.id:
        return "Unauthorized or Not Found", 404

    # Dusri file se function call karna
    pdf_bytes = generate_pdf_report(scan, user.username)
    
    return send_file(
        io.BytesIO(pdf_bytes),
        download_name=f"Security_Report_{scan.id}.pdf",
        as_attachment=True
    )
@app.route('/')
def home():
    # Database se statistics nikalna
    total_scans = ScanHistory.query.count()
    
    # Phishing URL count
    phishing_count = ScanHistory.query.filter(
        (ScanHistory.scan_type == 'URL') & (ScanHistory.result.contains('Phishing'))
    ).count()
    
    # Malicious File count
    malware_count = ScanHistory.query.filter(
        (ScanHistory.scan_type == 'Malware File') & (ScanHistory.result.contains('MALICIOUS'))
    ).count()
    
    # Safe results count
    safe_count = total_scans - (phishing_count + malware_count)

    return render_template('index.html', 
                           total=total_scans, 
                           phishing=phishing_count, 
                           malware=malware_count, 
                           safe=safe_count)

# REGISTER 
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # 1. Check Username
        if User.query.filter_by(username=username).first():
            flash("Username already exists!", "error")
            return redirect(url_for('register'))
        
        # 2. AI Strength Check
        if ai_model:
            strength = ai_model.predict([password])[0] 
            if strength == 'Weak': 
                flash("Error: Password is too Weak! Please use a stronger password.", "error")
                return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        user = User(
            username=username,
            password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        flash("Registration successful! Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')

# LOGIN
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id  # Session start
            flash(f"Welcome {user.username}!", "success")
            return redirect(url_for('home'))

        flash("Invalid username or password", "error")

    return render_template('login.html')

# LOGOUT
@app.route('/logout')
def logout():
    session.pop('user_id', None) 
    flash("Logged out successfully.", "info")
    return redirect(url_for('home'))
@app.route('/api/analyze-url', methods=['POST'])
def api_analyze_url():
     # --- LOGIN CHECK START ---
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized. Please login to use Extension."}), 401
    # --- LOGIN CHECK END ---
    data = request.json
    url = data.get('url', '')
    if not url:
        return jsonify({"error": "No URL provided"}), 400
    
    # Aapka purana function use karein
    result = analyze_url_security(url)
    
    return jsonify({
        "prediction": result['ai_prediction'],
        "risk_score": result['risk_score']
    })
# TOOL 1: PASSWORD ANALYZER
@app.route('/password-tool')
def password_tool():
    return render_template('password_tool.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # --- LOGIN CHECK ---
    #if 'user_id' not in session:
        #return jsonify({"error": "Unauthorized. Please login."}), 401

    # if 'user_id' not in session:
    #     return jsonify({"error": "Unauthorized"}), 401

    # user = db.session.get(User, session['user_id'])
    
    # # AGAR DISABLE HAI TOH YAHIN SE WAPIS BHEJ DO
    # if not user.extension_enabled:
    #     return jsonify({"status": "inactive"}) 
    if 'user_id' in session:
        user = db.session.get(User, session['user_id'])
        if user and not user.extension_enabled:
            return jsonify({"status": "inactive", "message": "Extension disabled by user"})

    password = request.json.get('password', '')
    
    # 1. AI Strength Prediction
    if ai_model:
        strength = ai_model.predict([password])[0].upper()
    else:
        strength = "UNKNOWN"

    # 2. HEURISTIC OVERRIDE (Length Check Fix)
    # Agar password 8 chars se chota hai toh AI kuch bhi kahe, hum WEAK dikhayenge
    if len(password) < 8:
        strength = "WEAK"

    # 3. Yahan 'res' variable banayein taake print ho sakay
    res = {
        "strength": strength,
        "warnings": check_nlp_patterns(password),
        "breach_count": check_breach(password),
        "crack_time": calculate_crack_time(password),
        "suggestions": generate_strong_passwords(password)
    }

    print("BACKEND RESPONSE:", res) # Ab ye line error nahi degi
    return jsonify(res) # Sirf aik bar return hoga

# --- TOOL 2: URL SCANNER (UPDATED) ---
@app.route('/url_tool', methods=['GET', 'POST'])
def url_tool():
    analysis = None
    if request.method == 'POST':
        # Dono tarah ka data handle karein (Form ya JSON)
        user_url = request.form.get('url') or (request.json.get('url') if request.is_json else None)

        if user_url:
            analysis = analyze_url_security(user_url)
            new_scan = ScanHistory(
                filename_or_url=user_url,
                scan_type="URL",
                result=analysis.get('ai_prediction', 'Unknown'),
                user_id=session.get('user_id')
            )
            db.session.add(new_scan)
            db.session.commit()

            # Agar request JS (Fetch) se aayi hai toh JSON bhejo
            if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify(analysis)

    return render_template('url_tool.html', analysis=analysis)

# --- TOOL 3: MALWARE ANALYZER (UPDATED) ---
@app.route('/malware-tool', methods=['GET', 'POST'])
def malware_tool():
    result = None
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file.filename:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)

            from malware_analyzer import analyze_malware_ai
            result = analyze_malware_ai(path)

            new_scan = ScanHistory(
                filename_or_url=filename,
                scan_type="Malware File",
                result=result.get('ai_prediction', 'Unknown'),
                user_id=session.get('user_id')
            )
            db.session.add(new_scan)
            db.session.commit()

            # Agar request JS se aayi hai toh JSON bhejo
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.is_json:
                return jsonify(result)

    return render_template('malware_tool.html', result=result)
#  HISTORY PAGE 
@app.route('/history')
def history():

    if 'user_id' in session:
        scans = ScanHistory.query.filter_by(user_id=session['user_id']).order_by(ScanHistory.timestamp.desc()).all()
    else:
        scans = [] 
        flash("Please login to view history", "info")

    return render_template('history.html', scans=scans)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
