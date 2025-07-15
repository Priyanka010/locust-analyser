import streamlit as st
import requests
import os

st.set_page_config(page_title="Locust Load Test Analyser", layout="wide")
st.title("📊 Locust Load Test Analyser")

st.markdown("Upload aa your **Locust PDF report** to get a natural language summary of performance, latency, and reliability issues.")

# Url from env or use localhost
backend_url = os.getenv("API_URL", "http://localhost:8080/analyze")

# Upload the PDF file
uploaded_file = st.file_uploader("Upload Locust PDF file", type=["pdf"])

if uploaded_file and backend_url:
    files = {"file": uploaded_file}

    with st.spinner("Analysing PDF..."):
        try:
            response = requests.post(backend_url, files=files)

            if response.status_code == 200:
                st.success("Analysis complete!")
                st.subheader("📝 Performance Analysis")
                st.markdown(response.text)

                # Allow user to download the result..this is in txt format
                st.download_button("Download Analysis", response.text, file_name="locust_analysis.txt")

            else:
                st.error(f"Backend returned status code {response.status_code}")
                st.text(response.text)

        except Exception as e:
            st.error("An error occurred while sending the request.")
            st.text(str(e))

