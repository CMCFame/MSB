# ============================================================================
# GLOBAL CONFIGURATION OPTIONS TAB - FIXED
# ============================================================================
import streamlit as st
import pandas as pd
import io
from utils.ai_assistant import get_openai_response, save_chat_history

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
    total_questions = 53  # As specified in the original file
    answered_count = len([v for v in st.session_state.global_config_answers.values() if v not in (None, '', False, 0)])
    
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
    
    if tab_name == "Roster Admin":
        render_roster_admin_section()
    elif tab_name == "Calling Config":
        render_calling_config_section()
    elif tab_name == "VRU Config":
        render_vru_config_section()
    elif tab_name == "One-Call Rules":
        render_one_call_rules_section()
    elif tab_name == "Availability":
        render_availability_section()
    elif tab_name == "Employee Page":
        render_employee_page_section()
    elif tab_name == "Work & Rest Rules":
        render_work_rest_rules_section()
    elif tab_name == "Charge & Credit":
        render_charge_credit_section()
    elif tab_name == "Misc & New Year":
        render_misc_new_year_section()
    else:
        st.warning(f"Configuration for {tab_name} not yet implemented.")

def render_roster_admin_section():
    """Render Roster Admin section"""
    st.markdown("### Roster Sorting Methods")
    st.markdown("Select which roster sorting methods you want to use:")
    
    sorting_methods = ["Alpha", "Seniority", "Overtime", "Pointer - Last Attempted", 
                      "Pointer - Last Accepted", "Rotate", "Maintain Sort"]
    
    for method in sorting_methods:
        key = f"roster_sorting_{method.lower().replace(' ', '_').replace('-', '_')}"
        st.session_state.global_config_answers[key] = st.checkbox(
            method, 
            value=st.session_state.global_config_answers.get(key, False),
            key=key
        )
    
    st.markdown("### ARCOS Add-On Features")
    st.markdown("Mark the ARCOS add-on features included in your contract:")
    
    addon_features = [
        "ARCOS Mobile", "Web & Inbound Callout Activations", "Email Alerts",
        "Batched Reporting", "Closest to the Trouble (CTT)", "Text-To-Speech (TTS)",
        "Monthly Data Extract"
    ]
    
    for feature in addon_features:
        key = f"addon_{feature.lower().replace(' ', '_').replace('&', 'and').replace('(', '').replace(')', '').replace('-', '_')}"
        st.session_state.global_config_answers[key] = st.checkbox(
            feature,
            value=st.session_state.global_config_answers.get(key, False),
            key=key
        )
    
    # CTT Types (conditional)
    if st.session_state.global_config_answers.get("addon_closest_to_the_trouble_ctt", False):
        key = "ctt_applicable_types"
        st.session_state.global_config_answers[key] = st.text_input(
            "If CTT was selected, list applicable CO Types",
            value=st.session_state.global_config_answers.get(key, ""),
            key=key
        )

def render_calling_config_section():
    """Render Calling Config section"""
    st.markdown("### Calling Methods")
    key = "calling_methods_required"
    st.session_state.global_config_answers[key] = st.text_input(
        "Which calling methods are required? (Horizontal, Vertical)",
        value=st.session_state.global_config_answers.get(key, ""),
        key=key
    )
    
    st.markdown("### Exclusive Rule")
    key = "exclusive_rule_required"
    st.session_state.global_config_answers[key] = st.radio(
        "Is the Exclusive Rule required?",
        ["Yes", "No", "Not Sure"],
        index=["Yes", "No", "Not Sure"].index(st.session_state.global_config_answers.get(key, "Not Sure")),
        key=key
    )
    
    st.markdown("### Exclude from All Hands")
    key = "exclude_all_hands_required"
    st.session_state.global_config_answers[key] = st.radio(
        "Is the Exclude from All Hands field required?",
        ["Yes", "No", "Not Sure"],
        index=["Yes", "No", "Not Sure"].index(st.session_state.global_config_answers.get(key, "Not Sure")),
        key=key
    )

def render_vru_config_section():
    """Render VRU Config section"""
    st.markdown("### Device Limitations")
    key = "max_devices_per_employee"
    st.session_state.global_config_answers[key] = st.number_input(
        "How many devices can an employee have active at one time? (Up to three)",
        min_value=1, max_value=3,
        value=st.session_state.global_config_answers.get(key, 2),
        key=key
    )
    
    st.markdown("### Device Modification")
    key = "employee_device_modification"
    st.session_state.global_config_answers[key] = st.selectbox(
        "Which devices are employees allowed to modify through the Inbound system?",
        ["First", "Second", "Third", "All", "None"],
        index=["First", "Second", "Third", "All", "None"].index(st.session_state.global_config_answers.get(key, "All")),
        key=key
    )
    
    st.markdown("### Temporary Numbers")
    col1, col2 = st.columns(2)
    with col1:
        key = "temp_callout_numbers"
        st.session_state.global_config_answers[key] = st.number_input(
            "Temporary numbers allowed per employee (Callout)",
            min_value=0, max_value=5,
            value=st.session_state.global_config_answers.get(key, 1),
            key=key
        )
    
    with col2:
        key = "temp_mobile_numbers"
        st.session_state.global_config_answers[key] = st.number_input(
            "Temporary numbers allowed per employee (Mobile)",
            min_value=0, max_value=5,
            value=st.session_state.global_config_answers.get(key, 1),
            key=key
        )
    
    st.markdown("### PIN Requirement")
    key = "pin_required_outbound"
    st.session_state.global_config_answers[key] = st.radio(
        "Do you require a PIN to be entered by employees on Outbound calls?",
        ["Yes", "No"],
        index=["Yes", "No"].index(st.session_state.global_config_answers.get(key, "No")),
        key=key
    )

