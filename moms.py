import streamlit as st
import pandas as pd
import re
from docx import Document
import base64
import os

def generate_email(template, row):
    email = template
    for column in row.index:
        email = re.sub(f'\\[{re.escape(column)}\\]', str(row[column]), email)
    return email

def save_as_docx(text, filename):
    doc = Document()
    doc.add_paragraph(text)
    doc.save(filename)

def create_download_link(filename):
    with open(filename, 'rb') as file:
        file_data = file.read()
    b64 = base64.b64encode(file_data).decode()
    return f'<a href="data:application/octet-stream;base64,{b64}" download="{filename}">Download {filename}</a>'

def main():
    st.set_page_config(page_title="SANTOSO", layout="wide")

    st.title("PROGRAM RAHASIA IBU SANTOSO")

    # Create columns for layout
    left_column, right_column = st.columns([1, 1])

    with left_column:
        st.header("KOPAS DISINI")
        user_text = st.text_area("Enter your text here:", height=600)

        st.header("UPLOD DISINI BOS")
        uploaded_file = st.file_uploader("Choose a file", type=["csv"])

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)

            st.write("Attributes:")
            for x in df.columns:
                st.write(f'\t{x}\t')

    with right_column:
        st.header("MONGGO BOS")
        output_text = st.empty()

        if uploaded_file is not None and user_text:
            emails = []
            for _, row in df.iterrows():
                email = generate_email(user_text, row)
                emails.append(email)

            for i, email in enumerate(emails, start=1):
                st.write(f"Email {i}:")
                st.write(email)

                filename = f"email_{i}.docx"
                save_as_docx(email, filename)
                st.markdown(create_download_link(filename), unsafe_allow_html=True)

                os.remove(filename)  # remove the saved file after creating download link

                st.write("------")

if __name__ == "__main__":
    main()
