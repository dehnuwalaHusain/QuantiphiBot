#  Multi-User Document Search and Conversational Q&A System
- Users are be able to query the system and retrieve relevant excerpts from documents they have access to.
- The system provides a conversational experience by maintaining context from previous user queries and answers.
- Ensures that queries and responses are isolated per user, meaning User A cannot see answers from documents User B has access to.
- A basic UI is included where users can:
  - Log in or simulate access using their email IDs.
  - Submit queries and view retrieved answers.

# How to deploy
Install the dependencies using
`pip3 install -r requirements.txt`

Create an API key from Groq and assign it as a system variable - 
`export GROQ_API_KEY=<your-key-here>`

Run the backend API system, implemented via FastAPI as - 

In terminal 1, we will run the backend API system, implemented via FastAPI  -
`cd src`
`uvicorn app:app --reload --port 8000`

In a second terminal, we will launch streamlit to mimic a UI -
`cd src`
`python3 -m streamlit run ui_app.py`
