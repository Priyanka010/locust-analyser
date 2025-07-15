import pdfplumber
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import PlainTextResponse
from vertexai.generative_models import GenerativeModel
import vertexai
import pandas as pd
import os
import io
import uvicorn

app = FastAPI()

# Log the environment
print("GCP_PROJECT:", os.getenv("GCP_PROJECT"))
print("GCP_REGION:", os.getenv("GCP_REGION"))

# Initialise Vertex AI (Cloud Run is using IAM service account)
vertexai.init(project=os.getenv("GCP_PROJECT"), location=os.getenv("GCP_REGION"))
#Choose your preferred model
model = GenerativeModel("gemini-1.5-pro")

PROMPT_TEMPLATE = """
You are a performance engineer analyzing Locust load testing results for a software application. This analysis is intended for project managers who need a plain-English summary of system performance.

The report should:
- Clearly identify high-latency endpoints.
- Highlight any endpoints with high failure rates.
- Detect points of performance degradation.
- Present latency in a readable markdown table.
- Provide a high-level business recommendation.

You must write your entire response in plain English **paragraphs only**, suitable for non-technical stakeholders. Do not return JSON or structured data. Do not use numbered or bulleted lists. Seamlessly include insights, findings, and conclusions inside natural language. If helpful, embed a markdown table inline.

Here is the extracted Locust table data:
{table_data}

Additional context:
{extra}

Begin your plain-English summary now:
"""

@app.post("/analyze")
async def analyze_locust_report(file: UploadFile = File(...)):
    try:
        print("Received file:", file.filename)
        pdf_data = await file.read()

        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            first_page = pdf.pages[0]
            table = first_page.extract_table()

            if table is None or len(table) == 0:
                raise HTTPException(status_code=400, detail="No table found in the PDF.")

        df = pd.DataFrame(table[1:], columns=table[0])

        if df.empty:
            raise HTTPException(status_code=400, detail="Extracted table is empty.")

        table_data = df.head(20).to_markdown(index=False)
        prompt = PROMPT_TEMPLATE.format(table_data=table_data, extra="")

        response = model.generate_content(prompt)

        return PlainTextResponse(content=response.text)

    except Exception as e:
        print("Error:", str(e))
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
