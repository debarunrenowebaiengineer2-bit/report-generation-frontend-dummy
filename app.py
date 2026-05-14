import streamlit as st
import requests
import streamlit.components.v1 as components

# ==========================================
# Premium App Configuration
# ==========================================
st.set_page_config(
    page_title="Digital Presence Auditor",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded"
)

API_BASE_URL = "http://localhost:8000"

# ==========================================
# High-End Custom CSS
# ==========================================
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #1e293b;
        }

        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        .stApp { background-color: #fcfcfd; }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0f172a;
            color: white;
        }
        [data-testid="stSidebar"] * {
            color: #f1f5f9 !important;
        }

        /* Form / Container Styling */
        div[data-testid="stForm"] {
            background-color: #ffffff;
            padding: 30px;
            border-radius: 16px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            max-width: 900px;
            margin: 0 auto;
        }

        /* Buttons */
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            height: 55px;
            font-weight: 600;
            background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-1px);
            box-shadow: 0 10px 15px -3px rgba(79, 70, 229, 0.4);
        }

        .main-title {
            text-align: center;
            font-size: 2.5rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# Helper Function
# ==========================================
def run_audit(endpoint: str, payload: dict = None, files: dict = None):
    with st.spinner("✨ AI is analyzing... please wait."):
        try:
            if files:
                response = requests.post(f"{API_BASE_URL}{endpoint}", files=files)
            else:
                response = requests.post(f"{API_BASE_URL}{endpoint}", json=payload)
                
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    st.toast("Analysis Complete!", icon="✅")
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown('<div style="background: white; border-radius: 20px; border: 1px solid #e2e8f0; box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
                    components.html(data.get("html_report", ""), height=1500, scrolling=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.error(f"Error: {data.get('detail')}")
            else:
                st.error(f"Server Error: {response.status_code}")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

# ==========================================
# Sidebar Module Selector
# ==========================================
with st.sidebar:
    st.markdown("## 💎 Auditor Pro")
    module = st.radio("Analysis Module", [
        "🚀 Full Analysis",
        "🌐 Website SEO",
        "📸 Instagram Audit",
        "🎨 Visual Brand Match"
    ])
    st.markdown("---")
    apify_token = st.text_input("Apify Token", type="password")

# ==========================================
# UI Logic
# ==========================================
st.markdown(f'<h1 class="main-title">{module}</h1>', unsafe_allow_html=True)

if not apify_token and module != "🎨 Visual Brand Match":
    st.info("👈 Please enter your Apify Token in the sidebar to begin.")
else:
    with st.form("audit_inputs"):
        if module == "🚀 Full Analysis":
            domain = st.text_input("Domain", placeholder="pureorganiczone.com")
            ig_user = st.text_input("Instagram Username", placeholder="pureorganiczone")
            if st.form_submit_button("GENERATE COMPLETE PDF-STYLE REPORT"):
                run_audit("/report/generate-full", {
                    "domain": domain, "ig_username": ig_user.replace("@",""), 
                    "apify_token": apify_token
                })

        elif module == "🌐 Website SEO":
            domain = st.text_input("Domain", placeholder="pureorganiczone.com")
            if st.form_submit_button("ANALYZE WEBSITE ANATOMY"):
                run_audit("/report/generate-seo", {"domain": domain, "apify_token": apify_token})

        elif module == "📸 Instagram Audit":
            ig_user = st.text_input("Username", placeholder="pureorganiczone")
            limit = st.slider("Posts to analyze", 10, 50, 20)
            if st.form_submit_button("ANALYZE SOCIAL ANATOMY"):
                run_audit("/report/generate-instagram", {
                    "ig_username": ig_user.replace("@",""), 
                    "ig_results_limit": limit, 
                    "apify_token": apify_token
                })

        elif module == "🎨 Visual Brand Match":
            col1, col2 = st.columns(2)
            with col1: web_img = st.file_uploader("Website Screenshot", type=["png", "jpg"])
            with col2: ig_img = st.file_uploader("Instagram Screenshot", type=["png", "jpg"])
            if st.form_submit_button("RUN VISION AI COMPARISON"):
                if web_img and ig_img:
                    files = {
                        "website_screenshot": (web_img.name, web_img, web_img.type),
                        "instagram_screenshot": (ig_img.name, ig_img, ig_img.type)
                    }
                    run_audit("/report/visual/brand-match", files=files)