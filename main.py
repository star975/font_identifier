def main():
    # Initialize session state for payment selection
    if "selected_payment" not in st.session_state:
        st.session_state.selected_payment = None

import asyncio
import os
import json
import sqlite3
import hashlib
import base64
from typing import Optional, Tuple, Dict, Any
from datetime import datetime, timedelta
import streamlit as st
from PIL import Image
import streamlit.components.v1 as components
from torchvision import models as tv_models
import torch
import torch.nn as nn

st.set_page_config(
    page_title="Font Identifier & Recorder", 
    layout="wide",
    page_icon="🖋️",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://github.com/your-repo/issues',
        'Report a bug': 'https://github.com/your-repo/issues',
        'About': "# Font Identifier\nAI-powered font identification with screen recording capabilities."
    }
)

try: 
    import utils 
    HAS_UTILS = True 
except Exception:
    HAS_UTILS = False
# ====================================================
#               EVENT LOOP SAFETY (ASYNCIO)
# ====================================================
try:
    asyncio.get_running_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

# ====================================================
#                 ENVIRONMENT FIXES
# ====================================================
os.environ["STREAMLIT_WATCHER_IGNORE_ERRORS"] = "true"
os.environ["STREAMLIT_SERVER_FILE_WATCHER_TYPE"] = "none"
os.environ["STREAMLIT_WATCHER_IGNORE_MODULES"] = "torch"
os.environ["STREAMLIT_WATCH_SYSTEM_PYTHON"] = "false"

# Path for recordings
RECORDINGS_DIR = os.path.join("backend", "recordings")
os.makedirs(RECORDINGS_DIR, exist_ok=True)

# ====================================================
#               TORCH CPU FIXES
# ====================================================
try:
    import torch.backends.mkldnn as mkldnn
    mkldnn.enabled = False
except Exception:
    pass

# ====================================================
#                 CONSTANTS / PATHS
# ====================================================
APP_BRAND = "🖋️ Font Identifier"
DB_PATH = "app_users.db"
MODEL_PATH = "model.pth"
LABELS_PATH = os.path.join("data", "fontlist.txt")

# -----------------------------
# === PWA AND MOBILE SETUP ===

# PWA Meta tags and manifest
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<meta name="theme-color" content="#6366f1">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="FontID">
<link rel="manifest" href="/static/manifest.json">
<link rel="apple-touch-icon" href="/static/icons/icon-192x192.png">
<link rel="icon" type="image/png" sizes="32x32" href="/static/icons/icon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/static/icons/icon-16x16.png">
<script>
  // Register service worker for PWA functionality
  if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/sw.js')
        .then((registration) => {
          console.log('SW registered: ', registration);
        })
        .catch((registrationError) => {
          console.log('SW registration failed: ', registrationError);
        });
    });
  }
</script>
""", unsafe_allow_html=True)

# === GLOBAL APP DESIGN (Dark + Mixed Colors + Glassmorphism + Mobile Responsive) ===
st.markdown("""
<style>
/* ===== Root Colors ===== */
:root {
  --bg: #0a0f1e;
  --card: rgba(255, 255, 255, 0.06);
  --border: rgba(255, 255, 255, 0.15);
  --text: #f8fafc;
  --muted: #94a3b8;
  --accent: #6366f1;
  --accent-2: #06b6d4;
  --accent-3: #ec4899;
  --shadow: 0 8px 25px rgba(0,0,0,.35);
  --blur: 18px;
  --radius: 18px;
}

