import pdfplumber
from docx import Document
import requests

PROMPT_TEMPLATE = """
You are an assistant helping summarize research protocols or SOPs for mental health projects.

Extract and structure the following from the document:

1. Title
2. Objective
3. Study Design (arms, duration, measurements)
4. Primary and Secondary Outcomes
5. Sample Size
6. Version Number (if available)
7. Checklist Items mentioned (if it's an SOP)

Here is the document content:
"""
# {document_text}
"""

Return your output in clear bullet format.
"""

def extract_text_from_pdf(file_path):
    with pdfplplumber.open(file_path) as pdf:
        return "\n".join([p.extract_text() for p in pdf.pages if p.extract_text()])

def extract_text_from_docx(file_path):
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs if p.text.strip()])

def query_llm(document_text: str, endpoint_url: str, hf_token: str):
    prompt = PROMPT_TEMPLATE.format(document_text=document_text[:4000])
    response = requests.post(
        endpoint_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": prompt}
    )
    response.raise_for_status()
    return response.json()[0].get("generated_text", "")