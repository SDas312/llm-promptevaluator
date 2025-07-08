import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Set Streamlit page config
st.set_page_config(page_title="LLM Prompt Evaluator", layout="centered")

st.title("🧠 LLM Prompt Evaluator")
st.markdown("Evaluate LLM prompts interactively using OpenAI's API.")

# Initialize chat history in session state
if "history" not in st.session_state:
    st.session_state.history = []

# Choose task
task = st.selectbox("🛠️ Choose Task", ["Translate to French", "Summarize", "Fix Grammar"])

# Define prompt templates
prompt_templates = {
    "Translate to French": "Translate this to French: {text}",
    "Summarize": "Summarize this: {text}",
    "Fix Grammar": "Correct the grammar: {text}"
}

# Show prompt template
prompt_template = prompt_templates[task]
st.text_area("📄 Prompt Template", value=prompt_template, height=100)

# Input text
user_input = st.text_input("🔥 Input Text")

# Choose model
model = st.selectbox("🧠 Choose Model", ["gpt-3.5-turbo", "gpt-4"])

# On Evaluate
if st.button("🚀 Evaluate"):
    if user_input.strip() == "":
        st.warning("Please enter some input text.")
    else:
        # Construct full prompt
        formatted_prompt = prompt_template.replace("{text}", user_input)

        try:
            # Call OpenAI API using new SDK
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": formatted_prompt}
                ]
            )

            result = response.choices[0].message.content.strip()

            # Save to history
            st.session_state.history.append({
                "task": task,
                "input": user_input,
                "output": result
            })

            st.success("✅ Output:")
            st.write(result)

        except Exception as e:
            st.error(f"❌ API call failed: {e}")

# Show history
if st.session_state.history:
    st.markdown("### 🕘 Chat History")
    for idx, item in enumerate(reversed(st.session_state.history), 1):
        st.markdown(f"**{idx}. {item['task']}**")
        st.markdown(f"- **Input**: {item['input']}")
        st.markdown(f"- **Output**: {item['output']}")
        st.markdown("---")