/* ===== Background ===== */
html, body, [class*="css"] {
  background: radial-gradient(circle at top left, #1e293b, #0a0f1e);
  color: var(--text);
  font-family: 'Segoe UI', sans-serif;
}

/* ===== Headings ===== */
h1, h2, h3 {
  font-weight: 700;
  letter-spacing: -0.5px;
}
h1 {
  font-size: 42px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2), var(--accent-3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
h2 {
  font-size: 28px;
  color: var(--accent-2);
}
p {
  font-size: 16px;
  color: var(--muted);
  line-height: 1.6;
}

/* ===== Buttons ===== */
.stButton>button {
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  color: white;
  border: none;
  padding: .75rem 1.25rem;
  border-radius: var(--radius);
  font-weight: 600;
  box-shadow: var(--shadow);
  transition: all .25s ease;
}
.stButton>button:hover {
  transform: translateY(-2px) scale(1.02);
  background: linear-gradient(135deg, var(--accent-3), var(--accent-2));
}

/* ===== Glass Cards ===== */
.card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 22px;
  border: 1px solid var(--border);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
  box-shadow: var(--shadow);
  margin-bottom: 20px;
}
.kpi {
  text-align: center;
}

/* ===== Navbar ===== */
.navbar {
  width: 100%;
  display: flex;
  justify-content: center;
  gap: 18px;
  padding: 14px 12px;
  margin-bottom: 28px;
  position: sticky;
  top: 0;
  background: rgba(15, 23, 42, 0.7);
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
  border-bottom: 1px solid var(--border);
  border-radius: 0 0 var(--radius) var(--radius);
  z-index: 9999;
}
.navlink {
  color: var(--text);
  text-decoration: none;
  font-weight: 600;
  padding: 8px 16px;
  border-radius: 12px;
  transition: all .25s ease;
}
.navlink:hover {
  background: rgba(255,255,255,0.12);
}

/* ===== Hero Section ===== */
.hero {
  background: linear-gradient(135deg, rgba(99,102,241,.25), rgba(6,182,212,.25), rgba(236,72,153,.2));
  backdrop-filter: blur(var(--blur));
  -webkit-backdrop-filter: blur(var(--blur));
  padding: 80px 28px;
  border-radius: 22px;
  text-align: center;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}
.hero h1 {
  font-size: 50px;
  margin-bottom: 12px;
}
.hero p {
  font-size: 18px;
  color: var(--muted);
}
.hero-cta {
  margin-top: 28px;
  display: flex;
  gap: 14px;
  justify-content: center;
}
.hero-cta a {
  text-decoration: none;
  color: white;
  font-weight: 600;
  padding: 12px 20px;
  border-radius: 14px;
  background: linear-gradient(135deg, var(--accent), var(--accent-2));
  box-shadow: var(--shadow);
  transition: all .25s ease;
}
.hero-cta a.secondary {
  background: transparent;
  color: var(--text);
  border: 1px solid var(--border);
}
.hero-cta a:hover {
  transform: scale(1.05);
}

/* ===== Feature Boxes ===== */
.feature {
  background: var(--card);
  border-radius: var(--radius);
  padding: 20px;
  text-align: center;
  border: 1px solid var(--border);
  box-shadow: var(--shadow);
}
.feature h3 {
  margin-top: 10px;
  font-size: 20px;
}
.feature p {
  font-size: 15px;
  color: var(--muted);
}

/* ===== Mobile Responsive Design ===== */
@media (max-width: 768px) {
  /* Mobile layout adjustments */
  .hero {
    padding: 40px 16px;
    text-align: center;
  }
  .hero h1 {
    font-size: 32px;
  }
  .hero p {
    font-size: 16px;
  }
  .hero-cta {
    flex-direction: column;
    gap: 10px;
  }
  .hero-cta a {
    width: 100%;
    text-align: center;
  }
  
  /* Navigation adjustments */
  .navbar {
    flex-wrap: wrap;
    gap: 8px;
    padding: 10px 8px;
  }
  .navlink {
    font-size: 14px;
    padding: 6px 12px;
  }
  
  /* Cards and features */
  .card {
    padding: 16px;
    margin-bottom: 16px;
  }
  .feature {
    padding: 16px;
    margin-bottom: 16px;
  }
  
  /* Buttons */
  .stButton>button {
    width: 100%;
    padding: 12px 16px;
    font-size: 16px;
    margin-bottom: 8px;
  }
  
  /* Form elements */
  .stTextInput>div>div>input,
  .stTextArea>div>div>textarea,
  .stSelectbox>div>div>select {
    font-size: 16px; /* Prevents zoom on iOS */
  }
  
  /* File uploader */
  .stFileUploader {
    margin-bottom: 16px;
  }
  
  /* Columns stack on mobile */
  .row-widget.stColumns {
    flex-direction: column;
  }
  .element-container .column {
    width: 100% !important;
    margin-bottom: 16px;
  }
}

@media (max-width: 480px) {
  /* Extra small screens */
  .hero h1 {
    font-size: 28px;
  }
  .card, .feature {
    padding: 12px;
  }
  .navbar {
    padding: 8px 4px;
  }
  .navlink {
    font-size: 12px;
    padding: 4px 8px;
  }
}

/* ===== Touch-friendly elements ===== */
@media (pointer: coarse) {
  .stButton>button {
    min-height: 44px; /* Minimum touch target size */
    padding: 12px 20px;
  }
  
  .navlink {
    min-height: 44px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  /* Larger tap targets */
  input, button, select, textarea {
    min-height: 44px;
  }
}

/* ===== Dark mode media query support ===== */
@media (prefers-color-scheme: dark) {
  /* Already dark by default, but can add overrides here */
}

/* ===== Reduced motion support ===== */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}

/* ===== High contrast support ===== */
@media (prefers-contrast: high) {
  :root {
    --border: rgba(255, 255, 255, 0.3);
    --text: #ffffff;
    --muted: #cccccc;
  }
}

/* ===== PWA specific styles ===== */
@media (display-mode: standalone) {
  /* When running as PWA */
  body {
    padding-top: env(safe-area-inset-top);
    padding-bottom: env(safe-area-inset-bottom);
  }
  
  .navbar {
    top: env(safe-area-inset-top);
  }
}

/* ===== Orientation support ===== */
@media (orientation: landscape) and (max-height: 500px) {
  .hero {
    padding: 20px 16px;
  }
  .hero h1 {
    font-size: 24px;
  }
}
</style>
""", unsafe_allow_html=True)



# ====================================================
#                 PERSISTENT AUTH (SQLite)
# ====================================================

def init_db():
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT NOT NULL,
            plan TEXT DEFAULT 'Free',
            expiry_date TEXT
        );
    """)
    con.commit()
    con.close()