def render_one_call_rules_section():
    """Render One-Call Rules section"""
    st.markdown("### One Call per Co Main")
    key = "one_call_per_co_main"
    st.session_state.global_config_answers[key] = st.radio(
        "Do you require one call per Co Main?",
        ["Yes", "No"],
        index=["Yes", "No"].index(st.session_state.global_config_answers.get(key, "No")),
        key=key
    )
    st.caption("Employee will not be called on multiple sub-callouts but could be called multiple times WITHIN sub-callouts")
    
    st.markdown("### One Call per Co")
    key = "one_call_per_co"
    st.session_state.global_config_answers[key] = st.radio(
        "Do you require one call per Co?",
        ["Yes", "No"],
        index=["Yes", "No"].index(st.session_state.global_config_answers.get(key, "No")),
        key=key
    )
    st.caption("An employee will not be called more than once when on a series of chained rosters")

def render_availability_section():
    """Render Availability section"""
    st.markdown("### Availability Response Percentage")
    key = "availability_threshold"
    st.session_state.global_config_answers[key] = st.number_input(
        "What is the lowest percentage to keep text black?",
        min_value=0, max_value=100,
        value=st.session_state.global_config_answers.get(key, 85),
        key=key
    )
    
    st.markdown("### Zero Calls Percentage")
    key = "zero_calls_percentage"
    st.session_state.global_config_answers[key] = st.radio(
        "If an employee has received zero calls, should ARCOS display their percentage as:",
        ["0%", "100%"],
        index=["0%", "100%"].index(st.session_state.global_config_answers.get(key, "100%")),
        key=key
    )

def render_employee_page_section():
    """Render Employee Page section"""
    st.markdown("### Radio Field")
    key = "radio_field_required"
    st.session_state.global_config_answers[key] = st.text_input(
        "Do you require the Radio field? If yes, where do you want to see it?",
        value=st.session_state.global_config_answers.get(key, ""),
        placeholder="Roster view, Roster maintenance, Scheduler, Manual bypass",
        key=key
    )
    
    st.markdown("### Vehicle Field")
    key = "vehicle_field_config"
    st.session_state.global_config_answers[key] = st.selectbox(
        "Do you require the Vehicle field? If so, which configuration?",
        ["Not Required", "Type", "String", "Vehicle ID"],
        index=["Not Required", "Type", "String", "Vehicle ID"].index(st.session_state.global_config_answers.get(key, "Not Required")),
        key=key
    )

def render_work_rest_rules_section():
    """Render Work & Rest Rules section"""
    st.markdown("### Automatic Rest Status")
    key = "automatic_rest_status"
    st.session_state.global_config_answers[key] = st.radio(
        "Should ARCOS automatically place an employee on Rest status when released from working status if rest requirements are met?",
        ["Yes", "No"],
        index=["Yes", "No"].index(st.session_state.global_config_answers.get(key, "No")),
        key=key
    )
    
    if st.session_state.global_config_answers.get(key) == "Yes":
        rest_key = "rest_rule"
        st.session_state.global_config_answers[rest_key] = st.text_input(
            "If you answered Yes to automatic rest, which Rest Rule do you use?",
            value=st.session_state.global_config_answers.get(rest_key, ""),
            key=rest_key
        )

def render_charge_credit_section():
    """Render Charge & Credit section"""
    st.markdown("### Call Result Charges")
    
    key = "charges_employee_reached"
    st.session_state.global_config_answers[key] = st.text_input(
        "For employee reached but non-accept (Employee Not Home, Hangup, Invalid Entry), what is the charge?",
        value=st.session_state.global_config_answers.get(key, ""),
        key=key
    )
    
    key = "charges_employee_not_reached"
    st.session_state.global_config_answers[key] = st.text_input(
        "For employee not reached (Answering Machine, Busy, No Answer), what is the charge?",
        value=st.session_state.global_config_answers.get(key, ""),
        key=key
    )

def render_misc_new_year_section():
    """Render Misc & New Year section"""
    st.markdown("### Holdover Configuration")
    key = "holdover_functionality"
    st.session_state.global_config_answers[key] = st.radio(
        "Does your company use Holdover functionality?",
        ["Yes", "No"],
        index=["Yes", "No"].index(st.session_state.global_config_answers.get(key, "No")),
        key=key
    )
    
    if st.session_state.global_config_answers.get(key) == "Yes":
        name_key = "holdover_name"
        st.session_state.global_config_answers[name_key] = st.text_input(
            "What do you call it?",
            value=st.session_state.global_config_answers.get(name_key, ""),
            key=name_key
        )
    
    st.markdown("### New Year Start")
    key = "new_year_start"
    st.session_state.global_config_answers[key] = st.selectbox(
        "When does the new year begin in your organization?",
        ["January 1st", "Fiscal Year", "Other"],
        index=["January 1st", "Fiscal Year", "Other"].index(st.session_state.global_config_answers.get(key, "January 1st")),
        key=key
    )

def create_config_template():
    """Create a DataFrame template for global configuration"""
    template_data = [
        {"Section": "Roster Admin", "Question": "Alpha sorting method", "Question_ID": "roster_sorting_alpha"},
        {"Section": "Roster Admin", "Question": "Seniority sorting method", "Question_ID": "roster_sorting_seniority"},
        {"Section": "Calling Config", "Question": "Calling methods required", "Question_ID": "calling_methods_required"},
        {"Section": "VRU Config", "Question": "Max devices per employee", "Question_ID": "max_devices_per_employee"},
        # Add more template data as needed
    ]
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
        if 'Question_ID' in df.columns:
            question_id = row['Question_ID']
            answers[question_id] = row.get('Answer', '')
    
    return answers