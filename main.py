import streamlit as st
import requests
from newspaper import Article
import newspaper
import os
import tempfile

# ✅ Fix Windows temp directory issue
custom_temp_dir = os.path.join(tempfile.gettempdir(), "newspaper_custom")
if not os.path.exists(custom_temp_dir):
    os.makedirs(custom_temp_dir)

newspaper.settings.SCRAPER_TEMP_DIR = custom_temp_dir
newspaper.settings.CACHE_DIRECTORY = os.path.join(custom_temp_dir, "cache")
newspaper.settings.MEMOIZE_ARTICLES = False

# Streamlit UI
st.set_page_config(page_title="Wise – AI Research Assistant")
st.title("Wise – AI Research Assistant")
st.subheader("Generate structured research briefs with source references")

topic = st.text_input("Enter a topic you'd like to research:")

# 🔍 Live article search via SerpAPI
def get_articles(query):
    SERPAPI_KEY = st.secrets.get("SERPAPI_KEY") or os.getenv("SERPAPI_KEY")
    if not SERPAPI_KEY:
        return []

    search_url = "https://serpapi.com/search"
    params = {
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY,
        "num": 5,
    }

    try:
        res = requests.get(search_url, params=params)
        results = res.json().get("organic_results", [])
        return [r["link"] for r in results if "link" in r]
    except Exception as e:
        return []

# ✂️ Hugging Face summarization
def summarize(text):
    HUGGINGFACE_API_TOKEN = st.secrets.get("HUGGINGFACE_API_TOKEN") or os.getenv("HUGGINGFACE_API_TOKEN")
    if not HUGGINGFACE_API_TOKEN:
        return "❌ Missing Hugging Face API Token"

    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_TOKEN}"}
    payload = {
        "inputs": text[:1000],  # Truncate for speed and safety
        "parameters": {"min_length": 60, "max_length": 300}
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        return f"❌ Hugging Face API Error {response.status_code}: {response.text}"

    try:
        return response.json()[0]["summary_text"]
    except Exception as e:
        return f"❌ Error parsing response: {e}"

# 📄 Extract clean text
def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# 🧪 App logic
if topic:
    with st.spinner("🔍 Searching and summarizing..."):
        links = get_articles(topic)
        all_summaries = []

        for link in links:
            try:
                article_text = extract_article_text(link)
                summary = summarize(article_text)
                all_summaries.append((link, summary))
            except Exception as e:
                all_summaries.append((link, f"❌ Error: {e}"))
                continue

    if all_summaries:
        st.header("📄 Research Summary")
        for link, summary in all_summaries:
            st.markdown(f"### 🔗 Source: [{link}]({link})")
            st.markdown(summary)
    else:
        st.error("No summaries could be generated. Try another topic or check your API keys.")