init_db()

def _hash_password(password: str, salt: Optional[str] = None) -> str:
    """Salted SHA-256 (simple, dependency-free). Format: salt$hash"""
    if salt is None:
        salt = base64.urlsafe_b64encode(os.urandom(16)).decode("utf-8")
    h = hashlib.sha256((salt + password).encode("utf-8")).hexdigest()
    return f"{salt}${h}"

def _verify_password(password: str, salted_hash: str) -> bool:
    try:
        salt, h = salted_hash.split("$", 1)
    except ValueError:
        return False
    return _hash_password(password, salt) == f"{salt}${h}"

def create_user(username: str, password: str) -> Tuple[bool, str]:
    if not username or not password:
        return False, "Username and password are required."
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute(
            "INSERT INTO users (username, password_hash, created_at) VALUES (?, ?, ?)",
            (username, _hash_password(password), datetime.utcnow().isoformat()),
        )
        con.commit()
        con.close()
        return True, "Account created successfully."
    except sqlite3.IntegrityError:
        return False, "Username already exists."
    except Exception as e:
        return False, f"Error: {e}"
def get_user(username):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE username=?", (username,))
    row = cur.fetchone()
    con.close()
    return row 
def update_plan(username, plan):
    con = sqlite3.connect(DB_PATH)
    cur = con.cursor()
    expiry = (datetime.utcnow() + timedelta(days=30)).isoformat()
    cur.execute("UPDATE users SET plan=?, expiry_date=? WHERE username=?", (plan, expiry, username))
    con.commit()
    con.close() 

def authenticate(username: str, password: str) -> bool:
    try:
        con = sqlite3.connect(DB_PATH)
        cur = con.cursor()
        cur.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        con.close()
        if not row:
            return False
        return _verify_password(password, row[0])
    except Exception:
        return False

# ====================================================
#                 MODEL & INFERENCE
# ====================================================

def read_class_names() -> list:
    path = LABELS_PATH
    if not os.path.isabs(path):
        path = os.path.join(os.path.dirname(__file__), path)
    if not os.path.exists(path):
        # fallback dummy classes
        return [f"Font_{i}" for i in range(10)]
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

