# Comprehensive mapping of Global Configuration Questions
import streamlit as st

def parse_list_input(input_str):
    """Helper to parse comma-separated or multi-line inputs"""
    return [item.strip() for item in input_str.split(',') if item.strip()]

GLOBAL_CONFIG_QUESTIONS = {
    "Roster Administration": [
        # Roster Sorting Methods
        {"id": "1a_alpha", "category": "Roster Sorting Methods", 
         "question": "Use Alpha sorting?", "type": "checkbox"},
        {"id": "1a_seniority", "category": "Roster Sorting Methods", 
         "question": "Use Seniority sorting?", "type": "checkbox"},
        {"id": "1a_overtime", "category": "Roster Sorting Methods", 
         "question": "Use Overtime sorting?", "type": "checkbox"},
        {"id": "1a_pointer_last_attempted", "category": "Roster Sorting Methods", 
         "question": "Use Pointer - Last Attempted sorting?", "type": "checkbox"},
        {"id": "1a_pointer_last_accepted", "category": "Roster Sorting Methods", 
         "question": "Use Pointer - Last Accepted sorting?", "type": "checkbox"},
        {"id": "1a_rotate", "category": "Roster Sorting Methods", 
         "question": "Use Rotate sorting?", "type": "checkbox"},
        {"id": "1a_maintain_sort", "category": "Roster Sorting Methods", 
         "question": "Maintain Sort?", "type": "checkbox"},
        
        # ARCOS Add-On Features
        {"id": "1b_mobile", "category": "ARCOS Add-On Features", 
         "question": "ARCOS Mobile", "type": "checkbox"},
        {"id": "1b_web_inbound", "category": "ARCOS Add-On Features", 
         "question": "Web & Inbound Callout Activations", "type": "checkbox"},
        {"id": "1b_email_alerts", "category": "ARCOS Add-On Features", 
         "question": "Email Alerts", "type": "checkbox"},
        {"id": "1b_batched_reporting", "category": "ARCOS Add-On Features", 
         "question": "Batched Reporting", "type": "checkbox"},
        {"id": "1b_ctt", "category": "ARCOS Add-On Features", 
         "question": "Closest to the Trouble (CTT)", "type": "checkbox"},
        {"id": "1b_ctt_types", "category": "ARCOS Add-On Features", 
         "question": "CTT Applicable Callout Types", "type": "text", 
         "depends_on": "1b_ctt"},
        {"id": "1b_tts", "category": "ARCOS Add-On Features", 
         "question": "Text-To-Speech (TTS)", "type": "checkbox"},
        {"id": "1b_monthly_extract", "category": "ARCOS Add-On Features", 
         "question": "Monthly Data Extract", "type": "checkbox"}
    ],
    "Calling Configuration": [
        {"id": "2_calling_methods", "category": "Calling Methods", 
         "question": "Which calling methods are required?", "type": "text"},
        {"id": "3_exclusive_rule", "category": "Exclusive Rule", 
         "question": "Is the Exclusive Rule required?", "type": "text"},
        {"id": "4_exclude_all_hands", "category": "Exclude from All Hands", 
         "question": "Is the Exclude from All Hands field required?", "type": "text"}
    ],
    "VRU Configuration": [
        {"id": "5_device_limit", "category": "Device Limitations", 
         "question": "How many devices can an employee have active at one time?", "type": "number"},
        {"id": "6_device_modification", "category": "Device Modification", 
         "question": "Which devices can employees modify through Inbound?", "type": "text"},
        {"id": "7_temp_callout_numbers", "category": "Temporary Numbers", 
         "question": "How many temporary callout numbers per employee?", "type": "number"},
        {"id": "7_temp_mobile_numbers", "category": "Temporary Numbers", 
         "question": "How many temporary mobile numbers per employee?", "type": "number"},
        {"id": "7a_temp_callout_duration", "category": "Temporary Number Duration", 
         "question": "Temporary callout number max hours", "type": "number", 
         "default": 72},
        {"id": "7a_temp_mobile_duration", "category": "Temporary Number Duration", 
         "question": "Temporary mobile number max hours", "type": "number", 
         "default": 72}
    ]
    # Note: Would continue with all 53 questions, but abbreviated for brevity
}

def render_global_config_question(question):
    """Render a specific question based on its type"""
    session_key = f"global_config_{question['id']}"
    
    # Check for dependencies
    if question.get('depends_on'):
        parent_key = f"global_config_{question['depends_on']}"
        if not st.session_state.global_config_answers.get(parent_key, False):
            return None
    
    # Render based on question type
    if question['type'] == 'checkbox':
        return st.checkbox(
            question['question'], 
            value=st.session_state.global_config_answers.get(session_key, False),
            key=session_key
        )
    elif question['type'] == 'text':
        return st.text_input(
            question['question'], 
            value=st.session_state.global_config_answers.get(session_key, ''),
            key=session_key
        )
    elif question['type'] == 'number':
        return st.number_input(
            question['question'], 
            value=st.session_state.global_config_answers.get(session_key, 
                question.get('default', 0)),
            key=session_key
        )
    
    return None

def render_category_questions(category):
    """Render all questions for a specific category"""
    category_questions = [
        q for section in GLOBAL_CONFIG_QUESTIONS.values() 
        for q in section if q['category'] == category
    ]
    
    for question in category_questions:
        render_global_config_question(question)

def get_total_questions():
    """Get total number of questions"""
    return sum(len(section) for section in GLOBAL_CONFIG_QUESTIONS.values())

def get_answered_questions():
    """Count answered questions"""
    return len([
        q for q in st.session_state.global_config_answers.values() 
        if q not in (None, '', False, 0)
    ])