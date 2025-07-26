import streamlit as st
from openai import OpenAI

# Set up Streamlit page
st.set_page_config(page_title="OpenAI Prompt Tester", page_icon="🧠")

st.title("🧠 Ask OpenAI Something")
st.markdown("Type your prompt below and get a response from GPT!")

# Load OpenAI client with API key
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# User input prompt
user_prompt = st.text_area("Enter your prompt:", height=150)

# On submit
if st.button("Generate Response"):
    if user_prompt.strip() == "":
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Thinking..."):
            response = client.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" if you want faster/cheaper
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_prompt}
                ]
            )
            output = response.choices[0].message.content
            st.success("Done!")
            st.markdown("### ✨ Response:")
            st.write(output)
