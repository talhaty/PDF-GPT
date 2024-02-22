import os
import streamlit as st
from streamlit_chat import message
from fpdf import FPDF


class ChatHistory:
    
    def __init__(self):
        self.history = st.session_state.get("history", [])
        st.session_state["history"] = self.history

    def default_greeting(self):
        return "Hey PDF GPT ! 👋"

    def default_prompt(self, topic):
        return f"Hello ! Ask me anything 🤗"

    def initialize_user_history(self):
        st.session_state["user"] = [self.default_greeting()]

    def initialize_assistant_history(self, uploaded_file):
        st.session_state["assistant"] = [self.default_prompt(uploaded_file)]

    def initialize(self, uploaded_file):
        if "assistant" not in st.session_state:
            self.initialize_assistant_history(uploaded_file)
        if "user" not in st.session_state:
            self.initialize_user_history()

    def reset(self, uploaded_file):
        st.session_state["history"] = []
        
        self.initialize_user_history()
        self.initialize_assistant_history(uploaded_file)
        st.session_state["reset_chat"] = False

    def append(self, mode, message):
        st.session_state[mode].append(message)

    def generate_messages(self, container):
        if st.session_state["assistant"]:
            with container:
                for i in range(len(st.session_state["assistant"])):
                    message(
                        st.session_state["user"][i],
                        is_user=True,
                        key=f"history_{i}_user",
                        avatar_style="big-smile",
                    )
                    message(st.session_state["assistant"][i], key=str(i), avatar_style="thumbs")



    def save_as_pdf(self, file_path):
        print(file_path)

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=8)

        pdf.cell(200, 10, txt="Chat History", ln=True, align='C')

        for i, (question, answer) in enumerate(self.history):
            pdf.ln(10)  # Add a line break
            pdf.multi_cell(0,4, txt=f"Question:  {self.format_text(question)}")
            pdf.multi_cell(0,4, txt=f"Answer:  {self.format_text(answer)}")

        pdf.output(file_path)

    def format_text(self, text):
        # Ensure text is a string
        text_str = " ".join(map(str, text)) if isinstance(text, tuple) else str(text)
        return text_str




    def save(self, pdf_file_path):
        self.save_as_pdf(pdf_file_path)
