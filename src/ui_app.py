import streamlit as st
import requests

API_URL = "http://localhost:8000" # Backend hosted by fastAPI can be accessed from here

st.set_page_config(page_title="Multi-User GenAI Q&A", layout="wide")
st.title("Multi-User Document Search and Q&A System")

email = st.text_input("Enter your email:")

if email:
    if "latest_input" not in st.session_state:
        st.session_state.latest_input = ""

    query = st.text_input("Ask a question:", key="query_input")
    if st.button("Send") and query:
        st.session_state.latest_input = query
        try:
            response = requests.post(
                f"{API_URL}/chat",
                json={"user_email": email, "query": query}
            )
            if response.status_code == 200:
                st.success("Answer received.")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"API error: {e}")

    try:
        hist_response = requests.get(f"{API_URL}/history", params={"user_email": email})
        if hist_response.status_code == 200:
            history = hist_response.json().get("history", [])
            st.markdown("### Conversation History (from backend)")
            for idx, msg in enumerate(history):
                if msg["role"] == "human":
                    st.markdown(f"**You:** {msg['content']}")
                else:
                    st.markdown(f"**AI:** {msg['content']}")
        else:
            st.warning("Could not retrieve history.")
    except Exception as e:
        st.error(f"Error retrieving history: {e}")
