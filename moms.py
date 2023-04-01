import streamlit as st
import pandas as pd
import clipboard
import re

def generate_email(template, row, colors):
    email = template
    for index, column in enumerate(row.index):
        colored_value = f'<span style="color:{colors[index % len(colors)]}">{str(row[column])}</span>'
        email = re.sub(f'\\[{re.escape(column)}\\]', colored_value, email)
    return email

def copy_to_clipboard(text):
    clipboard.copy(text)
    st.write("Email copied to clipboard!")

def main():
    st.set_page_config(page_title="SANTOSO", layout="wide")

    st.title("PROGRAM RAHASIA IBU SANTOSO")

    # Custom CSS styles
    custom_css = """
    <style>
        body {
            font-family: 'Arial', sans-serif;
            color: #333;
            background-color: #f9f9f9;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #333;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border: none;
            font-size: 14px;
            padding: 8px 16px;
            cursor: pointer;
            text-align: center;
            border-radius: 4px;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
    </style>
    """

    st.markdown(custom_css, unsafe_allow_html=True)

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
            colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown', 'magenta', 'cyan']
            for _, row in df.iterrows():
                email = generate_email(user_text, row, colors)
                emails.append(email)

            for i, email in enumerate(emails, start=1):
                st.write(f"Email {i}:")
                st.write(email, unsafe_allow_html=True)
                copy_button = st.button(f"Copy Email {i}")
                if copy_button:
                    copy_to_clipboard(email)
                st.write("------")

if __name__ == "__main__":
    main()
