from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import streamlit as st
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Retrieve the API key from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

"""
def generate_medical_report(file):
    prompt_template = PromptTemplate(

            template = f""""You are a medical assistant AI. Based on the following responses to medical questions, generate a detailed and structured medical report. The report should be formatted in the following sections:
            """)
    chain = LLMChain(prompt=prompt_template)
    reformulated_question = chain.run({"question": "you have to generate a medical report"})
    return reformulated_question.strip()
"""
class SingleQuestionReformulationAgent:
    def __init__(self, llm):
        self.llm = llm

    def reformulate_question(self, question):
        """
        Reformulates a given question to make it clearer and more precise.
        """
        # Define the prompt template
        prompt_template = PromptTemplate(
            input_variables=["question"],
            template="Reformulate the following question to make it clearer and more precise , Imagine you are interacting with a woman who may be at risk for breast cancer. Your goal is to guide her through a self-assessment process by asking relevant and thoughtful questions. Approach the conversation with sensitivity and care. Avoid using harsh or overly clinical language that might cause alarm or discomfort. Instead, prioritize empathy, understanding, and support. Based on her responses, adapt your questions to ensure they are appropriate and considerate. For example, if she mentions pain or discomfort, gently inquire further to gather more information without being intrusive. At every step, reassure her that her well-being is your priority and that the process is designed to help identify potential concerns early. End the conversation by summarizing the findings, and invite her to ask any additional questions or note she may have."
        )
        chain = LLMChain(prompt=prompt_template)
        reformulated_question = chain.run({"question": question})
        return reformulated_question.strip()



# Initialize application state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "current_question_index" not in st.session_state:
    st.session_state["current_question_index"] = 0
if "questions_done" not in st.session_state:
    st.session_state["questions_done"] = False
if "conversation_log" not in st.session_state:
    st.session_state["conversation_log"] = ""
if "responses" not in st.session_state:
    st.session_state["responses"] = {}

# User interface
st.title("Post-Self-Examination Questionnaire")

# Initial question
if st.session_state["current_question_index"] == 0:
    st.chat_message("assistant").write("Are you ready to begin?")

    if user_input := st.chat_input("Response:"):
        if user_input.strip().lower() in ["yes", "oui"]:
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["current_question_index"] += 1
            st.rerun()
        else:
            st.session_state["messages"].append({"role": "assistant", "content": "Okay, you can come back later."})
            st.stop()

# List of questions (limited to 5 for demo purposes)
questions = [
    "Have you noticed any changes in the size or shape of your breasts?",
    "Do you experience any pain or discomfort in your breasts?",
    "Have you noticed any lumps or bumps in your breasts that were not there before?",
    "Are you aware of any family history of breast cancer?",
    "Do you perform regular breast self-examinations?"
]

# Display chat history
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Ask questions interactively
if not st.session_state["questions_done"] and st.session_state["current_question_index"] > 0:
    if st.session_state["current_question_index"] <= len(questions):
        current_question = questions[st.session_state["current_question_index"] - 1]

        # Ensure the question is added to the history only once
        if len(st.session_state["messages"]) == 0 or st.session_state["messages"][-1]["content"] != current_question:
            st.chat_message("assistant").write(current_question)
            st.session_state["messages"].append({"role": "assistant", "content": current_question})
            st.session_state["conversation_log"] += f"Assistant: {current_question}\n"

        # User input
        if user_input := st.chat_input("Your response:"):
            st.session_state["messages"].append({"role": "user", "content": user_input})
            st.session_state["conversation_log"] += f"User: {user_input}\n"
            st.session_state["responses"][f"Q{st.session_state['current_question_index']}"] = {"question": current_question, "response": user_input}
            st.session_state["current_question_index"] += 1

            if st.session_state["current_question_index"] > len(questions):
                st.session_state["questions_done"] = True
                st.session_state["messages"].append({"role": "assistant", "content": "Thank you for answering. Feel free to ask any additional questions."})
                st.session_state["conversation_log"] += "Assistant: Thank you for answering. Feel free to ask any additional questions.\n"

            st.rerun()

# Save conversation log to a file
if st.session_state["questions_done"]:
    with open("conversation_log.txt", "w") as log_file:
        log_file.write(st.session_state["conversation_log"])

  # Replace None with your LLM instance
    medical_report = generate_medical_report(st.session_state["responses"])

    st.subheader("Generated Medical Report")
    st.text(medical_report)

    # Download as PDF
    st.download_button(
        label="Download Report as PDF",
        data=medical_report,
        file_name="medical_report.pdf",
        mime="application/pdf"
    )

    if user_input := st.chat_input("Ask an additional question:"):
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append(
            {"role": "assistant", "content": "Thank you for your question. I will get back to you soon."}
        )
        st.session_state["conversation_log"] += f"User: {user_input}\nAssistant: Thank you for your question. I will get back to you soon.\n"
        st.rerun()