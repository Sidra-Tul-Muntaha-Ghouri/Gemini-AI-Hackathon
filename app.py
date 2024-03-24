import streamlit as st
import pathlib
import textwrap
from IPython.display import Markdown
import google.generativeai as genai
import fitz

GOOGLE_API_KEY = "GOOGLE_API_KEY"
genai.configure(api_key=GOOGLE_API_KEY)

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def etfp(pdf_file): # function to extract text from pdf
    text = ''
    with fitz.open(pdf_file) as pdf_document:
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            text += page.get_text()
    return text

def summarize(text, model):
    summary = model.generate_content(contents=f"Summarize this research article + {text}")
    result = summary.text
    return result

def explore(text, question, model):
    exp = model.generate_content(contents=f"write answer to {question} in context of this article {text}")
    result = exp.text
    return result

def delete_uploaded_file(file_path):
    if pathlib.Path(file_path).exists():
        pathlib.Path(file_path).unlink()
        return True
    else:
        return False

model = genai.GenerativeModel('gemini-pro')

title = "Research Paper Summarizer"
st.set_page_config(page_title=title, layout='centered')
st.title(title)
st.subheader("A gemini powered Research Papers Summarizer!",divider='rainbow')
file = st.file_uploader("Upload a Research Paper in .pdf extension", type="pdf",  accept_multiple_files=False)
summary_or_explore = st.radio("Choose an option:", ("Summarize", "Explore"))
with st.sidebar:
  
    st.title('Team Members')

    # Adding content to the sidebar
    st.write('Aref\nAyesha Mehboob\nMudassar Rehman\nMuhammad Qasim\nSidra Tul Muntaha\nSudha Sanjeevani\n ') 

if file is not None:
    text = etfp(file)
    
    if summary_or_explore == "Summarize":
        summary = summarize(text, model)
        st.markdown(summary)
    else:
        question = st.text_input("Write your questions here")
        if question:
            answer = explore(text, question, model)
            st.markdown(answer)
        else:
            st.write("Please enter your question.")

else:
    st.write("Please upload a PDF file.")
