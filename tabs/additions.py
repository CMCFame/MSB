# ============================================================================
# ADDITIONS TAB
# ============================================================================
import streamlit as st

def render_additions():
    """Render the Additions configuration form"""
    st.markdown('<p class="tab-header">Additions</p>', unsafe_allow_html=True)
    
    # Initialize session state for additions if not exists
    if 'additions' not in st.session_state:
        st.session_state.additions = {
            # Contact Devices
            'standby_device': '',
            
            # Closest-to-the-Trouble (CTT)
            'ctt_callout_type': '',
            'ctt_truck_in_garage': '',
            'ctt_sort_basis': '',
            'ctt_method': '',
            'ctt_bullseye_calling': {
                'used': '',
                'ot_order': '',
                'home_address': '',
                'employee_location': ''
            },
            
            # Qualifications
            'qual_version': '',
            'qual_callout_types': '',
            'extended_attributes': {
                'required': '',
                'options': [],
                'storm_category': '',
                'loader_attribute': '',
                'ext_attr_matrix': ''
            },
            
            # J/A Rule Usage
            'ja_rule': '',
            'ja_rule_example': '',
            
            # Crew in a Barrel
            'crew_barrel_min_max': '',
            
            # Dates in Employee Record
            'employee_record_dates': '',
            
            # Email Alerts
            'email_alerts': [],
            
            # Vacation Management
            'vlg_configuration': '',
            'vacation_award_basis': '',
            'vacation_days': '',
            'max_unavailable_employees': '',
            'time_off_calculation': '',
            'vacation_days_exceptions': '',
            'personal_days_exceptions': ''
        }
    
    # Contact Devices Section
    st.markdown("## Contact Devices")
    st.session_state.additions['standby_device'] = st.text_input(
        "Does the Employee Record require a Stand By device?",
        value=st.session_state.additions['standby_device']
    )
    
    # Closest-to-the-Trouble (CTT) Section
    st.markdown("## Closest-to-the-Trouble (CTT)")
    
    # Conditional CTT Configuration
    st.markdown("If customer is using CTT question 9 on Tab 7 has been answered")
    st.session_state.additions['ctt_callout_type'] = st.text_input(
        "Callout Type that will use CTT",
        value=st.session_state.additions['ctt_callout_type']
    )
    
    st.markdown("### CTT Configuration")
    st.session_state.additions['ctt_truck_in_garage'] = st.text_input(
        "1. Will CTT use 'Truck in Garage'?",
        value=st.session_state.additions['ctt_truck_in_garage']
    )
    
    st.session_state.additions['ctt_sort_basis'] = st.text_input(
        "2. Should the CTT sort be based on Level 4 Address or the employee home address?",
        value=st.session_state.additions['ctt_sort_basis']
    )
    
    st.session_state.additions['ctt_method'] = st.text_input(
        "3. What should the CTT Method be at callout time? (Default: Raw Distance, Drive Distance, Drive Time, All)",
        value=st.session_state.additions['ctt_method']
    )
    
    st.markdown("### CTT Bullseye Calling")
    st.session_state.additions['ctt_bullseye_calling']['used'] = st.text_input(
        "4. Will CTT with Bullseye Calling be used?",
        value=st.session_state.additions['ctt_bullseye_calling']['used']
    )
    
    # Conditional Bullseye Calling Details
    if st.session_state.additions['ctt_bullseye_calling']['used'].lower() in ['yes', 'y']:
        st.markdown("#### Bullseye Calling Considerations")
        st.session_state.additions['ctt_bullseye_calling']['ot_order'] = st.text_input(
            "a. Consider OT order?",
            value=st.session_state.additions['ctt_bullseye_calling']['ot_order']
        )
        st.session_state.additions['ctt_bullseye_calling']['home_address'] = st.text_input(
            "b. Consider employee home address?",
            value=st.session_state.additions['ctt_bullseye_calling']['home_address']
        )
        st.session_state.additions['ctt_bullseye_calling']['employee_location'] = st.text_input(
            "c. Consider employee location?",
            value=st.session_state.additions['ctt_bullseye_calling']['employee_location']
        )
    
    # Qualifications Section
    st.markdown("## Qualifications (Qual's)")
    st.session_state.additions['qual_version'] = st.text_input(
        "Which version of QUAL's is required? (CMS or PPL Version)",
        value=st.session_state.additions['qual_version']
    )
    
    st.session_state.additions['qual_callout_types'] = st.text_input(
        "List all Callout types that should recognize QUAL's.",
        value=st.session_state.additions['qual_callout_types']
    )
    
    st.info("Note: The use of QUAL's requires Extended Attributes to be enabled.")
    
    # Extended Attributes Section
    st.markdown("## Extended Attributes")
    st.session_state.additions['extended_attributes']['required'] = st.text_input(
        "Will Extended attributes be required?",
        value=st.session_state.additions['extended_attributes']['required']
    )
    
    st.markdown("### Extended Attribute Options")
    extended_attr_options = [
        "Extended Employee Attribute Admin Page",
        "Attribute Standard Category",
        "Attribute Search"
    ]
    st.session_state.additions['extended_attributes']['options'] = st.multiselect(
        "Enabling Extended Attributes includes the following options:",
        options=extended_attr_options,
        default=st.session_state.additions['extended_attributes']['options']
    )
    
    st.session_state.additions['extended_attributes']['storm_category'] = st.text_input(
        "Is the Attribute Storm Category required? (Only available with SOS)",
        value=st.session_state.additions['extended_attributes']['storm_category']
    )
    
    st.session_state.additions['extended_attributes']['loader_attribute'] = st.text_input(
        "Is the Loader Attribute option required? (Must be enabled to add or modify extended attributes through the loader)",
        value=st.session_state.additions['extended_attributes']['loader_attribute']
    )
    
    st.session_state.additions['extended_attributes']['ext_attr_matrix'] = st.text_input(
        "Is the Ext Attr Matrix required? (Only available with SOS)",
        value=st.session_state.additions['extended_attributes']['ext_attr_matrix']
    )
    
    # J/A Rule Usage Section
    st.markdown("## J/A Rule Usage")
    st.session_state.additions['ja_rule'] = st.text_input(
        "Which J/A Rule will be used.",
        value=st.session_state.additions['ja_rule']
    )
    
    st.session_state.additions['ja_rule_example'] = st.text_area(
        "Please provide an example of the J/A Rule requirements. Example: Only one Apprentice is allowed to accept for any callout and for single person callouts, Apprentices are unavailable.",
        value=st.session_state.additions['ja_rule_example']
    )
    
    # Crew in a Barrel Section
    st.markdown("## Crew in a Barrel")
    st.session_state.additions['crew_barrel_min_max'] = st.text_input(
        "Min and Max for making unavailable.",
        value=st.session_state.additions['crew_barrel_min_max']
    )
    
    # Dates in Employee Record Section
    st.markdown("## Dates in Employee Record")
    st.session_state.additions['employee_record_dates'] = st.text_input(
        "Seniority Date, Service Date, Birthday Date (Show Tie breakers, identify fields when using different dates in different fields)",
        value=st.session_state.additions['employee_record_dates']
    )
    
    # Email Alerts Section
    st.markdown("## Email Alerts")
    email_alert_options = [
        "Callout Complete",
        "Audit Alert",
        "Callout Done/Closed",
        "Callout Done/Stop Managers",
        "Vacation Management"
    ]
    st.session_state.additions['email_alerts'] = st.multiselect(
        "Select email alerts to configure:",
        options=email_alert_options,
        default=st.session_state.additions['email_alerts']
    )
    
    # Vacation Management Section
    st.markdown("## Vacation Management")
    st.session_state.additions['vlg_configuration'] = st.text_input(
        "How to configure VLG's.",
        value=st.session_state.additions['vlg_configuration']
    )
    
    st.session_state.additions['vacation_award_basis'] = st.text_input(
        "How do you determine the time to award or allot an employee? (Service date, Hire date, Seniority date - This is the date vacation hours resets)",
        value=st.session_state.additions['vacation_award_basis']
    )
    
    st.session_state.additions['vacation_days'] = st.text_input(
        "How many days are employees entitled to vacation within a given timeframe?",
        value=st.session_state.additions['vacation_days']
    )
    
    st.session_state.additions['max_unavailable_employees'] = st.text_input(
        "How many employees can be unavailable where you do not compromise the ability to respond to an emergency?",
        value=st.session_state.additions['max_unavailable_employees']
    )
    
    st.session_state.additions['time_off_calculation'] = st.text_input(
        "Is the time off calculated by hours or by days?",
        value=st.session_state.additions['time_off_calculation']
    )
    
    st.session_state.additions['vacation_days_exceptions'] = st.text_input(
        "Which exceptions account toward Vacation Days calculated?",
        value=st.session_state.additions['vacation_days_exceptions']
    )
    
    st.session_state.additions['personal_days_exceptions'] = st.text_input(
        "Which exceptions account toward Personal Days calculated?",
        value=st.session_state.additions['personal_days_exceptions']
    )