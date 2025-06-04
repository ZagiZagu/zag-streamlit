import streamlit as st
import pandas as pd
from together import Together
from fpdf import FPDF
from datetime import datetime

# Step 1: Setup Together API client
api_key = "fe72b5ea5936d3f2f7e6d5e758771200486a84e8bf43ad74f3c01e6225f3a988"
client = Together(api_key=api_key)

# Step 2: Streamlit UI
st.set_page_config(page_title="Excel + LLaMA AI Analysis", page_icon="📊")
st.title("✅ This is a Continuous improvement software")
st.caption("📁 Upload Excel + 🦙 LLaMA AI Analysis + 📄 PDF Export")

uploaded_file = st.file_uploader("Upload your Excel file:", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.write("✅ Uploaded Data Preview:")
    st.dataframe(df)

    question = st.text_area("🔍 Enter your question about the data:")

    if st.button("🧠 Analyze with LLaMA"):
        if question:
            with st.spinner("Sending request to LLaMA..."):
                prompt = f"""
You are a production data analyst. Here's a sample of the dataset:
{df.head(10).to_string()}

Now answer this question:
{question}
"""
                response = client.chat.completions.create(
                    model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                answer = response.choices[0].message.content
                st.success("✅ LLaMA's Answer:")
                st.write(answer)

                # PDF Export
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.cell(200, 10, txt="LLaMA Analysis Report", ln=True, align='C')
                pdf.ln(10)
                pdf.multi_cell(0, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
                pdf.ln(5)
                pdf.multi_cell(0, 10, txt=f"Question:\n{question}")
                pdf.ln(5)
                pdf.multi_cell(0, 10, txt=f"Answer:\n{answer}")

                pdf_path = "llama_analysis_report.pdf"
                pdf.output(pdf_path)

                with open(pdf_path, "rb") as pdf_file:
                    st.download_button(
                        label="📄 Download PDF Report",
                        data=pdf_file,
                        file_name="LLaMA_Report.pdf",
                        mime="application/pdf"
                    )
        else:
            st.warning("Please enter a question to proceed.")
else:
    st.info("Please upload an Excel file to begin.")
