import streamlit as st
from openai import OpenAI
import time

# Load from secrets
assistant_id = st.secrets["ASSISTANT_ID"]
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Set up page
st.set_page_config(page_title="OpenAI Assistant App", page_icon="🤖")
st.title("🤖 Talk to Your OpenAI Assistant")

# User prompt input
user_prompt = st.text_area("Enter your question or request:", height=150)

# On submit
if st.button("Generate Response"):
    if not user_prompt.strip():
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Assistant is thinking..."):

            # Step 1: Create a new thread (or store one in session_state for reuse)
            thread = client.beta.threads.create()

            # Step 2: Add the user message to the thread
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_prompt
            )

            # Step 3: Run the assistant on the thread
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=assistant_id
            )

            # Step 4: Poll for completion
            while True:
                run_status = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                if run_status.status == "completed":
                    break
                elif run_status.status in ["failed", "cancelled", "expired"]:
                    st.error(f"Run failed with status: {run_status.status}")
                    break
                time.sleep(1)

            # Step 5: Retrieve messages (assistant reply)
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            reply = None
            for msg in messages.data:
                if msg.role == "assistant":
                    reply = msg.content[0].text.value
                    break

            if reply:
                st.markdown("### ✨ Assistant's Response:")
                st.write(reply)
            else:
                st.warning("No response received.")

            output = response.choices[0].message.content
            st.success("Done!")
            st.markdown("### ✨ Response:")
            st.write(output)
