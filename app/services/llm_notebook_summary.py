import nbformat
import requests

NOTEBOOK_WITH_SOP_PROMPT = """
You are Norah AI, a smart assistant reviewing a data analysis notebook.

First, here is the SOP context describing how the data was collected and structured:
"""
# {context_from_sop}
"""

Now, here is the analysis script:
"""
# {notebook_text}
"""

Please summarize the following:
1. What type of analysis is performed? (e.g., EDA, modeling)
2. Which variables or outcomes are being studied?
3. Are any models or statistical methods used?
4. What key insights or outputs were generated?
5. Does the analysis appear to align with how the data was collected per the SOP?

Return your answer in structured bullet points.
"""

def extract_notebook_text(file_path):
    nb = nbformat.read(file_path, as_version=4)
    content = []

    for cell in nb.cells:
        if cell.cell_type in ["markdown", "code"]:
            content.append(cell.source.strip())

    return "\n\n".join(content)

def summarize_notebook_with_llm(notebook_text, sop_context, endpoint_url, hf_token):
    prompt = NOTEBOOK_WITH_SOP_PROMPT.format(
        notebook_text=notebook_text[:3000],
        context_from_sop=sop_context[:1000]
    )
    response = requests.post(
        endpoint_url,
        headers={"Authorization": f"Bearer {hf_token}"},
        json={"inputs": prompt}
    )
    response.raise_for_status()
    return response.json()[0].get("generated_text", "")