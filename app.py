import os
import csv
import json
from datetime import datetime
from flask import Flask, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__, static_folder='.')

# On Vercel, filesystem is read-only except /tmp
IS_VERCEL = os.environ.get('VERCEL', False)
BASE_DIR = '/tmp' if IS_VERCEL else '.'

UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
POSTER_FOLDER = os.path.join(BASE_DIR, 'uploads', 'posters')
CSV_FILE = os.path.join(BASE_DIR, 'submissions.csv')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['POSTER_FOLDER'] = POSTER_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max size
app.config['CSV_FILE'] = CSV_FILE

ADMIN_PIN = "sol@123"

# Ensure directories exist (safe on both local and /tmp)
for folder in [UPLOAD_FOLDER, POSTER_FOLDER]:
    try:
        os.makedirs(folder, exist_ok=True)
    except Exception:
        pass

# Ensure CSV file exists with headers
try:
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Name', 'Meme_Filename', 'Likes', 'JuryScore'])
except Exception:
    pass


ALLOWED_MEME_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_POSTER_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_meme(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_MEME_EXTENSIONS

def allowed_poster(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_POSTER_EXTENSIONS

# ─── STATIC ROUTES ──────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)

# ─── MEME SUBMIT ────────────────────────────────────────────
@app.route('/upload', methods=['POST'])
def upload_meme():
    if 'meme_file' not in request.files:
        return 'Missing meme file.', 400

    meme_file = request.files['meme_file']
    name = request.form.get('name', '').strip()
    consent = request.form.get('consent')

    if not name:
        return 'Please enter your name.', 400
    if not consent:
        return 'You must agree to the event rules.', 400
    if meme_file.filename == '':
        return 'No file selected.', 400
    if not allowed_meme(meme_file.filename):
        return 'Invalid file type. Only JPG, PNG, GIF allowed.', 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_name = secure_filename(name).replace(' ', '_')
    meme_filename = f"MEME_{timestamp}_{safe_name}_{secure_filename(meme_file.filename)}"
    meme_file.save(os.path.join(app.config['UPLOAD_FOLDER'], meme_filename))

    # Log to CSV
    with open(app.config['CSV_FILE'], 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            name, meme_filename, 0, 0
        ])

    return f'''
    <html>
        <body style="background:#05000a;color:#00FF00;font-family:'Outfit',sans-serif;display:flex;flex-direction:column;align-items:center;justify-content:center;height:100vh;text-align:center;">
            <h1 style="font-size:3rem;margin-bottom:20px;">Meme Uploaded! 🚀</h1>
            <p style="font-size:1.2rem;color:#B8A2C9;">Welcome to the Meme-verse, {name}. Your meme is pending approval.</p>
            <div style="background:rgba(255,0,255,0.1);padding:20px;border-radius:10px;margin-top:30px;border:1px solid #FF00FF;">
                <p><strong>File:</strong> {meme_filename}</p>
            </div>
            <a href="/" style="color:#00FFFF;margin-top:30px;text-decoration:none;font-size:1.1rem;border-bottom:1px solid #00FFFF;">← Back to Home</a>
        </body>
    </html>
    '''

# ─── POSTER UPLOAD ──────────────────────────────────────────
@app.route('/upload-poster', methods=['POST'])
def upload_poster():
    pin = request.form.get('pin', '')
    if pin != ADMIN_PIN:
        return jsonify({'error': 'Invalid PIN'}), 403

    if 'poster_file' not in request.files:
        return jsonify({'error': 'No poster file provided'}), 400

    poster_file = request.files['poster_file']
    title = request.form.get('poster_title', 'Event Poster').strip()

    if poster_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    if not allowed_poster(poster_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    poster_filename = f"POSTER_{timestamp}_{secure_filename(poster_file.filename)}"
    poster_file.save(os.path.join(app.config['POSTER_FOLDER'], poster_filename))

    # Save metadata
    meta_path = os.path.join(app.config['POSTER_FOLDER'], 'posters.json')
    posters = []
    if os.path.exists(meta_path):
        with open(meta_path, 'r') as f:
            posters = json.load(f)
    posters.append({'filename': poster_filename, 'title': title, 'uploaded_at': timestamp})
    with open(meta_path, 'w') as f:
        json.dump(posters, f)

    return jsonify({'success': True, 'filename': poster_filename})

# ─── API: POSTERS ────────────────────────────────────────────
@app.route('/api/posters')
def api_posters():
    meta_path = os.path.join(app.config['POSTER_FOLDER'], 'posters.json')
    if not os.path.exists(meta_path):
        return jsonify([])
    with open(meta_path, 'r') as f:
        posters = json.load(f)
    # Add URL path
    for p in posters:
        p['url'] = f"/uploads/posters/{p['filename']}"
    return jsonify(posters)

# ─── API: MEMES (Gallery) ────────────────────────────────────
@app.route('/api/memes')
def api_memes():
    if not os.path.exists(app.config['CSV_FILE']):
        return jsonify([])
    memes = []
    with open(app.config['CSV_FILE'], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fn = row.get('Meme_Filename', '')
            if fn and os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], fn)):
                ext = fn.rsplit('.', 1)[-1].lower()
                if ext in ('jpg', 'jpeg', 'png', 'gif'):
                    memes.append({
                        'name': row.get('Name', 'Anonymous'),
                        'filename': fn,
                        'url': f"/uploads/{fn}",
                        'timestamp': row.get('Timestamp', '')
                    })
    return jsonify(memes)

# ─── API: LEADERBOARD ────────────────────────────────────────
@app.route('/api/leaderboard')
def api_leaderboard():
    if not os.path.exists(app.config['CSV_FILE']):
        return jsonify([])
    rows = []
    with open(app.config['CSV_FILE'], 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                likes = int(row.get('Likes', 0))
                jury = int(row.get('JuryScore', 0))
                score = (likes * 10) + jury
                fn = row.get('Meme_Filename', '')
                ext = fn.rsplit('.', 1)[-1].lower() if fn else ''
                rows.append({
                    'name': row.get('Name', 'Anonymous'),
                    'filename': fn,
                    'url': f"/uploads/{fn}" if fn and ext in ('jpg','jpeg','png','gif') else None,
                    'likes': likes,
                    'jury_score': jury,
                    'total_score': score,
                    'timestamp': row.get('Timestamp', '')
                })
            except (ValueError, KeyError):
                continue
    # Sort by total score descending
    rows.sort(key=lambda x: x['total_score'], reverse=True)
    return jsonify(rows)

# ─── API: VERIFY ADMIN PIN ───────────────────────────────────
@app.route('/api/verify-pin', methods=['POST'])
def verify_pin():
    data = request.get_json() or {}
    pin = data.get('pin', '')
    if pin == ADMIN_PIN:
        return jsonify({'valid': True})
    return jsonify({'valid': False}), 403

if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
