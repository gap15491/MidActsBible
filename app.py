"""
KJV Rightly Divided — backend.
Serves the static Bible + companion chart, and provides a small authenticated
notes API (per-user chapter and verse notes) backed by Postgres (SQLite locally).
"""
import os
import re
import json
import datetime
from flask import Flask, request, jsonify, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import UniqueConstraint

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__, static_folder=None)

# --- Secret key (sign session cookies) ---
app.secret_key = os.environ.get("SECRET_KEY", "dev-insecure-change-me")

# --- Database URL: Railway injects DATABASE_URL for the Postgres plugin. ---
db_url = os.environ.get("DATABASE_URL", "").strip()
if db_url.startswith("postgres://"):            # SQLAlchemy needs the +psycopg2 dialect name
    db_url = db_url.replace("postgres://", "postgresql://", 1)
if not db_url:
    db_url = "sqlite:///" + os.path.join(BASE_DIR, "notes.db")   # local dev fallback
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# --- Cookie hardening (Secure only when not local dev) ---
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = bool(os.environ.get("DATABASE_URL"))

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Note(db.Model):
    __tablename__ = "notes"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    book = db.Column(db.String(40), nullable=False)
    chapter = db.Column(db.Integer, nullable=False)
    verse = db.Column(db.Integer, nullable=True)          # NULL = chapter-level note
    text = db.Column(db.Text, nullable=False, default="")
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow,
                           onupdate=datetime.datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "book", "chapter", "verse",
                                       name="uq_note_scope"),)


with app.app_context():
    db.create_all()


# ---------------- helpers ----------------
def current_user():
    uid = session.get("uid")
    if not uid:
        return None
    return db.session.get(User, uid)


def require_login():
    u = current_user()
    if not u:
        return None
    return u


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


# ---------------- auth ----------------
@app.post("/api/register")
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    if not EMAIL_RE.match(email):
        return jsonify(error="Please enter a valid email address."), 400
    if len(password) < 8:
        return jsonify(error="Password must be at least 8 characters."), 400
    if User.query.filter_by(email=email).first():
        return jsonify(error="An account with that email already exists."), 409
    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    session["uid"] = user.id
    return jsonify(email=user.email)


@app.post("/api/login")
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify(error="Incorrect email or password."), 401
    session["uid"] = user.id
    return jsonify(email=user.email)


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(ok=True)


@app.get("/api/me")
def me():
    u = current_user()
    return jsonify(email=u.email if u else None)


# ---------------- notes ----------------
def _norm_verse(v):
    if v in (None, "", "null"):
        return None
    return int(v)


@app.get("/api/notes")
def get_notes():
    u = require_login()
    if not u:
        return jsonify(error="Not logged in."), 401
    book = (request.args.get("book") or "").strip()
    try:
        chapter = int(request.args.get("chapter"))
    except (TypeError, ValueError):
        return jsonify(error="book and chapter are required."), 400
    rows = Note.query.filter_by(user_id=u.id, book=book, chapter=chapter).all()
    chapter_note = None
    verses = {}
    for r in rows:
        if r.verse is None:
            chapter_note = r.text
        else:
            verses[str(r.verse)] = r.text
    return jsonify(book=book, chapter=chapter, chapter_note=chapter_note, verses=verses)


@app.put("/api/notes")
def put_note():
    u = require_login()
    if not u:
        return jsonify(error="Not logged in."), 401
    data = request.get_json(silent=True) or {}
    book = (data.get("book") or "").strip()
    try:
        chapter = int(data.get("chapter"))
    except (TypeError, ValueError):
        return jsonify(error="book and chapter are required."), 400
    verse = _norm_verse(data.get("verse"))
    text = (data.get("text") or "").strip()
    row = Note.query.filter_by(user_id=u.id, book=book, chapter=chapter, verse=verse).first()
    if not text:
        if row:
            db.session.delete(row)
            db.session.commit()
        return jsonify(ok=True, deleted=True)
    if row:
        row.text = text
    else:
        row = Note(user_id=u.id, book=book, chapter=chapter, verse=verse, text=text)
        db.session.add(row)
    db.session.commit()
    return jsonify(ok=True, updated_at=row.updated_at.isoformat())


@app.delete("/api/notes")
def delete_note():
    u = require_login()
    if not u:
        return jsonify(error="Not logged in."), 401
    data = request.get_json(silent=True) or {}
    book = (data.get("book") or "").strip()
    try:
        chapter = int(data.get("chapter"))
    except (TypeError, ValueError):
        return jsonify(error="book and chapter are required."), 400
    verse = _norm_verse(data.get("verse"))
    row = Note.query.filter_by(user_id=u.id, book=book, chapter=chapter, verse=verse).first()
    if row:
        db.session.delete(row)
        db.session.commit()
    return jsonify(ok=True)


# ---------------- Strong's concordance ----------------
STRONGS_DIR = os.path.join(BASE_DIR, "data")
try:
    with open(os.path.join(STRONGS_DIR, "strongs_verses.json"), encoding="utf-8") as _f:
        STRONGS_VERSES = json.load(_f)
    with open(os.path.join(STRONGS_DIR, "strongs_lex.json"), encoding="utf-8") as _f:
        STRONGS_LEX = json.load(_f)
except Exception:
    STRONGS_VERSES, STRONGS_LEX = {}, {}

TAG_RE = re.compile(r"\[([GH]\d+)\]")


@app.get("/api/strongs")
def strongs():
    book = (request.args.get("book") or "").strip()
    try:
        chapter = int(request.args.get("chapter"))
        verse = int(request.args.get("verse"))
    except (TypeError, ValueError):
        return jsonify(error="book, chapter and verse are required."), 400
    en = STRONGS_VERSES.get(f"{book}|{chapter}|{verse}")
    if en is None:
        return jsonify(ref=f"{book} {chapter}:{verse}", available=False, words=[])
    words = []
    for tok in en.split(" "):
        nums = TAG_RE.findall(tok)
        if not nums:
            continue
        word = TAG_RE.sub("", tok).strip()
        entries = []
        for n in nums:
            e = STRONGS_LEX.get(n)
            entries.append({"num": n, **e} if e else {"num": n})
        words.append({"w": word, "entries": entries})
    return jsonify(ref=f"{book} {chapter}:{verse}", available=True, words=words)


# ---------------- static site ----------------
@app.get("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/chart.html")
def chart():
    return send_from_directory(BASE_DIR, "chart.html")


@app.get("/healthz")
def healthz():
    return jsonify(ok=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=True)
