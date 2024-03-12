import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

load_dotenv() ## load all our environment variables

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input):
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content(input)
    return response.text

def input_pdf_text(uploaded_file):
    reader=pdf.PdfReader(uploaded_file)
    text=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text+=str(page.extract_text())
    return text

#Prompt Template



input_prompt = """
Hey, act like a skilled or very experienced ATS (Application Tracking System)
with a deep understanding of the tech field, software engineering, data science,
data analysis, and big data engineering. Your task is to provide an ATS score for the given resume
and suggest potential interview questions. Consider the job market is highly competitive, 
and you should offer the best assistance for improving the resume.

Resume: {text}


# You can use this prompt to get both the ATS score and interview questions.

description:{jd}

I want the response in one single string having the structure
{"{{\"ATS Score\":\"%\",\"Interview Questions\":[],\"Profile Summary\":\"\"}}"
"""

## streamlit app
st.title("Smart ATS")
st.text("Improve Your Resume ATS")
jd=st.text_area("Paste the Job Description")
uploaded_file=st.file_uploader("Upload Your Resume",type="pdf",help="Please uplaod the pdf")
submit1 = st.button("Tell Me About the Resume")
submit2 = st.button("Give ats score of my resume")
submit3 = st.button("how can i improve my resume ")
submit = st.button("what interview question can be asked on basis of resume")

if submit:
    if uploaded_file is not None:
        text=input_pdf_text(uploaded_file)
        response=get_gemini_repsonse(input_prompt)
        st.subheader(response)