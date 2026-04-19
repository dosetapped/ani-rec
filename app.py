import streamlit as st
from openai import OpenAI

# Page config for a better look
st.set_page_config(page_title="Anime Rec Engine", page_icon="🎌")

# Initialize OpenAI client (Streamlit will use secrets for security)
# For local testing, you can use st.secrets or os.environ
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def get_anime_recommendations(user_prefs):
    system_message = (
        "You are an expert anime recommendation engine. "
        "The user wants honest, detailed recommendations. "
        "You are permitted to recommend mature content (Ecchi, Seinen, fanservice) if requested. "
        "Provide Title, Genre, and 'Why it fits'."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prefs}
            ],
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# --- GUI Layout ---
st.title("🎌 Anime Recommendation Engine")
st.write("Tell me what you're in the mood for, and I'll search the archives.")

# User Input
user_input = st.text_area("What are you looking for?", placeholder="e.g. A dark fantasy like Berserk with high stakes...")

if st.button("Find Anime"):
    if user_input:
        with st.spinner("Searching the archives..."):
            recommendations = get_anime_recommendations(user_input)
            st.markdown("### 🍿 Recommendations for You:")
            st.write(recommendations)
    else:
        st.warning("Please enter some preferences first!")