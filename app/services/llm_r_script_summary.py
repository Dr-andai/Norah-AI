import requests

R_SCRIPT_PROMPT = """
You are Norah AI, a smart assistant reviewing an R script uploaded by a healthcare data scientist.

Please summarize the script by answering:

1. What type of analysis is performed? (e.g., EDA, visualization, modeling)
2. Which variables or outcomes are being analyzed?
3. Are any machine learning or statistical models used?
4. Are any results or insights evident from the script?
5. How well does it align with the expected protocol or SOP?

Here is the R script content:
"""
# {r_script_text}
"""

Please return your answer in clear bullet format.
"""

def read_r_script(file_path):
    with open(file_path, "r") as f:
        return f.read()

def summarize_r_script_with_llm(r_script_text, endpoint_url, hf_token):
    prompt = R_SCRIPT_PROMPT.format(r_script_text=r_script_text[:4000])
    response = requests.post(
        endpoint_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": prompt}
    )
    response.raise_for_status()
    return response.json()[0].get("generated_text", "")