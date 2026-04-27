import streamlit as st
from api.client import APIClient
from ui.forms import website_form, instagram_form, visual_form
from ui.renderers import render_section, render_full_report, render_json

st.set_page_config(page_title="Digital Presence Dashboard", layout="wide")

st.title("📊 Digital Presence Report Dashboard")

# Sidebar config
st.sidebar.header("🔧 Configuration")

backend_url = st.sidebar.text_input(
    "Backend URL",
    value="http://72.62.247.229:8004"
)

apify_token = st.sidebar.text_input(
    "Apify Token",
    type="password",
    placeholder="Paste your Apify API key here"
)

st.sidebar.markdown("---")

st.sidebar.subheader("⚙️ Setup Guide")
st.sidebar.markdown("""
1. Get Apify API Token  
2. Replace actor names in backend  
3. Start FastAPI server  
4. Enter token here  
5. Run analysis  

**Actor placeholders (replace in backend):**
- https://console.apify.com/actors/3R9pWxyCy9C2hRJfY/input?addFromActorId=3R9pWxyCy9C2hRJfY
- https://console.apify.com/actors/dSCLg0C3YEZ83HzYX/input?addFromActorId=dSCLg0C3YEZ83HzYX
- https://console.apify.com/actors/jWD4G57HhqYY0mFhd/input?addFromActorId=jWD4G57HhqYY0mFhd
- https://console.apify.com/actors/yUvj8W0M4T0HhZKyA?addFromActorId=yUvj8W0M4T0HhZKyA  
""")

client = APIClient(backend_url)

tabs = st.tabs([
    "🏠 Overview",
    "🌐 Website Audit",
    "📸 Instagram Audit",
    "🎨 Visual Brand Match"
])

# -----------------------------
# Overview
# -----------------------------
with tabs[0]:
    st.header("Overview")
    st.info("Use the tabs to generate reports.")

# -----------------------------
# Website Audit
# -----------------------------
with tabs[1]:
    st.header("Website Audit")

    form_data = website_form(apify_token)


    st.divider()

    st.subheader("Individual Sections")

    if st.button("Authority & Visibility"):
        with st.spinner("Fetching Authority & Visibility section..."):
            try:
                res = client.website_section("authority-visibility", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Authority & Visibility: {e}")

    if st.button("AI Visibility"):
        with st.spinner("Fetching AI Visibility section..."):
            try:
                res = client.website_section("ai-visibility", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load AI Visibility: {e}")

    if st.button("Keyword Intent"):
        with st.spinner("Fetching Keyword Intent section..."):
            try:
                res = client.website_section("keyword-intent", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Keyword Intent: {e}")

    if st.button("Technical Health"):
        with st.spinner("Fetching Technical Health section..."):
            try:
                res = client.website_section("technical-health", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Technical Health: {e}")

    if st.button("Backlink Profile"):
        with st.spinner("Fetching Backlink Profile section..."):
            try:
                res = client.website_section("backlink-profile", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Backlink Profile: {e}")

# -----------------------------
# Instagram Audit
# -----------------------------
with tabs[2]:
    st.header("Instagram Audit")

    form_data = instagram_form(apify_token)


    st.divider()

    if st.button("Profile Section"):
        with st.spinner("Fetching Instagram Profile section..."):
            try:
                res = client.instagram_section("profile", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Profile section: {e}")

    if st.button("Follower Quality"):
        with st.spinner("Fetching Follower Quality section..."):
            try:
                res = client.instagram_section("follower-quality", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Follower Quality section: {e}")

    if st.button("Engagement"):
        with st.spinner("Fetching Engagement section..."):
            try:
                res = client.instagram_section("engagement", form_data)
                render_section(res)
            except Exception as e:
                st.error(f"Failed to load Engagement section: {e}")

# -----------------------------
# Visual Brand Match
# -----------------------------
with tabs[3]:
    st.header("Visual Brand Match")

    website_file, insta_file = visual_form()

    if st.button("Analyze Brand Match"):
        if website_file and insta_file:
            with st.spinner("Analyzing brand match..."):
                try:
                    res = client.visual_brand_match(website_file, insta_file)
                    render_json(res)
                except Exception as e:
                    st.error(f"Failed to analyze brand match: {e}")
        else:
            st.warning("Upload both images.")