@st.cache_resource
def load_model_and_classes() -> Tuple[torch.nn.Module, list]:
    """
    Robust loader:
    - Works if 'model.pth' is a full pickled model
    - Or if it's a state_dict (with or without 'state_dict' key)
    - Avoids PyTorch 2.6 weights_only=True default by explicitly using weights_only=False
    """
    classes = read_class_names()

    # Resolve model path
    model_path = r"C:\Users\pc\Desktop\AI\model.pth"
    if not os.path.isabs(model_path):
        model_path = os.path.join(os.path.dirname(__file__), model_path)

    if not os.path.exists(model_path):
        st.error(f"Model file not found at: {model_path}")
        # Create trivial dummy classifier to avoid crashing
        class Dummy(nn.Module):
            def __init__(self, n): super().__init__(); self.fc = nn.Linear(1, n)
            def forward(self, x): return torch.zeros((x.shape[0], self.fc.out_features))
        return Dummy(len(classes)).eval(), classes

    # Load checkpoint (force weights_only=False for backward compatibility)
    ckpt = torch.load(model_path, map_location="cpu", weights_only=False)

    # Try to detect if it's a full model
    if isinstance(ckpt, nn.Module):
        model = ckpt
        try:
            model.eval()
        except Exception:
            pass
        return model, classes

    # Otherwise, assume it's a state_dict-like
    
    model = tv_models.resnet18(weights=None)  # backbone must match training
    model.fc = nn.Linear(model.fc.in_features, len(classes))

    # Handle possible nested "state_dict" key
    if isinstance(ckpt, dict) and "state_dict" in ckpt and isinstance(ckpt["state_dict"], dict):
        state = ckpt["state_dict"]
    else:
        state = ckpt

    missing, unexpected = model.load_state_dict(state, strict=False)
    if unexpected:
        st.info(f"Loaded with unexpected keys: {unexpected}")
    if missing:
        st.info(f"Loaded with missing keys: {missing}")

    model.eval()
    return model, classes

def preprocess_fallback(image: Image.Image) -> torch.Tensor:
    """Used only if utils.preprocess is unavailable."""
    from torchvision import transforms
    t = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    return t(image)

def predict_font(image: Image.Image, model: torch.nn.Module, class_names: list) -> Tuple[str, float]:
    model_input = (utils.preprocess(image) if HAS_UTILS else preprocess_fallback(image)).unsqueeze(0)
    model_input = model_input.to(torch.float32)
    with torch.no_grad():
        outputs = model(model_input)
        probs = torch.softmax(outputs, dim=1)
        conf, idx = torch.max(probs, 1)
    return class_names[idx.item()], float(conf.item())

# ====================================================
#                 NAV / ROUTING HELPERS
# ====================================================

def get_query_param(name: str, default: Optional[str] = None) -> Optional[str]:
    # Streamlit >= 1.31: st.query_params, older: experimental_get_query_params
    try:
        return st.query_params.get(name, default)
    except Exception:
        try:
            return st.experimental_get_query_params().get(name, [default])[0]
        except Exception:
            return default

def set_query_params(**kwargs):
    try:
        st.query_params.clear()
        for k, v in kwargs.items():
            st.query_params[k] = v
    except Exception:
        st.experimental_set_query_params(**kwargs)

def redirect_to_dashboard():
    st.session_state["page"] = "Dashboard"
    #st.rerun()

def logout_button_sidebar():
    if st.sidebar.button("Logout"):
        st.session_state.clear()
        # Keep user on welcome
        set_query_params(nav="welcome")
        st.rerun()

# ====================================================
#                 PAGES
# ====================================================

def top_navbar():
    st.markdown(
        """
        <div class="navbar-top">
            <a class="navlink" href="?nav=welcome">Home</a>
            <a class="navlink" href="?nav=login">Login</a>
            <a class="navlink" href="?nav=signup">Signup</a>
            <a class="navlink" href="?nav=about">About</a>
        </div>
        """,
        unsafe_allow_html=True
    )

