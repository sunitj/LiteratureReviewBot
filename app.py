#!/usr/bin/env python3
import asyncio
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

template = """{prompt}
Answer:
"""
prompt_template = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="llama3.1")
chain = prompt_template | model

# Main content
col1, col2 = st.columns(2)
with col1:
    question = st.text_input("Enter your question here")
    if question:
        with st.spinner("Thinking..."):
            # Streamlit runs the script from top to bottom on each interaction.
            # For a simple, one-off async call like this, asyncio.run() is a
            # pragmatic choice. For more complex apps, a different approach
            # might be needed.
            prompt = asyncio.run(lit_review_prompt(question))
            answer = chain.invoke({"prompt": prompt})
            st.success("Done!")
        st.markdown(f"**Answer:** {answer}")
    else:
        st.warning("Please enter a question to get an answer.")
