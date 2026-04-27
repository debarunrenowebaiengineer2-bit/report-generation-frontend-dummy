import streamlit as st


def website_form(apify_token):
    st.subheader("Website Input")

    target = st.text_input("Target Domain")
    country = st.text_input("Country", value="in")
    keyword = st.text_input("Keyword (optional)")

    return {
        "apify_token": apify_token,
        "target": target,
        "country": country,
        "keyword": keyword or None
    }


def instagram_form(apify_token):
    st.subheader("Instagram Input")

    username = st.text_input("Username")
    limit = st.slider("Results Limit", 1, 100, 12)

    return {
        "apify_token": apify_token,
        "username": username,
        "results_limit": limit
    }


def visual_form():
    st.subheader("Upload Screenshots")

    website_file = st.file_uploader("Website Screenshot", type=["png", "jpg"])
    insta_file = st.file_uploader("Instagram Screenshot", type=["png", "jpg"])

    return website_file, insta_file