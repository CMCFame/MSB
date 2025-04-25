# Comprehensive mapping of 53 Global Configuration Questions
import streamlit as st

def render_global_config_question(question, session_prefix='global_config_'):
    """Render a specific question based on its type"""
    session_key = f"{session_prefix}{question['id']}"
    
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
            value=st.session_state.global_config_answers.get(session_key, 0),
            key=session_key
        )
    elif question['type'] == 'radio':
        return st.radio(
            question['question'], 
            options=question.get('options', []),
            index=st.session_state.global_config_answers.get(session_key, 0),
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
    return 53  # Explicitly set to 53 as per document

def get_answered_questions():
    """Count answered questions"""
    return len([
        q for q in st.session_state.global_config_answers.values() 
        if q not in (None, '', False, 0)
    ])

def get_categories():
    """Get unique categories"""
    return sorted(set(
        category 
        for section in GLOBAL_CONFIG_QUESTIONS.values() 
        for category in set(q['category'] for q in section)
    ))

GLOBAL_CONFIG_QUESTIONS = {
    "Roster Administration": [
        # Roster Sorting Methods
        {"id": "1a_alpha", "category": "Roster Sorting Methods", 
         "question": "Alpha", "type": "checkbox"},
        {"id": "1a_seniority", "category": "Roster Sorting Methods", 
         "question": "Seniority", "type": "checkbox"},
        {"id": "1a_overtime", "category": "Roster Sorting Methods", 
         "question": "Overtime", "type": "checkbox"},
        {"id": "1a_pointer_last_attempted", "category": "Roster Sorting Methods", 
         "question": "Pointer - Last Attempted", "type": "checkbox"},
        {"id": "1a_pointer_last_accepted", "category": "Roster Sorting Methods", 
         "question": "Pointer - Last Accepted", "type": "checkbox"},
        {"id": "1a_rotate", "category": "Roster Sorting Methods", 
         "question": "Rotate", "type": "checkbox"},
        {"id": "1a_maintain_sort", "category": "Roster Sorting Methods", 
         "question": "Maintain Sort", "type": "checkbox"},
        
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
         "question": "If CTT was selected, list applicable CO Types", "type": "text", 
         "depends_on": "1b_ctt"},
        {"id": "1b_tts", "category": "ARCOS Add-On Features", 
         "question": "Text-To-Speech (TTS)", "type": "checkbox"},
        {"id": "1b_monthly_extract", "category": "ARCOS Add-On Features", 
         "question": "Monthly Data Extract", "type": "checkbox"}
    ],
    "Calling Configuration": [
        {"id": "2_calling_methods", "category": "Calling Methods", 
         "question": "Which calling methods are required? (Horizontal, Vertical)", "type": "text"},
        {"id": "3_exclusive_rule", "category": "Exclusive Rule", 
         "question": "Is the Exclusive Rule required?", "type": "text"},
        {"id": "4_exclude_all_hands", "category": "Exclude from All Hands", 
         "question": "Is the Exclude from All Hands field required?", "type": "text"}
    ],
    "VRU Configuration": [
        {"id": "5_device_limit", "category": "Device Limitations", 
         "question": "How many devices can an employee have active at one time? (Up to three)", "type": "number"},
        {"id": "6_device_modification", "category": "Device Modification", 
         "question": "Which devices are employees allowed to modify through the Inbound system? (First, second, third, all, or none)", "type": "text"},
        {"id": "7_temp_callout_numbers", "category": "Temporary Numbers", 
         "question": "How many temporary numbers are allowed per employee? (Callout)", "type": "number"},
        {"id": "7_temp_mobile_numbers", "category": "Temporary Numbers", 
         "question": "How many temporary numbers are allowed per employee? (Mobile)", "type": "number"},
        {"id": "7a_temp_callout_duration", "category": "Temporary Number Duration", 
         "question": "Temporary number should be set for a maximum of hours (Callout, Default: 72)", "type": "number", "default": 72},
        {"id": "7a_temp_mobile_duration", "category": "Temporary Number Duration", 
         "question": "Temporary number should be set for a maximum of hours (Mobile, Default: 72)", "type": "number", "default": 72},
        {"id": "8_temp_callout_replace", "category": "Temporary Number Replacement", 
         "question": "Which permanent device will the temporary callout number replace? (First, second, or third)", "type": "text"},
        {"id": "8_temp_mobile_replace", "category": "Temporary Number Replacement", 
         "question": "Which permanent device will the temporary mobile number replace? (First, second, or third)", "type": "text"},
        {"id": "8a_callout_percentage", "category": "Callout Percentage Reporting", 
         "question": "Do you want employees to hear their callout percentage via Inbound? If so, how should the percentage be spoken?", "type": "text"},
        {"id": "9_duty_phone", "category": "Duty Phone", 
         "question": "Do you require a Duty Phone?", "type": "text"},
        {"id": "10_pin_requirement", "category": "PIN Requirement", 
         "question": "Do you require a PIN to be entered by employees on Outbound calls?", "type": "text"},
        {"id": "12_callback_qualified_no", "category": "Callback Configuration", 
         "question": "When calling back an employee that pressed 9 for Qualified No, should ARCOS call: (Only the device on which the employee responded, Call all devices)", "type": "text"},
        {"id": "13_reaccept_declined", "category": "Reaccept Configuration", 
         "question": "Can an employee accept an open position through the Inbound system if they had already declined that position earlier?", "type": "text"},
        {"id": "15_final_result_rules", "category": "Final Result Rules", 
         "question": "Which of the following 'Final Result' rules do you have? (A: Do not call again for entire callout, B: Can be called again for different position, C: Can be called if callout is resubmitted)", "type": "text"}
    ],
    "One Call Configuration": [
        {"id": "16_one_call_co_main", "category": "One Call per Co Main", 
         "question": "Do you require one call per Co Main? (Employee will not be called on multiple sub-callouts but could be called multiple times WITHIN sub-callouts)", "type": "text"},
        {"id": "17_one_call_co", "category": "One Call per Co", 
         "question": "Do you require one call per Co? (An employee will not be called more than once when on a series of chained rosters)", "type": "text"}
    ],
    "Availability Configuration": [
        {"id": "18_availability_threshold", "category": "Availability Response Percentage", 
         "question": "What is the lowest percentage to keep text black?", "type": "number"},
        {"id": "19_zero_calls_percentage", "category": "Zero Calls Percentage", 
         "question": "If an employee has received zero calls, should ARCOS display their percentage as: (0% or 100%)", "type": "text"},
        {"id": "20_availability_rounding", "category": "Availability Percentage Rounding", 
         "question": "Should the Availability % round down or to the nearest integer?", "type": "text"},
        {"id": "21_separate_availability", "category": "On-Call/On-Duty Availability", 
         "question": "Do you track the availability % of employees separately when they are On Call or On Duty?", "type": "text"}
    ],
    "Employee Page Configuration": [
        {"id": "22_radio_field", "category": "Radio Field", 
         "question": "Do you require the Radio field? If yes, where do you want to see it? (Roster view, Roster maintenance, Scheduler, Manual bypass)", "type": "text"},
        {"id": "23_vehicle_field", "category": "Vehicle Field", 
         "question": "Do you require the Vehicle field? If so, which configuration? (Type, String, Vehicle ID)", "type": "text"}
    ],
    "Work and Rest Rules": [
        {"id": "24_automatic_rest", "category": "Automatic Rest Status", 
         "question": "Should ARCOS automatically place an employee on Rest status when released from working status if rest requirements are met?", "type": "text"},
        {"id": "25_rest_rule", "category": "Rest Rule", 
         "question": "If you answered Yes to automatic rest, which Rest Rule do you use?", "type": "text"},
        {"id": "26_working_screen_thresholds", "category": "Working Screen Color Thresholds", 
         "question": "What consecutive or cumulative hours determine when an employee's record on the Working Screen will display in yellow and red?", "type": "text"},
        {"id": "27_cumulative_hours", "category": "Cumulative Hours Calculation", 
         "question": "How does your cumulative hours calculation work? (Example: Do you look at all hours worked in the last 36 hours where a break of 4 hours or more has not occurred?)", "type": "text"}
    ],
    "Charge and Credit Configuration": [
        {"id": "28_call_result_charges_reached", "category": "Call Result Charges", 
         "question": "For employee reached but non-accept (Employee Not Home, Hangup, Invalid Entry), what is the charge?", "type": "text"},
        {"id": "28_call_result_charges_not_reached", "category": "Call Result Charges", 
         "question": "For employee not reached (Answering Machine, Busy, No Answer), what is the charge?", "type": "text"},
        {"id": "28_call_result_charges_phone_errors", "category": "Call Result Charges", 
         "question": "For employee not reached due to phone company errors, what is the charge?", "type": "text"},
        {"id": "29_max_charges_credits", "category": "Maximum Charges and Credits", 
         "question": "What are the maximum charges and credits an employee can receive, and in what time frame?", "type": "text"},
        {"id": "30_response_window", "category": "Response Window", 
         "question": "What is the maximum time an employee has to call Inbound to respond to a callout after receiving an Outbound call they did not respond to before being subject to a charge?", "type": "text"},
        {"id": "31_grace_period", "category": "Grace Period", 
         "question": "What is the Grace Period before and after a working status and associated charges?", "type": "text"},
        {"id": "32_uncalled_devices", "category": "Uncalled Devices", 
         "question": "Should an employee be excused (not receive a charge) if the callout is stopped or ends and the employee has uncalled devices?", "type": "text"},
        {"id": "32a_above_employee_acceptance", "category": "Above Employee Acceptance Rule", 
         "question": "Are there any rules related to whether an 'above employee' on the roster accepted? Does it matter if the list is exhausted?", "type": "text"}
    ],
    "Miscellaneous Configuration": [
        {"id": "33_holdover_functionality", "category": "Holdover Configuration", 
         "question": "Does your company use Holdover functionality?", "type": "text"},
        {"id": "34_holdover_name", "category": "Holdover Configuration", 
         "question": "If Yes, what do you call it?", "type": "text"},
        {"id": "35_default_holdover_length", "category": "Holdover Configuration", 
         "question": "What is the default length of a Holdover? (Minimum 4 hours)", "type": "text"},
        # Release Methods (Checkboxes)
        {"id": "release_web_interface", "category": "Release Methods", 
         "question": "ARCOS user releases through web interface", "type": "checkbox"},
        {"id": "release_touch_tone", "category": "Release Methods", 
         "question": "Employee calls in and releases via touch-tone phone", "type": "checkbox"},
        {"id": "release_normal_shift", "category": "Release Methods", 
         "question": "Employee released when callout/holdover continues into normal shift", "type": "checkbox"},
        {"id": "release_automatic", "category": "Release Methods", 
         "question": "Automatic release from holdover when selected end time is reached", "type": "checkbox"},     
        {"id": "40_serial_calling", "category": "Serial Calling Progression", 
         "question": "If using Serial Calling, when should ARCOS proceed to the next subcallout? (Wait or Done)", "type": "text"},
        {"id": "41_bypass_one_call", "category": "Bypass Configuration", 
         "question": "If using one call per co_main, do you need 'bypass one call per co_main' configured?", "type": "text"},
        {"id": "42_bypass_reason", "category": "Bypass Reason Requirement", 
         "question": "If manually bypassing an employee on a callout, what is the reason/comment requirement? (A: Not required, B: Required but not for unchecked, C: Required for each bypassed employee)", "type": "text"},
        {"id": "43_callout_auto_close", "category": "Callout Auto-Close", 
         "question": "How long will ARCOS wait before auto-closing a callout in Wait status when no one is working? (Min: 2 hours, Max: 48)", "type": "number"},
        {"id": "44_wait_status_acknowledge", "category": "Wait Status Configuration", 
         "question": "Do you require an Acknowledge button on the pop-up window when a callout goes to wait status?", "type": "text"},
        {"id": "45_shift_week", "category": "Shift Week Configuration", 
         "question": "What is considered the Shift Week? (Sunday-Saturday, Monday-Sunday, Saturday-Friday, Other)", "type": "text"},
        {"id": "46_holiday_assignment", "category": "Holiday Assignment", 
         "question": "Do you require Holidays to be assigned: (By location or System-wide)", "type": "text"},
        {"id": "47_location_access_security", "category": "Location Access", 
         "question": "Do you require the Location Access security function?", "type": "text"},
        {"id": "48_future_roster_assignments", "category": "Future Roster Assignments", 
         "question": "Do you require the Future Roster Assignments feature?", "type": "text"}
    ],
    "New Year Configuration": [
        {"id": "49_new_year_start", "category": "New Year Start", 
         "question": "When does the new year begin in your organization? (January 1st, Fiscal Year, Other)", "type": "text"},
        {"id": "50_roster_resequencing", "category": "Roster Resequencing", 
         "question": "What does the first day of the year mean to rosters? Do all rosters resequence on the same day?", "type": "text"},
        {"id": "51_chain_delay", "category": "Chain Delay", 
         "question": "Do you require Chain Delay and Chain Delay pop-up features?", "type": "text"},
        {"id": "52_date_selector", "category": "Date Selector", 
         "question": "Do you require a date selector on the Roster View and Callout List report?", "type": "text"},
        {"id": "53_crew_request", "category": "Crew Request", 
         "question": "Do you require the Crew Request functionality?", "type": "text"}
    ],
    "Landing Page Configuration": [
        {"id": "landing_page_welcome", "category": "Welcome Message", 
         "question": "What text should be used for the Landing Page Welcome message? (Typically just the customer name)", "type": "text"}
    ]
}

def export_questions_to_csv():
    """Export questions to a CSV for reference"""
    import csv
    import io

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Section", "Category", "Question ID", "Question"])
    
    for section, questions in GLOBAL_CONFIG_QUESTIONS.items():
        for question in questions:
            writer.writerow([
                section, 
                question.get('category', ''), 
                question['id'], 
                question['question']
            ])
    
    return output.getvalue()