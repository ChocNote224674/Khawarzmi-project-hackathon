# agents.py
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from config import openai_api_key

class QuestionAskingAgent:
    def __init__(self, questions, llm):
        self.questions = questions
        self.llm = llm
        self.responses = {}

    def ask_questions(self):
        # Parcourir chaque question et collecter la réponse
        for i, question in enumerate(self.questions):
            prompt_template = PromptTemplate(
                input_variables=["question"],
                template="You are a medical assistant. Ask the patient the following question and wait for their response:\n\nQUESTION: {question}\n\nPlease enter your response below."
            )
            chain = LLMChain(prompt=prompt_template, llm=self.llm)
            response = chain.run({"question": question})
            self.responses[f"Q{i+1}"] = {"question": question, "response": response}
        return self.responses

class MedicalReportAgent:
    def __init__(self, llm):
        self.llm = llm

    def generate_report(self, responses):
        prompt_template = PromptTemplate(
            input_variables=["responses"],
            template="""You are a medical assistant AI. Based on the following responses to medical questions, generate a detailed and structured medical report. The report should be formatted in the following sections:

            1. **Observation**: Summarize any significant changes in the patient's condition, including breast size, shape, or any related symptoms.
            2. **Pain**: Mention any pain or discomfort reported by the patient.
            3. **Skin Changes**: Note any changes in the appearance or texture of the breast skin.
            4. **Lumps**: Summarize any lumps or masses felt by the patient during self-examination.
            5. **Nipple Discharge**: Mention if there is any nipple discharge or changes in nipple appearance.
            6. **Appearance**: Summarize any changes in the overall appearance of the breasts, such as dimpling or puckering.
            7. **Family History**: If relevant, include the patient's family history of breast cancer.
            8. **Self-Examination**: Note whether the patient has been performing regular breast self-examinations.
            9. **Tenderness**: Summarize any tenderness or sensitivity reported by the patient.
            10. **Lymph Nodes**: Mention any changes in the size or appearance of the lymph nodes in the underarm area.

            **Patient Responses**:
            {responses}

            **Generated Medical Report**:
            """
        )
        chain = LLMChain(prompt=prompt_template, llm=self.llm)
        responses_text = "\n".join([f"{key}: {value['question']} - {value['response']}" for key, value in responses.items()])
        report = chain.run({"responses": responses_text})
        return report
