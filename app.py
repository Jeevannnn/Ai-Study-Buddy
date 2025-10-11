import streamlit as st
import google.generativeai as genai
import json
import pathlib
import toml

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Study Buddy",
    page_icon="🎓",
    layout="wide",
)

# --- Custom CSS for Styling ---
def load_css():
    st.markdown("""
        <style>
            /* Main app background */
            .stApp {
                background-color: #0a0a14;
            }

            /* Chat bubbles */
            .stChatMessage {
                border-radius: 20px;
                padding: 1rem 1.5rem;
                margin-bottom: 1rem;
                box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            }
            [data-testid="chat-message-container"]:has(div[data-testid="stChatMessageContent-user"]) {
                background-color: #2a2a40; /* User bubble color */
            }
            [data-testid="chat-message-container"]:has(div[data-testid="stChatMessageContent-assistant"]) {
                background-color: #1c1c2e; /* Assistant bubble color */
            }

            /* Buttons */
            .stButton>button {
                border-radius: 50px;
                border: 2px solid #6C22F8;
                background: linear-gradient(45deg, #6C22F8, #A369FF);
                color: white;
                padding: 0.75rem 1.5rem;
                font-weight: bold;
                transition: all 0.2s ease-in-out;
            }
            .stButton>button:hover {
                transform: scale(1.05);
                box-shadow: 0 0 15px #6C22F8;
            }

            /* Tabs */
            .stTabs [data-baseweb="tab"] {
                border-radius: 8px 8px 0 0;
                padding: 10px 20px;
                background-color: #1c1c2e;
            }
            .stTabs [data-baseweb="tab"][aria-selected="true"] {
                background-color: #2a2a40;
                border-bottom: 3px solid #6C22F8;
            }
            
            /* Text Input / Chat Input */
            .stTextInput>div>div>input, .stChatInput>div>div>input {
                border-radius: 50px;
                background-color: #1c1c2e;
                border: 2px solid #2a2a40;
                color: #FAFAFA;
            }
        </style>
    """, unsafe_allow_html=True)

# Apply the custom CSS
load_css()

# --- API Key Configuration ---
# ... (The rest of your API key logic remains the same)
def get_key_from_secrets():
    secrets_path = pathlib.Path(".streamlit/secrets.toml")
    if secrets_path.exists():
        secrets = toml.load(secrets_path)
        return secrets.get("GEMINI_API_KEY")
    return None

api_key = get_key_from_secrets()
if not api_key:
    st.error("Gemini API key not found. Please add it to your .streamlit/secrets.toml file.", icon="🚨")
    st.stop()

genai.configure(api_key=api_key)

# --- Helper Function to Call Gemini API ---
def get_gemini_response(prompt, model_name='gemini-flash-latest'):
    try:
        model = genai.GenerativeModel(model_name)
        with st.spinner("Thinking..."):
            response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        st.error(f"An error occurred with the Gemini API: {e}")
        st.stop()

# --- Main Application UI ---
st.title(" AI Study Buddy")
st.write("Your personal AI-powered assistant to help you with your studies.")

tab1, tab2, tab3 = st.tabs(["**Concept Explainer**", "**Notes Summarizer**", "**Quiz Generator**"])

