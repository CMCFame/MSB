# ============================================================================
# GLOBAL CONFIGURATION OPTIONS TAB
# ============================================================================
import streamlit as st
import pandas as pd
import io
from utils.ai_assistant import get_openai_response, save_chat_history
from utils.global_config_questions import (
    GLOBAL_CONFIG_QUESTIONS, 
    render_category_questions,
    get_total_questions,
    get_answered_questions
)

def render_global_config():
    """Render the Global Configuration Options form"""
    st.markdown('<p class="tab-header">Global Configuration Options</p>', unsafe_allow_html=True)
    
    # Initialize session state for global config if not exists
    if 'global_config_answers' not in st.session_state:
        st.session_state.global_config_answers = {}
    
    # Tab configuration
    tab_labels = [
        "Roster Admin", "Calling Config", "VRU Config",
        "One-Call Rules", "Availability", "Employee Page",
        "Work & Rest Rules", "Charge & Credit", "Misc & New Year"
    ]
    tabs = st.tabs(tab_labels)
    
    # Compute total and answered questions
    total_questions = get_total_questions()
    answered_count = get_answered_questions()
    
    # Progress indicator
    st.markdown(f'<div class="info-box">Answered: {answered_count} / {total_questions} Questions</div>', unsafe_allow_html=True)
    
    # Render each tab
    for i, tab in enumerate(tabs):
        with tab:
            # AI Help toggle
            if st.button("🤖 Need Help?", key=f"help_{tab_labels[i]}"):
                help_query = f"Provide detailed guidance on completing the {tab_labels[i]} section of the Global Configuration Options in ARCOS."
                with st.spinner("Getting expert assistance..."):
                    help_response = get_openai_response(help_query)
                    save_chat_history(f"Help with {tab_labels[i]}", help_response)
                st.info(help_response)
            
            # Render specific tab content
            render_tab_content(tab_labels[i])
    
    # Export/Import functionality
    st.markdown("<hr>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Configuration Template"):
            template_df = create_config_template()
            excel_buffer = io.BytesIO()
            template_df.to_excel(excel_buffer, index=False)
            st.download_button(
                label="Download Excel Template",
                data=excel_buffer.getvalue(),
                file_name="arcos_global_config_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    with col2:
        uploaded_file = st.file_uploader("📤 Upload Filled Template", type=["xlsx", "csv"])
        if uploaded_file:
            try:
                imported_answers = parse_config_template(uploaded_file)
                st.session_state.global_config_answers.update(imported_answers)
                st.success("Configuration imported successfully!")
            except Exception as e:
                st.error(f"Error importing configuration: {str(e)}")

def render_tab_content(tab_name):
    """Render content for specific global config tabs"""
    category_map = {
        "Roster Admin": ["Roster Sorting Methods", "ARCOS Add-On Features"],
        "Calling Config": ["Calling Methods", "Exclusive Rule", "Exclude from All Hands"],
        "VRU Config": ["Device Limitations", "Device Modification", "Temporary Numbers", "Temporary Number Duration"],
        # Add more mappings for other tabs
    }
    
    # Render categories for the specific tab
    if tab_name in category_map:
        for category in category_map[tab_name]:
            st.markdown(f"### {category}")
            render_category_questions(category)
    else:
        st.warning(f"Configuration for {tab_name} not yet implemented.")

def create_config_template():
    """Create a DataFrame template for global configuration"""
    template_data = []
    for section in GLOBAL_CONFIG_QUESTIONS.values():
        for question in section:
            template_data.append({
                "Section": question.get('category', 'Uncategorized'),
                "Question": question['question'],
                "Question ID": question['id']
            })
    return pd.DataFrame(template_data)

def parse_config_template(uploaded_file):
    """Parse uploaded configuration template"""
    if uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_csv(uploaded_file)
    
    # Basic parsing logic
    answers = {}
    for _, row in df.iterrows():
        # Look for the question ID column, assuming it exists
        if 'Question ID' in df.columns:
            question_id = row['Question ID']
            # Add basic parsing logic here
            answers[f"global_config_{question_id}"] = row.get('Answer', '')
    
    return answers