import os
import streamlit as st
import google.generativeai as genai

# Secrets నుండి కీని తీసుకోవడం
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Page configuration
st.set_page_config(
    page_title="Chaitanya - Voter Awareness AI",
    page_icon="🗳️",
    layout="centered"
)

# Main Heading
st.title("🗳️ చైతన్య - ఓటరు అవగాహన అసిస్టెంట్ (Chaitanya Voter Awareness AI)")

# Welcome message
st.markdown("""
Welcome! I am **Chaitanya**, your AI assistant dedicated to guiding Indian citizens through the election process. 
I can help you with topics like voter registration, checking your name in the voter list, understanding EVMs, and more. 

నమస్కారం! నేను **చైతన్య**, ఎన్నికల ప్రక్రియ ద్వారా భారతీయ పౌరులకు మార్గనిర్దేశం చేయడానికి అంకితమైన మీ AI అసిస్టెంట్‌ని. 
మీరు నన్ను ఇంగ్లీష్ లేదా తెలుగులో (English or Telugu) ప్రశ్నలు అడగవచ్చు!
""")

# Sidebar for API Key and Info
with st.sidebar:
    st.header("⚙️ Configuration")
    # మొదట ఎన్విరాన్మెంట్ వేరియబుల్ ఉందేమో చూస్తుంది
    api_key = os.getenv("GEMINI_API_KEY")

    # ఒకవేళ లేకపోతేనే యూజర్‌ని అడుగుతుంది
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

# System Instruction for the Gemini Model
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

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask your question here / మీ ప్రశ్నను ఇక్కడ అడగండి"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    if not api_key:
        with st.chat_message("assistant"):
            st.error("Please enter your Gemini API Key in the sidebar to proceed.")
    else:
        try:
            # Configure Gemini API
            genai.configure(api_key=api_key)
            
            # Initialize the model with system instruction
            # Using gemini-2.5-flash as it natively supports system instructions 
            model = genai.GenerativeModel(
            model_name="models/gemini-2.5-flash",
            system_instruction=system_instruction
        )
            
            # Create a chat session with history
            # Convert streamlit history format to google generativeai format
            history = []
            for msg in st.session_state.messages[:-1]: # Exclude the current prompt
                role = "user" if msg["role"] == "user" else "model"
                history.append({"role": role, "parts": [msg["content"]]})
                
            chat_session = model.start_chat(history=history)

            # Display assistant response in chat message container
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                with st.spinner("Thinking..."):
                    response = chat_session.send_message(prompt)
                message_placeholder.markdown(response.text)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            with st.chat_message("assistant"):
                st.error(f"An error occurred: {str(e)}")