# --- TAB 1: Conversational Explainer ---
with tab1:
    st.header("📚 Explain a Complex Concept")
    # ... (rest of the tab logic is the same)
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hi! What complex topic can I help you understand today?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask me anything about your topic..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        full_prompt = "You are a friendly tutor. Based on the history, answer the student's latest question.\n\n"
        for msg in st.session_state.messages:
            full_prompt += f'{msg["role"].capitalize()}: {msg["content"]}\n'
        
        response_text = get_gemini_response(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
        st.rerun()

# --- TAB 2: Conversational Notes Summarizer ---
with tab2:
    st.header("📝 Summarize and Discuss Your Notes")
    # ... (rest of the tab logic is the same)
    if "summarize_messages" not in st.session_state:
        st.session_state.summarize_messages = [{"role": "assistant", "content": "Hello! Paste your notes here and I'll summarize them for you."}]

    for message in st.session_state.summarize_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Paste your notes or ask a follow-up question..."):
        st.session_state.summarize_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        full_prompt = "You are an expert study assistant. Summarize the provided notes and answer any follow-up questions.\n\n"
        for msg in st.session_state.summarize_messages:
            full_prompt += f'{msg["role"].capitalize()}: {msg["content"]}\n'
        
        response_text = get_gemini_response(full_prompt)
        with st.chat_message("assistant"):
            st.markdown(response_text)
        st.session_state.summarize_messages.append({"role": "assistant", "content": response_text})
        st.rerun()

# --- TAB 3: Generate a Quiz ---
with tab3:
    st.header("🧠 Generate a Quiz")
    # ... (rest of the tab logic is the same)
    if 'quiz_results' in st.session_state:
        results = st.session_state['quiz_results']
        st.success(f"**Your final score: {results['score']}/{results['total']}**")
        st.markdown("---")
        st.subheader("Review Your Answers:")
        for item in results['review']:
            st.markdown(item)
        if st.button("Take Another Quiz"):
            for key in ['quiz_results', 'quiz_data', 'quiz_topic', 'user_answers']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    elif 'quiz_data' not in st.session_state:
        with st.form("quiz_topic_form"):
            quiz_topic = st.text_input("Enter the topic for the quiz:", key="quiz_topic_input")
            generate_button = st.form_submit_button("Generate Quiz")

            if generate_button and quiz_topic:
                prompt = f"Generate a 10-question multiple-choice quiz on '{quiz_topic}'. Output MUST be a valid JSON object..."
                # (rest of the quiz generation logic is the same)
                quiz_json_str = get_gemini_response(prompt)
                try:
                    if quiz_json_str.strip().startswith("```json"):
                        quiz_json_str = quiz_json_str.strip()[7:-4]
                    
                    quiz_data = json.loads(quiz_json_str)
                    st.session_state['quiz_topic'] = quiz_topic
                    st.session_state['quiz_data'] = quiz_data['questions']
                    st.session_state['user_answers'] = [None] * len(quiz_data['questions'])
                    st.rerun()

                except (json.JSONDecodeError, KeyError) as e:
                    st.error(f"Failed to generate a valid quiz. Please try again. Error: {e}")
                    st.text_area("AI Response for Debugging:", quiz_json_str)

    if 'quiz_data' in st.session_state:
        st.markdown("---")
        st.subheader(f"Quiz on: {st.session_state['quiz_topic']}")

        with st.form("quiz_answers_form"):
            for i, q in enumerate(st.session_state['quiz_data']):
                st.markdown(f"**Question {i+1}:** {q['question']}")
                st.session_state['user_answers'][i] = st.radio(
                    "Your answer:", q['options'], key=f"q{i}", label_visibility="collapsed", index=None
                )
            
            submit_answers_button = st.form_submit_button("Submit Quiz")
            
            if submit_answers_button:
                score = 0
                correct_answers_list = []
                for i, q in enumerate(st.session_state['quiz_data']):
                    user_answer = st.session_state['user_answers'][i]
                    correct_answer = q['answer']
                    
                    if user_answer == correct_answer:
                        score += 1
                        correct_answers_list.append(f"✅ **Question {i+1}: Correct!** The answer was **{correct_answer}**.")
                    else:
                        correct_answers_list.append(f"❌ **Question {i+1}: Incorrect.** You chose '{user_answer}'. The correct answer was **'{correct_answer}'**.")
                
                st.session_state['quiz_results'] = {
                    "score": score,
                    "total": len(st.session_state['quiz_data']),
                    "review": correct_answers_list
                }

                del st.session_state['quiz_data']
                del st.session_state['quiz_topic']
                del st.session_state['user_answers']
                
                st.rerun()

