# ============================================================================
# AI ASSISTANT FUNCTIONALITY
# ============================================================================
import streamlit as st
import openai
import os
from config.constants import OPENAI_MODEL, OPENAI_MAX_TOKENS, OPENAI_TEMPERATURE

# ============================================================================
# OPENAI CLIENT INITIALIZATION
# ============================================================================
def initialize_openai_client():
    """Initialize the OpenAI client with API key from secrets"""
    try:
        client = openai.OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
        return client
    except Exception as e:
        print(f"Warning: OpenAI client initialization failed - {str(e)}")
        # Create a dummy client for demo purposes when API key is not available
        class DummyClient:
            def __init__(self):
                self.chat = self
                self.completions = self
            
            def create(self, **kwargs):
                from collections import namedtuple
                Choice = namedtuple('Choice', ['message'])
                Message = namedtuple('Message', ['content'])
                Response = namedtuple('Response', ['choices'])
                
                msg = Message(content="This is a placeholder response since the OpenAI API key is not configured. In a real deployment, this would be a helpful response from the AI model.")
                choices = [Choice(message=msg)]
                return Response(choices=choices)
        
        return DummyClient()

# Initialize the OpenAI client
client = initialize_openai_client()

def get_openai_response(prompt, context=""):
    """Get response from OpenAI API"""
    try:
        messages = [
            {"role": "system", "content": "You are a helpful expert on ARCOS system implementation. " + context},
            {"role": "user", "content": prompt}
        ]
        
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=messages,
            max_tokens=OPENAI_MAX_TOKENS,
            temperature=OPENAI_TEMPERATURE
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def save_chat_history(user_question, response):
    """Save user question and AI response to chat history"""
    st.session_state.chat_history.append({"role": "user", "content": user_question})
    st.session_state.chat_history.append({"role": "assistant", "content": response})

def get_recent_messages(limit=10):
    """Get the most recent messages from chat history"""
    if len(st.session_state.chat_history) > 0:
        return st.session_state.chat_history[-limit:]
    return []

def clear_chat_history():
    """Clear the chat history"""
    st.session_state.chat_history = []