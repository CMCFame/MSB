# ============================================================================
# SESSION STATE MANAGEMENT
# ============================================================================
import streamlit as st
import json
from config.constants import (
    DEFAULT_HIERARCHY_DATA, 
    DEFAULT_CALLOUT_TYPES, 
    DEFAULT_CALLOUT_REASONS,
    DEFAULT_JOB_CLASSIFICATION,
    DEFAULT_TROUBLE_LOCATION
)

def initialize_session_state():
    """Initialize session state variables if they don't exist"""
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = "Location Hierarchy"
        
    if 'hierarchy_data' not in st.session_state:
        # Initialize with default data
        st.session_state.hierarchy_data = DEFAULT_HIERARCHY_DATA
    
    # If existing entries don't have callout_types or callout_reasons fields, add them
    if 'hierarchy_data' in st.session_state:
        for entry in st.session_state.hierarchy_data["entries"]:
            if "callout_types" not in entry:
                entry["callout_types"] = {
                    "Normal": False,
                    "All Hands on Deck": False,
                    "Fill Shift": False,
                    "Travel": False,
                    "Notification": False,
                    "Notification (No Response)": False
                }
            if "callout_reasons" not in entry:
                entry["callout_reasons"] = ""
        
    if 'callout_types' not in st.session_state:
        st.session_state.callout_types = DEFAULT_CALLOUT_TYPES
    
    if 'callout_reasons' not in st.session_state:
        st.session_state.callout_reasons = DEFAULT_CALLOUT_REASONS
        
    if 'job_classifications' not in st.session_state:
        st.session_state.job_classifications = [DEFAULT_JOB_CLASSIFICATION]
    
    if 'trouble_locations' not in st.session_state:
        st.session_state.trouble_locations = [DEFAULT_TROUBLE_LOCATION]
    
    if 'event_types' not in st.session_state:
        # Initialize event types with default data (this will be populated from actual defaults later)
        st.session_state.event_types = load_default_event_types()
    
    if 'selected_callout_reasons' not in st.session_state:
        try:
            # Try to load from callout_reasons.json
            callout_reasons = load_callout_reasons()
            st.session_state.selected_callout_reasons = [r["ID"] for r in callout_reasons if r.get("Use?") == "x"]
        except:
            # Default to empty if can't load
            st.session_state.selected_callout_reasons = []
    
    if 'default_callout_reason' not in st.session_state:
        try:
            callout_reasons = load_callout_reasons()
            default_reasons = [r["ID"] for r in callout_reasons if r.get("Default?") == "x"]
            st.session_state.default_callout_reason = default_reasons[0] if default_reasons else ""
        except:
            st.session_state.default_callout_reason = ""
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 0

def load_callout_reasons():
    """Load callout reasons from JSON file"""
    try:
        with open('data/callout_reasons.json', 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading callout reasons: {str(e)}")
        # Return a basic set if file can't be loaded
        return [
            {"ID": "0", "Callout Reason Drop-Down Label": "", "Use?": "x", "Default?": "x", "Verbiage": "n/a"},
            {"ID": "1001", "Callout Reason Drop-Down Label": "Broken Line", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1002", "Callout Reason Drop-Down Label": "Depression Road", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1003", "Callout Reason Drop-Down Label": "Depression Yard", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1007", "Callout Reason Drop-Down Label": "Emergency", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"},
            {"ID": "1008", "Callout Reason Drop-Down Label": "Odor", "Use?": "x", "Default?": "", "Verbiage": "Pre-recorded"}
        ]

def load_default_event_types():
    """Load default event types"""
    return [
        {
            "id": "1001",
            "description": "Working - Normal Shift",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        },
        {
            "id": "1017",
            "description": "Discipline",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        },
        {
            "id": "1018",
            "description": "Sick",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        },
        # Add more default event types as needed
        {
            "id": "1024",
            "description": "Vacation",
            "use": True,
            "use_in_dropdown": True,
            "include_in_override": False,
            "charged_or_excused": "",
            "available_on_inbound": "",
            "employee_on_exception": "",
            "release_mobile": False,
            "release_auto": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        }
    ]