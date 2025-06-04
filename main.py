import streamlit as st
from newspaper import Article

# Streamlit UI
st.set_page_config(page_title="TopicWise – AI Research Assistant")
st.title("🧠 TopicWise – AI Research Assistant")
st.subheader("Generate structured research briefs from preloaded content")

topic = st.text_input("Enter a topic you'd like to research:")

# 🔁 Hardcoded list of article links (SerpAPI mock)
def get_articles(query):
    return [
        "https://fintech.global/2025/02/27/how-ai-and-automation-are-transforming-e-invoicing-in-2025/",
        "https://blog.axway.com/newsroom/e-invoicing-mandates-implementing-ai-frameworks-and-a-file-transfer-secret-weapon-latest-from-the-axway-blog",
        "https://www.comarch.com/trade-and-services/data-management/news/ai-capabilities-in-the-context-of-mandatory-invoice-exchange/",
        "https://www.ascendsoftware.com/blog/einvoicing-mandates",
        "https://easy-software.com/en/newsroom/ai-in-accounting-better-data-new-opportunities-for-companies/"
    ]

# 🧠 Hardcoded summaries per domain
def summarize(text, topic, url=None):
    mock_summaries = {
        "fintech.global": """- AI and automation are enabling real-time invoice validation, reducing fraud and human errors across finance departments.
- Predictive analytics are being used to forecast payment timelines, enhancing cash flow visibility for CFOs.
- Integration with ERP systems is becoming seamless through AI-driven APIs and connectors.
- E-invoicing compliance is increasingly automated through AI that adapts to jurisdictional tax rules.""",

        "axway.com": """- AI frameworks are being layered onto traditional B2B integration platforms to enforce evolving e-invoicing mandates.
- The article emphasizes the importance of secure file transfer as the “glue” between AI analysis and invoice submission workflows.
- Compliance strategies now include continuous monitoring powered by machine learning.
- Companies need cross-functional teams to manage both IT integration and regulatory interpretation.""",

        "comarch.com": """- AI is being embedded into invoice validation engines to catch data mismatches and schema compliance issues.
- Adaptive learning systems can now detect new fraud patterns in real-time invoice exchange.
- AI capabilities are helping businesses prepare for mandatory B2G and B2B invoice exchange in Europe.
- Human oversight remains essential, especially during transitional compliance rollouts.""",

        "ascendsoftware.com": """- Governments are accelerating mandates for e-invoicing, pushing enterprises to adopt automation.
- AI simplifies onboarding for vendors by interpreting and correcting invoice formats automatically.
- Intelligent workflows are reducing invoice approval times from days to hours.
- Enterprises are prioritizing AI tools that reduce manual intervention while maintaining audit trails.""",

        "easy-software.com": """- AI is improving data quality in accounting systems, which directly enhances invoice accuracy.
- Automation now covers extraction, matching, and error detection — creating "touchless invoicing."
- Mid-sized businesses are benefiting from pre-trained models without needing in-house data science teams.
- AI opens up strategic opportunities in spend analysis and working capital optimization."""
    }

    for domain in mock_summaries:
        if domain in url:
            return mock_summaries[domain]

    return f"🔧 [MOCK] Summary for topic: {topic} (text length: {len(text)})"

# ✅ Article extraction
def extract_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

# 🧪 App logic
if topic:
    with st.spinner("🔍 Generating summaries... please wait"):
        links = get_articles(topic)
        all_summaries = []

        for link in links:
            try:
                article_text = extract_article_text(link)
                summary = summarize(article_text, topic, url=link)
                all_summaries.append((link, summary))
            except Exception as e:
                print(f"Error for {link}: {e}")
                continue

    if all_summaries:
        st.header("📄 Research Summary")
        for link, summary in all_summaries:
            st.markdown(f"### 🔗 Source: [{link}]({link})")
            st.markdown(summary)
    else:
        st.error("No summaries could be generated.")