def page_welcome():
    top_navbar()
    st.markdown(
        f"""
        <div class="hero">
            <h1>{APP_BRAND}</h1>
            <p>Identify fonts from images with AI. Record your screen, add mic audio or webcam overlay,
            and manage your work — all in one place.</p>
            <div class="hero-cta">
                <a href="?nav=login">Login</a>
                <a class="secondary" href="?nav=signup">Create Account</a>
                <a class="secondary" href="?nav=about">About Us</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    def page_home():
    # Navbar
     st.markdown("""
    <div class="navbar">
        <a class="navlink" href="#">🏠 Home</a>
        <a class="navlink" href="#">📊 Dashboard</a>
        <a class="navlink" href="#">🧠 Predictions</a>
        <a class="navlink" href="#">📄 Reports</a>
        <a class="navlink" href="#">⚙️ Settings</a>
    </div>
    """, unsafe_allow_html=True)

    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>Welcome to Your AI Health App</h1>
        <p>Smart predictions, clear insights, and modern health analytics — all in one place.</p>
        <div class="hero-cta">
            <a href="#">🚀 Start Now</a>
            <a href="#" class="secondary">📘 Learn More</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")  # Spacer

    # KPI Cards
    cols = st.columns(3)
    with cols[0]:
        st.markdown('<div class="card kpi"><h2>50+</h2><p class="small">Predictions</p></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="card kpi"><h2>98%</h2><p class="small">Accuracy</p></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="card kpi"><h2>200+</h2><p class="small">Users</p></div>', unsafe_allow_html=True)

    st.write("")  # Spacer

    # Features
    cols = st.columns(3)
    with cols[0]:
        st.markdown('<div class="feature">📊<h3>Analytics</h3><p>Track real-time health insights</p></div>', unsafe_allow_html=True)
    with cols[1]:
        st.markdown('<div class="feature">🧠<h3>AI Predictions</h3><p>Early detection of diseases</p></div>', unsafe_allow_html=True)
    with cols[2]:
        st.markdown('<div class="feature">📄<h3>Reports</h3><p>Download and share PDF reports</p></div>', unsafe_allow_html=True)

    st.write("")
    col1, col2, col3, col4 = st.columns(4, gap="large")
    with col1:
        st.markdown("### 🔍 Accurate Recognition")
        st.markdown('<div class="feature small">Upload an image, get the predicted font with confidence.</div>', unsafe_allow_html=True)
    with col2:
        st.markdown("### 🎥 Screen & Webcam")
        st.markdown('<div class="feature small">Record screen, mic audio, and webcam overlay (PiP) — polished and simple.</div>', unsafe_allow_html=True)
    with col3:
        st.markdown("### ⚡ Fast Workflow")
        st.markdown('<div class="feature small">Clean dashboard, persistent accounts, and export-ready results.</div>', unsafe_allow_html=True)
    
        
def page_about():
    top_navbar()
    st.title("ℹ️ About Us")
    st.markdown(
        """
        **Font Identifier** is an AI-powered utility that helps designers, developers, and typographers
        quickly recognize fonts from images or recordings.

        **Highlights**
        - 🎯 High-quality predictions with confidence
        - 🎥 Optional screen recording with mic/webcam overlay
        This app allows you to:  
        - 🎥 Record your **screen with audio narration**  
        - 📸 Capture snapshots  
        - 🔎 Identify fonts (future integration)  
        - 💳 Subscribe for **premium features**

        Built with ❤️ for speed, clarity, and reliability.
        """
    )

def page_signup():
    top_navbar()
    st.title("Create an Account")
    with st.form("signup_form"):
        username = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        pw2 = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Create Account")
    if submit:
        if pw != pw2:
            st.error("Passwords do not match.")
        else:
            ok, msg = create_user(username, pw)
            if ok:
                st.success("✅Account created! Please log in.")
                st.balloons()
                st.markdown('[👉 Go to Login](:?nav=login)', unsafe_allow_html=True)
                
            else:
                st.error(msg)
               

def page_login():
    top_navbar()
    st.title("Welcome back")

    with st.form("login_form"):
        username = st.text_input("Username")
        pw = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")

    if submit:
        if authenticate(username, pw):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.success(f"Welcome back, {username}!")
            st.success("Login successful! Redirecting to your dashboard…")
            redirect_to_dashboard()
            #st.rerun()
        else:
            st.error("Invalid username or password.")


def page_dashboard(model: torch.nn.Module, class_names: list):
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to access the dashboard.")
        set_query_params(nav="login")
        st.stop()

    st.header(f"📊 Dashboard")
    c1, c2, c3 = st.columns(3)
    with c1: st.markdown('<div class="kpi">Current User<br><b>{}</b></div>'.format(st.session_state["username"]), unsafe_allow_html=True)
    with c2: st.markdown('<div class="kpi">Predictions Today<br><b>—</b></div>', unsafe_allow_html=True)
    with c3: st.markdown('<div class="kpi">Status<br><b>Active</b></div>', unsafe_allow_html=True)

    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Run a Prediction")
    uploaded = st.file_uploader("Upload an image of text", type=["jpg", "jpeg", "png"])
    if uploaded:
        image = Image.open(uploaded).convert("RGB")
        st.image(image, caption="Uploaded image", use_container_width=True)
        try:
            name, conf = predict_font(image, model, class_names)
            st.success(f"Predicted Font: **{name}**")
            st.caption(f"Confidence: {conf:.2%}")
        except Exception as e:
            st.error(f"Prediction error: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

def page_subscriptions():
    if not st.session_state.get("logged_in"):
        st.warning("Please log in to subscribe.")
        return

    st.header("💳 Subscription Plans")
    plans = {
        "Free": "Limited features, watermark recordings.",
        "Basic": "$5/month – Unlimited recordings, no watermark.",
        "Premium": "$10/month – All features + priority support."
    }

    for plan, desc in plans.items():
        with st.expander(plan, expanded=(plan == "Basic")):
            st.write(desc)
            if st.button(f"Choose {plan} Plan", key=plan):
                st.session_state["plan"] = plan
                #st.success(f"You selected {plan} plan!")
                #st.info("Redirecting to payment...")
                st.session_state["pending_plan"] = plan
                st.session_state["page"] = "Payment"
                st.rerun()

def page_payment():
    if not st.session_state.get("logged_in"):
        st.warning("Please log in first.")
        return
        
    plan = st.session_state.get("pending_plan", "Free")
    st.header(f"💳 Payment for {plan} Plan")
    
    # Payment method selection with logos
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.image("https://upload.wikimedia.org/wikipedia/commons/0/04/Mastercard-logo.svg", width=80)
        if st.button("MasterCard", key="mc"):
            st.session_state["selected_payment_method"] = "MasterCard"
            st.rerun()

    with col2:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Airtel_Money_Logo.svg/2560px-Airtel_Money_Logo.svg.png", width=80)
        if st.button("Airtel Money", key="am"):
            st.session_state["selected_payment_method"] = "Airtel Money"
            st.rerun()
    with col3:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/f/f9/MTN_Logo.svg/2560px-MTN_Logo.svg.png", width=80)
        if st.button("MTN Mobile Money", key="mom"):
            st.session_state["selected_payment_method"] = "MTN Mobile Money"
            st.rerun()

    with col4:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/PayPal_logo_PNG.png/512px-PayPal_logo_PNG.png", width=80)
        if st.button("PayPal", key="pp"):
            st.session_state["selected_payment_method"] = "PayPal"
            st.rerun()

      # Check if payment method is selected
    if "selected_payment_method" in st.session_state:
        st.success(f"✅ Selected: {st.session_state['selected_payment_method']}")
        
        # Show payment details form
        st.subheader("Payment Details")
        card_number = st.text_input("Card Number", type="password")
        exp_date = st.text_input("Expiration Date (MM/YY)")
        cvv = st.text_input("CVV", max_length=3, type="password")
        
        if st.button("Complete Payment"):
            if card_number and exp_date and cvv:
                st.success(f"✅ Payment processed via {st.session_state['selected_payment']}!")
                update_plan(st.session_state["username"], plan)
                st.session_state["plan"] = plan
                st.session_state.pop("pending_plan", None)
                st.session_state.pop("selected_payment", None)
                st.session_state["page"] = "Dashboard"
                st.rerun()
            else:
                  st.error("❌ Please fill in all payment details.")
    else:
        st.info("👆 Please select a payment method above")

def page_screen_record():
    st.title("📹 Screen Recording with Narration")

    save_dir = "recordings"
    os.makedirs(save_dir, exist_ok=True)

    # Frontend (browser) logic: screen + mic + screenshot
    js_code = """
    <script>
    let mediaRecorder;
    let recordedChunks = [];

    async function startRecording() {
        recordedChunks = [];
        const displayStream = await navigator.mediaDevices.getDisplayMedia({
            video: { mediaSource: "screen" }
        });
        const audioStream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const combinedStream = new MediaStream([
            ...displayStream.getTracks(),
            ...audioStream.getTracks()
        ]);

        mediaRecorder = new MediaRecorder(combinedStream);
        mediaRecorder.ondataavailable = function(e) {
            if (e.data.size > 0) {
                recordedChunks.push(e.data);
            }
        };

        mediaRecorder.onstop = function() {
            let blob = new Blob(recordedChunks, { type: "video/webm" });
            let url = URL.createObjectURL(blob);

            // Create download link
            const a = document.createElement("a");
            a.style.display = "block";
            a.innerText = "⬇️ Download Recording";
            a.href = url;
            a.download = "recording_" + Date.now() + ".webm";
            document.body.appendChild(a);
        };

        mediaRecorder.start();
        document.getElementById("status").innerText = "Recording... 🎥";
    }

    function stopRecording() {
        mediaRecorder.stop();
        document.getElementById("status").innerText = "Stopped ✅";
    }

    async function takeScreenshot() {
        const displayStream = await navigator.mediaDevices.getDisplayMedia({ video: true });
        const track = displayStream.getVideoTracks()[0];
        const imageCapture = new ImageCapture(track);
        const bitmap = await imageCapture.grabFrame();

        const canvas = document.createElement("canvas");
        canvas.width = bitmap.width;
        canvas.height = bitmap.height;
        const ctx = canvas.getContext("2d");
        ctx.drawImage(bitmap, 0, 0, bitmap.width, bitmap.height);

        canvas.toBlob((blob) => {
            let url = URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.style.display = "block";
            a.innerText = "📸 Download Screenshot";
            a.href = url;
            a.download = "screenshot_" + Date.now() + ".png";
            document.body.appendChild(a);
        });

        track.stop();
    }
    </script>

    <button onclick="startRecording()">▶️ Start Recording</button>
    <button onclick="stopRecording()">⏹️ Stop Recording</button>
    <button onclick="takeScreenshot()">📸 Take Screenshot</button>
    <p id="status">Not recording</p>
    """

    components.html(js_code, height=250)


    # TODO: Listen for JS messages (we’ll wire this part next)
    
# ====================================================
#                 SIDEBAR (POST-LOGIN)
# ====================================================

def sidebar_nav_logged_in():
    st.sidebar.title(APP_BRAND)
    st.sidebar.success(f"Hello, {st.session_state['username']}!")
    pages = ["Dashboard", "Screen Record", "Saved Recordings", "Subscriptions", "About"]
    default_idx = pages.index(st.session_state.get("page", "Dashboard")) if st.session_state.get("page", "Dashboard") in pages else 0
    choice = st.sidebar.radio("Navigate", pages, index=default_idx)
    st.session_state["page"] = choice
    logout_button_sidebar()
    return choice

def page_saved_recordings():
    st.title("🎥 Saved Recordings")

    if not os.path.exists(RECORDINGS_DIR):
        st.info("No recordings saved yet.")
        return

    files = [f for f in os.listdir(RECORDINGS_DIR) if f.endswith((".mp4", ".avi", ".mov", ".png", ".jpg"))]

    if not files:
        st.info("No recordings found.")
    else:
        for f in files:
            file_path = os.path.join(RECORDINGS_DIR, f)

            st.write(f"📂 {f}")

            # Show preview
            if f.endswith((".mp4", ".avi", ".mov")):
                st.video(file_path)
            elif f.endswith((".png", ".jpg")):
                st.image(file_path, use_column_width=True)

            col1, col2 = st.columns([1, 1])

            # Download option
            with col1:
                with open(file_path, "rb") as file:
                    st.download_button(
                        label="⬇️ Download",
                        data=file,
                        file_name=f
                    )

            # Delete option
            with col2:
                if st.button(f"🗑️ Delete {f}", key=f"del_{f}"):
                    os.remove(file_path)
                    st.success(f"Deleted {f}")
                    st.experimental_rerun()  # Refresh page to update file list

# ====================================================
#                 MAIN ROUTER
# ====================================================

def main():
    # Ensure DB exists
    init_db()

    # Load model & class names once
    global model, class_names
    model, class_names = load_model_and_classes()
    # If user is logged in → sidebar navigation
    if st.session_state.get("logged_in"):
        choice = sidebar_nav_logged_in()
        if choice == "Dashboard":
            page_dashboard(model, class_names)
        elif choice == "Screen Record":
            page_screen_record()
        elif choice == "Saved Recordings":
            page_saved_recordings()
        elif choice == "Subscriptions":
            page_subscriptions()
        elif choice == "Payment":
            page_payment()
        elif choice == "About":
            page_about()
        return   # ✅ now valid, inside main()

    # If not logged in → top navigation with query params
    nav = get_query_param("nav", "welcome")

    if nav == "login":
        page_login()
    elif nav == "signup":
        page_signup()
    elif nav == "about":
        page_about()
    elif nav == "subscriptions":
        page_subscriptions()
    elif nav == "payment":
        page_payment()
    else:
        page_welcome()

# ====================================================
#                 ENTRY POINT
# ====================================================

if __name__ == "__main__":
    main()
