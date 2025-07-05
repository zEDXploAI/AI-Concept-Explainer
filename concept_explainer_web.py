import streamlit as st
from openai import OpenAI

# ✅ OpenRouter client setup
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# ❌ Blocked words list
banned_keywords = [
    "sex", "porn", "nsfw", "nude", "drugs", "violence", "kill",
    "bomb", "terror", "dating", "suicide", "politics", "dark web",
    "hack", "adult", "gun", "murder"
]

# ✅ Educational check
def is_educational(text):
    for word in banned_keywords:
        if word.lower() in text.lower():
            return False
    return True

# 🧠 GPT-3.5 concept explainer
def explain_concept(concept):
    prompt = (
        f"You are an educational AI assistant. Your job is to explain academic and scientific concepts "
        f"in simple, clear language for students. Do not answer non-educational, NSFW, political, or inappropriate questions. "
        f"If the question is inappropriate, politely refuse. Now explain: '{concept}'"
    )

    try:
        response = client.chat.completions.create(
            model="openrouter/cypher-alpha:free",  # ✅ Correct model name
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Error: {e}"

# 🌐 Streamlit app UI
st.set_page_config(page_title="Concept Explainer Bot", page_icon="📚")
st.title("🧠 zEDXplo Concept Explainer Bot")
st.caption("📘 Powered by OpenRouter | For Educational Use Only")

concept = st.text_input("Enter a concept you want explained:")

if concept:
    if not is_educational(concept):
        st.error("🚫 Sorry! This bot is for educational purposes only.")
        with open("misuse_log.txt", "a") as log:
            log.write(concept + "\n")
    else:
        with st.spinner("Explaining..."):
            answer = explain_concept(concept)
        st.success("✅ Explanation Ready!")
        st.write(answer)
