# import packages
from dotenv import load_dotenv
import os
import openai
import streamlit as st


# load environment variables from .env file
load_dotenv()

# load OpenAI API key from environment variables
client = openai.OpenAI()

@st.cache_data
def get_response(user_prompt, temperature):
    response = client.responses.create(
        model="gpt-4o",  # Use the latest chat model
        input=[
            {"role": "system", "content": "You are a helpful assistant."},  # Set behavior
            {"role": "user", "content": user_prompt}  # Prompt
        ],
        temperature=temperature,  # A bit of creativity
        max_output_tokens=100  # Limit response length
    )
    return response



st.title("Hello, GenAI!")
st.write("This is your first Streamlit app.")

# Add a text input box for the user prompt
user_prompt = st.text_input("Enter your prompt:", "Explain generative AI in one sentence.")

# Add a slider for temperature
temperature = st.slider("Select creativity (temperature):", min_value=0.0, max_value=1.0, value=0.7, step=0.05)

with st.spinner("AI is working..."):
    if user_prompt:
        response = get_response(user_prompt, temperature)
        # print the response from OpenAI
        st.write(response.output[0].content[0].text)
