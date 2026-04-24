# 🗳️ Chaitanya - Voter Awareness AI Assistant

*Vertical:* Election Process Education  
*Challenge:* PromptWars Challenge 2  
*Developed by:* Guggilla Prashanth (Founder & Technical Architect - Digital Daari)

---

## 📝 Project Overview
*Chaitanya* is an advanced AI assistant built to bridge the information gap in the Indian electoral process. Designed for both first-time voters and senior citizens, it provides instant, accurate, and easy-to-understand guidance on voter registration, polling procedures, and constitutional rights.

## ✨ Key Features
- *Bilingual Support:* Communicates fluently in *Telugu* and *English*.
- *Instant Guidance:* Explains complex processes like Form 6 registration and EVM-VVPAT functionality.
- *User-Friendly UI:* Minimalist chat interface for distraction-free learning.
- *Security Focused:* Implemented Streamlit Secrets Management to ensure API keys are never exposed.

## 🛠️ Technical Implementation Details
- *AI Model:* Powered by *Gemini 2.5 Flash* for high-speed, native bilingual processing.
- *Observability:* Integrated *Python Logging* to monitor model initialization and query success rates (Google Cloud best practice).
- *Efficiency:* Utilized *Streamlit Caching* (@st.cache_resource) to optimize performance and reduce latency.
- *Automated Testing:* Comprehensive unit test suite in the /tests folder to validate environment and configuration.

## 🚀 How to Setup

### 1. Clone the Repository
```bash
git clone https://github.com/prashanthguggilla0092/Chaitanya-Voter-AI.git
