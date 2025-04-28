# ============================================================================
# EVENT TYPES TAB
# ============================================================================
import streamlit as st
from datetime import datetime
from utils.ai_assistant import get_openai_response, save_chat_history

def render_event_types_form():
    """Render the Event Types form with interactive elements matching the Excel format"""
    st.markdown('<p class="tab-header">Event Types</p>', unsafe_allow_html=True)
    
    # Display descriptive text
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        Following are the "Event Types" that are currently used in ARCOS.
        
        - Place an "X" in the "Use?" column for each Schedule Exception you want included in your system.
        - Place an "X" in the "Use in Schedule Module Dropdown" for those Events types used as exceptions and needed in the "Add Dropdown".
        - Add additional Event Types at the bottom of the list. Include all working Event Types as well.
        - Click on the drop-down arrow in cell B3 and select "X" to view only those Schedule Exceptions you will be using.
        - Answer the questions in columns D-G, where appropriate.
        """)
    
    # Main content area
    st.markdown('<p class="section-header">Event Types Configuration</p>', unsafe_allow_html=True)
    
    # Last Revision Date
    date_cols = st.columns([3, 1])
    with date_cols[0]:
        st.write("Last Revision Date:")
    with date_cols[1]:
        current_date = datetime.now().strftime("%m/%d/%Y")
        revision_date = st.text_input("", value=current_date, key="revision_date", 
                                     label_visibility="collapsed")
    
    # Add New Event Type button that matches the look in the screenshot
    add_col = st.container()
    with add_col:
        # Create a grey button that stretches across the container
        add_button = st.markdown(
            """
            <div style="background-color: #f8f9fa; border-radius: 5px; padding: 8px; text-align: center; cursor: pointer;"
                 onclick="document.getElementById('add_new_event_btn').click();">
                <span style="color: #6c757d;">➕ Add New Event Type</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Hidden button that will be triggered by the custom styled div
        if st.button("Add New Event Type", key="add_new_event_btn", label_visibility="collapsed"):
            # Generate new ID (just increment the highest existing ID)
            existing_ids = [int(event["id"]) for event in st.session_state.event_types]
            new_id = str(max(existing_ids) + 1) if existing_ids else "2000"
            
            # Add new empty event type
            st.session_state.event_types.append({
                "id": new_id,
                "description": "",
                "use": False,
                "use_in_dropdown": False,
                "include_in_override": False,
                "charged_or_excused": "",
                "employee_on_exception": "",
                "available_on_inbound": "",
                "release_mobile": False,
                "release_auto": False,
                "make_unavailable": False,
                "place_status": False,
                "min_duration": "",
                "max_duration": ""
            })
            st.rerun()
    
    # Filter options
    filter_cols = st.columns([3, 1])
    with filter_cols[0]:
        st.write("Filter Event Types:")
    with filter_cols[1]:
        show_active_only = st.checkbox("Show active only", value=False, key="show_active_events")
    
    # Apply filter
    filtered_events = st.session_state.event_types
    if show_active_only:
        filtered_events = [event for event in filtered_events if event["use"]]
    
    # Custom CSS for compact table and better alignment
    st.markdown("""
    <style>
    .compact-header {
        text-align: center;
        font-weight: bold;
        font-size: 0.8em;
        padding: 4px;
        height: 90px;
        overflow: hidden;
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        vertical-align: top;
    }
    .compact-table {
        width: 100%;
        overflow-x: auto;
        display: block;
        white-space: nowrap;
    }
    .compact-row {
        display: flex;
        margin-bottom: 4px;
        border-bottom: 1px solid #eee;
    }
    .compact-cell {
        padding: 4px;
        text-align: center;
        display: inline-block;
    }
    .stButton button {
        padding: 4px !important;
    }
    .stCheckbox > div {
        display: flex;
        justify-content: center;
    }
    
    /* Reduce input field padding */
    .st-emotion-cache-1a1dtzj.e1q9nlms0 {
        padding-top: 0px;
        padding-bottom: 0px;
    }
    
    /* Make selects and inputs smaller */
    div[data-baseweb="select"] {
        min-height: 32px !important;
    }
    
    .stSelectbox [data-testid="stMarkdownContainer"] {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Column headers - shortened to improve readability while showing key concepts
    column_headers = [
        "Event Description",
        "Use?",
        "Use in Schedule Module Dropdown",
        "Include in Override ALL?",
        "If override occurs...",
        "If employee is skipped...",
        "Can place on Inbound?",
        "Released via Mobile?",
        "Auto rest status?",
        "Make unavailable?",
        "Place on rest status?",
        "Min duration (hours)",
        "Max duration (hours)"
    ]
    
    # Full questions for tooltips - exact questions from the image
    full_headers = [
        "Event Description",
        "Use?",
        "Use in Schedule Module Dropdown",
        "Include in Override ALL?",
        "If an override occurs on this Schedule Exception and the employee is called and results in a non-accept, should the employee be Charged or Excused?",
        "If an employee is skipped during a callout due to being on this Schedule Exception, should he be Charged or Excused?",
        "Can the employee place themselves on this Exception on Inbound?",
        "Allow users to be released from this schedule record via Mobile?",
        "Allow users to automatically enter rest status from this schedule record via Mobile?",
        "Allow users to make themselves unavailable using this schedule record via Mobile?",
        "Allow users to place themselves on this status via rest status via Mobile?",
        "What is the minimum duration users can place themselves on this schedule record? (In Hours)",
        "What is the maximum duration users can place themselves on this schedule record? (In Hours)"
    ]
    
    # Render the headers with tooltips
    header_cols = st.columns([2, 1, 2, 1.5, 2, 2, 1.5, 1, 1, 1, 1, 1, 1])
    
    for i, (short_header, full_header) in enumerate(zip(column_headers, full_headers)):
        with header_cols[i]:
            st.markdown(
                f'<div title="{full_header}" style="font-weight: bold; text-align: center; font-size: 0.8em; white-space: normal; height: 60px; overflow: hidden;">{short_header}</div>',
                unsafe_allow_html=True
            )
    
    # Create each row for event types with the same column proportions
    for i, event in enumerate(filtered_events):
        # Create a row with the same column structure
        event_row = st.columns([2, 1, 2, 1.5, 2, 2, 1.5, 1, 1, 1, 1, 1, 1])
        
        with event_row[0]:
            # Description
            event["description"] = st.text_input(
                "Description", 
                value=event.get("description", ""), 
                key=f"event_desc_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[1]:
            # Use checkbox
            event["use"] = st.checkbox(
                "Use", 
                value=event.get("use", False), 
                key=f"event_use_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[2]:
            # Use in dropdown checkbox
            event["use_in_dropdown"] = st.checkbox(
                "Use in Dropdown", 
                value=event.get("use_in_dropdown", False), 
                key=f"event_dropdown_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[3]:
            # Include in Override ALL?
            event["include_in_override"] = st.checkbox(
                "Include in Override", 
                value=event.get("include_in_override", False), 
                key=f"event_override_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[4]:
            # If override occurs...
            charged_options = ["", "Charged", "Excused"]
            current_value = event.get("charged_or_excused", "")
            current_index = 0
            if current_value in charged_options:
                current_index = charged_options.index(current_value)
                
            event["charged_or_excused"] = st.selectbox(
                "If override occurs", 
                charged_options, 
                index=current_index,
                key=f"event_charge1_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[5]:
            # If employee is skipped...
            skipped_options = ["", "Charged", "Excused"]
            current_value = event.get("employee_on_exception", "")
            current_index = 0
            if current_value in skipped_options:
                current_index = skipped_options.index(current_value)
                
            event["employee_on_exception"] = st.selectbox(
                "If employee is skipped", 
                skipped_options, 
                index=current_index,
                key=f"event_charge2_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[6]:
            # Can place on inbound
            inbound_options = ["", "Yes", "No"]
            current_value = event.get("available_on_inbound", "")
            current_index = 0
            if current_value in inbound_options:
                current_index = inbound_options.index(current_value)
                
            event["available_on_inbound"] = st.selectbox(
                "Can employee place on Inbound", 
                inbound_options, 
                index=current_index,
                key=f"event_inbound_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[7]:
            # Release via mobile
            event["release_mobile"] = st.checkbox(
                "Release via Mobile", 
                value=event.get("release_mobile", False), 
                key=f"event_release_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[8]:
            # Auto rest status
            event["release_auto"] = st.checkbox(
                "Auto Rest", 
                value=event.get("release_auto", False), 
                key=f"event_auto_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[9]:
            # Make unavailable
            event["make_unavailable"] = st.checkbox(
                "Make Unavailable", 
                value=event.get("make_unavailable", False), 
                key=f"event_unavail_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[10]:
            # Place on status
            event["place_status"] = st.checkbox(
                "Place on Rest Status", 
                value=event.get("place_status", False), 
                key=f"event_status_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[11]:
            # Min duration
            event["min_duration"] = st.text_input(
                "Min Duration", 
                value=event.get("min_duration", ""), 
                key=f"event_min_{i}",
                label_visibility="collapsed"
            )
        
        with event_row[12]:
            # Max duration
            event["max_duration"] = st.text_input(
                "Max Duration", 
                value=event.get("max_duration", ""), 
                key=f"event_max_{i}",
                label_visibility="collapsed"
            )
        
        # Add delete button in a separate row to avoid cluttering the form
        trash_cols = st.columns([12, 1])
        with trash_cols[1]:
            if st.button("🗑️", key=f"remove_event_{i}"):
                st.session_state.event_types.pop(i)
                st.rerun()
        
        # Add a horizontal line between rows for better readability
        st.markdown("<hr style='margin: 2px 0; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    # Export buttons at the bottom - match screenshot styling
    export_cols = st.columns(2)
    with export_cols[0]:
        st.button("Export as CSV", key="export_csv")
    with export_cols[1]:
        st.button("Export as Excel", key="export_excel")
    
    # Side panel with help content
    help_cols = st.columns([3, 1])
    with help_cols[1]:
        # Help section
        st.markdown('<p class="section-header">Need Help?</p>', unsafe_allow_html=True)
        help_topic = st.selectbox(
            "Select topic for help",
            ["Event Types", "Schedule Exceptions", "Override Configuration", "Mobile Configuration"]
        )
        
        if st.button("Get Help", key="get_help"):
            help_query = f"Explain in detail what I need to know about {help_topic} when configuring ARCOS. Include examples and best practices."
            with st.spinner("Loading help..."):
                help_response = get_openai_response(help_query)
                save_chat_history(f"Help with {help_topic}", help_response)
            
            st.info(help_response)