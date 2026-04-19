import streamlit as st
import requests

# -----------------------------
# API URL
# -----------------------------
API_URL = "http://127.0.0.1:8000/chat"

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(page_title="Portfolio RAG Bot", page_icon="🤖")

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.title("👤 Muhammad Haris")
    st.write("AI Engineer")

    st.markdown("### 🔗 Connect")
    st.markdown("- 📧 harisaslam.se@gmail.com")
    st.markdown(
        "- 🔗 [LinkedIn](https://www.linkedin.com/in/muhammad-haris-14803022b/)")
    st.markdown(
        "- 💼 [Upwork](https://www.upwork.com/freelancers/~01dcf054e52fdc82e0)")
    st.markdown("- 🎯 [Fiverr](https://www.fiverr.com/sellers/harisaslam242)")
    st.markdown("- 💻 [GitHub](https://github.com/harryx65)")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -----------------------------
# Main UI
# -----------------------------
st.title("🤖 Portfolio RAG Chatbot")
st.write("Ask questions about Muhammad Haris, his skills, projects, and background.")

# -----------------------------
# Suggested questions
# -----------------------------
st.markdown("### 💡 Try asking:")

cols = st.columns(2)

suggestions = [
    "What skills does Haris have?",
    "List all his projects",
    "Where did Haris study?",
    "How can I contact Haris?"
]

for i, q in enumerate(suggestions):
    if cols[i % 2].button(q):
        st.session_state.input = q

# -----------------------------
# Chat history
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -----------------------------
# Chat input
# -----------------------------
question = st.chat_input("Ask something about Haris...")

# Handle suggestion click
if "input" in st.session_state:
    question = st.session_state.input
    del st.session_state.input

# -----------------------------
# When user asks a question
# -----------------------------
if question:
    # Show user message
    with st.chat_message("user"):
        st.markdown(question)

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    # 🔥 CALL FASTAPI
    try:
        response = requests.post(
            API_URL,
            json={"question": question}
        )

        data = response.json()
        answer = data.get("answer", "No answer found.")

    except Exception as e:
        answer = "⚠️ Error connecting to API. Make sure FastAPI is running."

    # Show assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })
