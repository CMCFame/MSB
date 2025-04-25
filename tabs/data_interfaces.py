# ============================================================================
# DATA AND INTERFACES TAB
# ============================================================================
import streamlit as st
import pandas as pd

def render_data_interfaces():
    """Render the Data and Interfaces configuration form"""
    st.markdown('<p class="tab-header">Data and Interfaces</p>', unsafe_allow_html=True)
    
    # Initialize session state for data interfaces if not exists
    if 'data_interfaces' not in st.session_state:
        st.session_state.data_interfaces = {
            'employee_data': '',
            'employee_id_zeros': '',
            'employee_id_length': '',
            'pii_consideration': '',
            'hri_oti_review': '',
            'web_traffic_hostnames': [],
            'hr_interface': {
                'initial_load': '',
                'data_update': '',
                'update_timing': {
                    'day': '',
                    'time': '',
                    'frequency': ''
                },
                'do_not_overwrite': ''
            },
            'overtime_interface': {
                'update_method': '',
                'manual_entry_requirements': [],
                'electronic_load_timing': '',
                'multiple_paycodes': ''
            }
        }
    
    # Employee Data Section
    st.markdown("## Employee Data")
    st.markdown("Please list the data elements that you and the ARCOS implementation team believe you will need to transfer to ARCOS")
    
    # Employee Data Input
    st.session_state.data_interfaces['employee_data'] = st.text_area(
        "Data Elements", 
        value=st.session_state.data_interfaces['employee_data'],
        height=100
    )
    
    # Employee ID Considerations
    st.markdown("### Employee ID Details")
    col1, col2 = st.columns(2)
    
    with col1:
        st.session_state.data_interfaces['employee_id_zeros'] = st.radio(
            "Do employee IDs include leading zeros?",
            ["Yes", "No"],
            index=["Yes", "No"].index(st.session_state.data_interfaces['employee_id_zeros']) 
                if st.session_state.data_interfaces['employee_id_zeros'] in ["Yes", "No"] 
                else 0
        )
    
    with col2:
        st.session_state.data_interfaces['employee_id_length'] = st.radio(
            "Is the employee ID fixed or variable length?",
            ["Fixed", "Variable"],
            index=["Fixed", "Variable"].index(st.session_state.data_interfaces['employee_id_length']) 
                if st.session_state.data_interfaces['employee_id_length'] in ["Fixed", "Variable"] 
                else 0
        )
    
    # PII Consideration
    st.markdown("### Personally Identifiable Information (PII)")
    st.session_state.data_interfaces['pii_consideration'] = st.text_input(
        "Are the above data elements considered PII at your company?",
        value=st.session_state.data_interfaces['pii_consideration']
    )
    
    st.info("Note: Will IT and Security Teams need to be involved due to data transmission and use of SAAS infrastructure")
    
    # HRI and OTI File Review
    st.session_state.data_interfaces['hri_oti_review'] = st.text_input(
        "Customer has reviewed and understands the HRI and OTI file specifications document",
        value=st.session_state.data_interfaces['hri_oti_review']
    )
    
    # Web Traffic Interface
    st.markdown("## Web Traffic Interface (All web traffic in and out of ARCOS)")
    st.markdown("Your IT Department should allow traffic to and from the following hostnames for all web traffic")
    
    # Web Traffic Hostnames
    default_hostnames = [
        'prod.rostermonster.com',
        'backup.rostermonster.com',
        'qa.rostermonster.com'
    ]
    
    # Allow adding/removing hostnames
    st.session_state.data_interfaces['web_traffic_hostnames'] = st.multiselect(
        "Web Traffic Hostnames",
        options=default_hostnames,
        default=st.session_state.data_interfaces['web_traffic_hostnames'] or default_hostnames
    )
    
    # HR Interface Section
    st.markdown("## HR Interface (Employee Data sent to ARCOS)")
    
    # Initial Load Method
    st.markdown("### 1. How will all Employee Records be initially loaded into ARCOS?")
    st.session_state.data_interfaces['hr_interface']['initial_load'] = st.radio(
        "Initial Load Method",
        ["Manually", "Electronically"],
        index=["Manually", "Electronically"].index(st.session_state.data_interfaces['hr_interface']['initial_load']) 
            if st.session_state.data_interfaces['hr_interface']['initial_load'] in ["Manually", "Electronically"] 
            else 0
    )
    
    # Data Update Method
    st.markdown("### 2. How will you update employee data in ARCOS (other than overtime hours)?")
    st.session_state.data_interfaces['hr_interface']['data_update'] = st.radio(
        "Data Update Method",
        ["Manually", "Electronically"],
        index=["Manually", "Electronically"].index(st.session_state.data_interfaces['hr_interface']['data_update']) 
            if st.session_state.data_interfaces['hr_interface']['data_update'] in ["Manually", "Electronically"] 
            else 0
    )
    
    # Electronic Update Timing
    if st.session_state.data_interfaces['hr_interface']['data_update'] == "Electronically":
        st.markdown("### 3. Electronic Update Timing")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.session_state.data_interfaces['hr_interface']['update_timing']['day'] = st.text_input(
                "Day of Week",
                value=st.session_state.data_interfaces['hr_interface']['update_timing']['day']
            )
        
        with col2:
            st.session_state.data_interfaces['hr_interface']['update_timing']['time'] = st.text_input(
                "Exact Time of Day",
                value=st.session_state.data_interfaces['hr_interface']['update_timing']['time']
            )
        
        with col3:
            st.session_state.data_interfaces['hr_interface']['update_timing']['frequency'] = st.text_input(
                "Frequency",
                value=st.session_state.data_interfaces['hr_interface']['update_timing']['frequency']
            )
    
    # Fields Not to Overwrite
    st.markdown("### 4. Fields Not to Overwrite")
    st.session_state.data_interfaces['hr_interface']['do_not_overwrite'] = st.text_input(
        "Do not overwrite",
        value=st.session_state.data_interfaces['hr_interface']['do_not_overwrite']
    )
    
    # Overtime Interface Section
    st.markdown("## Overtime Interface (Employee hours sent to ARCOS)")
    
    # Overtime Update Method
    st.markdown("### 1. Overtime Hours Update Method")
    st.session_state.data_interfaces['overtime_interface']['update_method'] = st.radio(
        "Will you update employee overtime hours manually or electronically?",
        ["Manually", "Electronically"],
        index=["Manually", "Electronically"].index(st.session_state.data_interfaces['overtime_interface']['update_method']) 
            if st.session_state.data_interfaces['overtime_interface']['update_method'] in ["Manually", "Electronically"] 
            else 0
    )
    
    # Manual Entry Requirements
    if st.session_state.data_interfaces['overtime_interface']['update_method'] == "Manually":
        st.markdown("### 2. Manual Entry Requirements")
        manual_options = ["Edit OT Hours Page", "Daily Overtime Entry Page", "Adjusted Hours Field"]
        st.session_state.data_interfaces['overtime_interface']['manual_entry_requirements'] = st.multiselect(
            "Which of the following are required for manual entry?",
            options=manual_options,
            default=st.session_state.data_interfaces['overtime_interface']['manual_entry_requirements']
        )
    
    # Electronic Overtime Loading
    st.markdown("### 3. Electronic Overtime Hours Loading")
    st.session_state.data_interfaces['overtime_interface']['electronic_load_timing'] = st.radio(
        "If sending overtime hours electronically, should the hours load immediately or require preview?",
        ["Immediately", "Preview Required"],
        index=["Immediately", "Preview Required"].index(st.session_state.data_interfaces['overtime_interface']['electronic_load_timing']) 
            if st.session_state.data_interfaces['overtime_interface']['electronic_load_timing'] in ["Immediately", "Preview Required"] 
            else 0
    )
    
    # Multiple Paycodes
    st.markdown("### 4. Multiple Paycodes")
    multiple_paycodes_options = ["Yes", "No"]
    st.session_state.data_interfaces['overtime_interface']['multiple_paycodes'] = st.radio(
        "Do you require ARCOS to display multiple paycodes (overtime hour types), such as 'time and a half', 'double time', 'refused hours', or specific type of work that splits hours?",
        multiple_paycodes_options,
        index=multiple_paycodes_options.index(st.session_state.data_interfaces['overtime_interface']['multiple_paycodes']) 
            if st.session_state.data_interfaces['overtime_interface']['multiple_paycodes'] in multiple_paycodes_options 
            else 0
    )
    
    # Additional Details for Multiple Paycodes
    if st.session_state.data_interfaces['overtime_interface']['multiple_paycodes'] == "Yes":
        st.text_input(
            "Please elaborate on the multiple paycodes",
            value=st.session_state.data_interfaces.get('multiple_paycodes_details', '')
        )