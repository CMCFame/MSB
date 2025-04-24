# ============================================================================
# SIDEBAR COMPONENT
# ============================================================================
import streamlit as st
from utils.ai_assistant import get_openai_response, save_chat_history
from config.constants import ARCOS_RED

def render_sidebar(unique_id):
    """Render the sidebar with the AI assistant"""
    # Logo and title for sidebar
    try:
        st.image("https://www.arcos-inc.com/wp-content/uploads/2020/10/logo-arcos-news.png", width=120)
    except Exception as e:
        st.write("ARCOS")
        print(f"Error loading logo: {str(e)}")

    st.markdown('<p style="font-size: 1.2em; font-weight: bold; color: #e3051b;">AI Assistant</p>', unsafe_allow_html=True)

    # Create a styled assistant box
    st.markdown("""
    <div style="border-left: 3px solid #e3051b; padding: 10px; background-color: #f8f9fa; border-radius: 5px; margin-bottom: 15px;">
        <p style="font-weight: bold;">Hello!</p>
        <p>This assistant is designed to help ARCOS solution consultants better understand the system configuration. 
        If you're unsure about any question, simply ask here and I'll provide a brief explanation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Chat input
    user_question = st.text_input("Ask anything about ARCOS configuration:", key=f"user_question_{unique_id}")

    if st.button("Ask AI Assistant", key=f"ask_ai_{unique_id}", type="primary"):
        if user_question:
            # Get current tab for context
            current_tab = st.session_state.current_tab
            context = f"The user is working on the ARCOS System Implementation Guide form. Currently on the '{current_tab}' tab."

            # Show spinner while getting response
            with st.spinner("Getting response..."):
                # Get response from OpenAI
                response = get_openai_response(user_question, context)

                # Store in chat history
                save_chat_history(user_question, response)

    # Display chat history
    st.markdown('<p style="font-weight: bold; margin-top: 20px;">Chat History</p>', unsafe_allow_html=True)

    chat_container = st.container()
    with chat_container:
        # Show up to 10 most recent messages
        recent_messages = st.session_state.chat_history[-10:] if len(st.session_state.chat_history) > 0 else []
        for message in recent_messages:
            if message["role"] == "user":
                st.markdown(
                    f"<div style='background-color: #f0f0f0; padding: 8px; border-radius: 5px; margin-bottom: 8px;'>"
                    f"<b>You:</b> {message['content']}</div>", 
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"<div style='background-color: #e6f7ff; padding: 8px; border-radius: 5px; margin-bottom: 8px;"
                    f"border-left: 3px solid #1E88E5;'><b>Assistant:</b> {message['content']}</div>", 
                    unsafe_allow_html=True
                )

    # Clear chat history button
    if st.button("Clear Chat History", key=f"clear_chat_{unique_id}", type="secondary"):
        st.session_state.chat_history = []
        st.rerun()