import streamlit as st
import google.generativeai as genai
import logging
import os

# --- Logging Setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

api_key = st.secrets.get("GEMINI_API_KEY")

# --- Page configuration ---
st.set_page_config(
    page_title="Chaitanya - Voter Awareness AI",
    page_icon="🗳️",
    layout="centered"
)

# --- AI Model Initialization
@st.cache_resource
def get_model(api_key):
    try:
        # 1. logging and configuration
        logger.info("Chaitanya AI Model Initializing...")
        genai.configure(api_key=api_key)
        
        system_instruction = """
You are "Chaitanya", a helpful and knowledgeable AI assistant dedicated to guiding Indian citizens through the election process. Answer questions clearly, accurately, and politely. You must be able to explain concepts in both Telugu (using Telugu script) and English, depending on the user's input language. If you are unsure of an answer, recommend the user check the official Election Commission of India (ECI) website.

Core topics to cover:
- How to check your name in the Voter List.
- Process for New Voter Registration (online and offline forms).
- Explaining EVM (Electronic Voting Machine) and VVPAT (Voter Verifiable Paper Audit Trail).
- Steps to take inside a Polling Station on voting day.
- General Election Timeline and stages.
- Candidate Information.
- Model Code of Conduct.
"""
        # 2. model object creation
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=system_instruction
        )
        return model
    except Exception as e:
        # 3. error logging and streamlit notification
        logger.error(f"Model Load Error: {str(e)}")
        st.error("AI మోడల్‌ని లోడ్ చేయడంలో సమస్య ఏర్పడింది. దయచేసి మీ API Key మరియు ఇంటర్నెట్ కనెక్షన్ సరిచూసుకోండి.")
        return None

# --- Main Heading ---
st.title("🗳️ చైతన్య - ఓటరు అవగాహన అసిస్టెంట్ (Chaitanya Voter Awareness AI)")

# --- Welcome message ---
st.markdown("""
Welcome! I am **Chaitanya**, your AI assistant dedicated to guiding Indian citizens through the election process. 
I can help you with topics like voter registration, checking your name in the voter list, understanding EVMs, and more. 

నమస్కారం! నేను **చైతన్య**, ఎన్నికల ప్రక్రియ ద్వారా భారతీయ పౌరులకు మార్గనిర్దేశం చేయడానికి అంకితమైన మీ AI అసిస్టెంట్‌ని. 
మీరు నన్ను ఇంగ్లీష్ లేదా తెలుగులో (English or Telugu) ప్రశ్నలు అడగవచ్చు!
""")

# --- Sidebar for API Key and Info ---
with st.sidebar:
    st.header("⚙️ Configuration")

    if not api_key:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            api_key = st.text_input(
                "Enter your Gemini API Key:", 
                type="password", 
                help="Get your API key from Google AI Studio to start chatting."
            )
    
    st.markdown("---")
    st.markdown("""
    **📚 Topics I can help with:**
    - Checking name in Voter List
    - New Voter Registration (Online/Offline)
    - EVM and VVPAT explanation
    - Polling Station steps
    - General Election Timeline
    - Candidate Information
    - Model Code of Conduct
    """)

# --- Initialize session state for chat history ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- Display chat messages ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- React to user input ---
if prompt := st.chat_input("Ask your question here / మీ ప్రశ్నను ఇక్కడ అడగండి"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        with st.chat_message("assistant"):
            st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    else:
        try:
            model = get_model(api_key)
            
            if model:
                # Chat history format
                history = []
                for msg in st.session_state.messages[:-1]:
                    role = "user" if msg["role"] == "user" else "model"
                    history.append({"role": role, "parts": [msg["content"]]})
                    
                chat_session = model.start_chat(history=history)

                # Response
                with st.chat_message("assistant"):
                    message_placeholder = st.empty()
                    with st.spinner("Thinking..."):
                        response = chat_session.send_message(prompt)
                        logger.info("User query processed and response generated successfully.")
                    message_placeholder.markdown(response.text)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            logger.error(f"Chat Error: {str(e)}")
            with st.chat_message("assistant"):
                st.error(f"An error occurred during chat: {str(e)}")
