# ============================================================================
# HEADER COMPONENT
# ============================================================================
import streamlit as st
from config.constants import ARCOS_LOGO_URL
from utils.ui_helpers import render_css

def render_header():
    """Render the application header with logo and title"""
    # Apply custom CSS
    render_css()

    # Display ARCOS logo and title
    col1, col2 = st.columns([1, 5])
    with col1:
        try:
            st.image(ARCOS_LOGO_URL, width=150)
        except Exception as e:
            st.write("ARCOS")
            print(f"Error loading logo: {str(e)}")

    with col2:
        st.markdown(
            '<p class="main-header">System Implementation Guide Form</p>',
            unsafe_allow_html=True
        )
        st.write("Complete your ARCOS configuration with AI assistance")
