#!/usr/bin/env python3
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
import streamlit as st

from literaturereviewbot.prompts.literature_review import (
    generate_prompt as lit_review_prompt,
)

st.title("Literature Review Bot")

# Styling
st.markdown(
    """
<style>
.main {
    background-color: #00000;
}
</style>
""",
    unsafe_allow_html=True,
)

# Sidebar for additional options or information
with st.sidebar:
    st.info("This app uses the Llama 3.1 model to answer your questions.")

### Possible prompt for literature review bot once we have the data
# documents = docs_to_be_summarized
# # Construct the conversation


###
kw_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are an experienced professional biomedical researcher.
            You will will be given a question or a statement to respond to.
            Identify the keywords in the question or statement and return the keywords separated by commas.
            """,
        ),
        (
            "human",
            "Use the given format to extract information from the following "
            "input: {question}",
        ),
    ]
)

entity_chain = kw_prompt | .with_structured_output(Entities)
entity_chain.invoke({"question": "Who are Nonna Lucia and Giovanni Caruso?"}).names

template = """{prompt}
Answer:
"""
model = OllamaLLM(model="llama3.1")
kw_chain = kw_prompt | model

research_prompt = ChatPromptTemplate.from_template(template)
research_chain = research_prompt | model

# Main content
col1, col2 = st.columns(2)
with col1:
    question = st.text_input("Enter your question here")
    if question:
        with st.spinner("Thinking..."):
            prompt = lit_review_prompt(question)
            answer = chain.invoke(prompt)
            st.success("Done!")
        st.markdown(f"**Answer:** {answer}")
    else:
        st.warning("Please enter a question to get an answer.")
