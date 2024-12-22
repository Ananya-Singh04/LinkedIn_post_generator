import streamlit as st
from few_shot import FewShotPosts
from post_generator import generate_post

# Set page config
st.set_page_config(
    page_title="LinkedIn Post Generator",
    page_icon="🔗",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
    <style>
    .stApp {
        background-color: #1E1E2E;
        color: white;
    }
    .stButton>button {
        color: #84fab0;
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid #84fab0;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        color: white;
        background-color: #84fab0;
    }
    .stSelectbox {
        background-color: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }
    .output-container {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def main():
    st.title("LinkedIn Post Generator")

    fs = FewShotPosts()
    length_options = ["Short", "Medium", "Long"]
    language_options = ["English", "Hinglish"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### Title")
        selected_tag = st.selectbox("", options=fs.get_tags(), label_visibility="collapsed")

    with col2:
        st.markdown("### Length")
        selected_length = st.selectbox("", options=length_options, label_visibility="collapsed")

    with col3:
        st.markdown("### Language")
        selected_language = st.selectbox("", options=language_options, label_visibility="collapsed")

    if st.button("Generate Post"):
        with st.spinner('Generating your LinkedIn post...'):
            post = generate_post(selected_tag, selected_length, selected_language)

            st.markdown('<div class="output-container">', unsafe_allow_html=True)
            st.success("✅ Post Generated Successfully!")
            st.markdown("### Your Generated Post:")
            st.write(post)

            if st.button("📋 Copy to Clipboard"):
                st.toast("Post copied to clipboard!")

            st.markdown('</div>', unsafe_allow_html=True)

    # Footer
    st.markdown("""
    <div style='text-align: center; margin-top: 2rem; color: rgba(255,255,255,0.5);'>
        Made with ❤️ for LinkedIn Content Creators
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()