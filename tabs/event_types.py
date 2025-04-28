# ============================================================================
# EVENT TYPES TAB
# ============================================================================
import streamlit as st
from datetime import datetime
from utils.ai_assistant import get_openai_response, save_chat_history

def render_event_types_form():
    """Render the Event Types form with improved alignment and shorter questions"""
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
    
    # Add New Event Type button
    add_col1, add_col2 = st.columns([6, 1])
    with add_col1:
        # Create a visually styled button container
        st.markdown(
            """
            <div style="background-color: #f8f9fa; border-radius: 4px; padding: 8px; 
                 text-align: center; margin: 10px 0; cursor: pointer;"
                 onclick="document.getElementById('hidden_add_button').click();">
                <span>➕ Add New Event Type</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Hidden button - placed in a column but without the label_visibility parameter
    with add_col2:
        if st.button("Add", key="hidden_add_button"):
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
    
    # CSS for better table-like styling
    st.markdown("""
    <style>
    /* Better header styling */
    .header-row {
        display: flex;
        background-color: #f2f2f2;
        border-bottom: 1px solid #ddd;
        padding: 5px 0;
        margin-bottom: 5px;
    }
    .header-cell {
        font-weight: bold;
        font-size: 12px;
        text-align: center;
        overflow: hidden;
        padding: 2px;
    }
    /* Custom form element styling */
    .stCheckbox > div {
        justify-content: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Shortened headers with clearer text
    headers = [
        "Event Description",
        "Use?",
        "Use in Module",
        "Include in Override?",
        "If override: Charged/Excused?",
        "If skipped: Charged/Excused?",
        "Can use Inbound?",
        "Mobile Release?",
        "Mobile Auto Rest?",
        "Mobile Unavailable?",
        "Mobile Rest Status?",
        "Min Hours",
        "Max Hours"
    ]
    
    # Column widths based on header content
    col_widths = [2, 0.7, 1.2, 1.5, 2, 2, 1.2, 1, 1, 1, 1, 0.7, 0.7]
    
    # Create header row
    header_cols = st.columns(col_widths)
    for i, header in enumerate(headers):
        with header_cols[i]:
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 11px;'>{header}</div>", unsafe_allow_html=True)
    
    # Create rows for each event
    for i, event in enumerate(filtered_events):
        # Create a row with the same column proportions
        event_cols = st.columns(col_widths)
        
        with event_cols[0]:
            event["description"] = st.text_input(
                "Description", 
                value=event.get("description", ""), 
                key=f"event_desc_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[1]:
            event["use"] = st.checkbox(
                "Use", 
                value=event.get("use", False), 
                key=f"event_use_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[2]:
            event["use_in_dropdown"] = st.checkbox(
                "Dropdown", 
                value=event.get("use_in_dropdown", False), 
                key=f"event_dropdown_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[3]:
            event["include_in_override"] = st.checkbox(
                "Override", 
                value=event.get("include_in_override", False), 
                key=f"event_override_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[4]:
            charged_options = ["", "Charged", "Excused"]
            current_value = event.get("charged_or_excused", "")
            current_index = 0
            if current_value in charged_options:
                current_index = charged_options.index(current_value)
                
            event["charged_or_excused"] = st.selectbox(
                "If override", 
                charged_options, 
                index=current_index,
                key=f"event_charge1_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[5]:
            skipped_options = ["", "Charged", "Excused"]
            current_value = event.get("employee_on_exception", "")
            current_index = 0
            if current_value in skipped_options:
                current_index = skipped_options.index(current_value)
                
            event["employee_on_exception"] = st.selectbox(
                "If skipped", 
                skipped_options, 
                index=current_index,
                key=f"event_charge2_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[6]:
            inbound_options = ["", "Yes", "No"]
            current_value = event.get("available_on_inbound", "")
            current_index = 0
            if current_value in inbound_options:
                current_index = inbound_options.index(current_value)
                
            event["available_on_inbound"] = st.selectbox(
                "Inbound", 
                inbound_options, 
                index=current_index,
                key=f"event_inbound_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[7]:
            event["release_mobile"] = st.checkbox(
                "Release", 
                value=event.get("release_mobile", False), 
                key=f"event_release_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[8]:
            event["release_auto"] = st.checkbox(
                "Auto Rest", 
                value=event.get("release_auto", False), 
                key=f"event_auto_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[9]:
            event["make_unavailable"] = st.checkbox(
                "Unavailable", 
                value=event.get("make_unavailable", False), 
                key=f"event_unavail_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[10]:
            event["place_status"] = st.checkbox(
                "Status", 
                value=event.get("place_status", False), 
                key=f"event_status_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[11]:
            event["min_duration"] = st.text_input(
                "Min", 
                value=event.get("min_duration", ""), 
                key=f"event_min_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[12]:
            event["max_duration"] = st.text_input(
                "Max", 
                value=event.get("max_duration", ""), 
                key=f"event_max_{i}",
                label_visibility="collapsed"
            )
        
        # Delete button in a separate row
        delete_cols = st.columns([12, 1])
        with delete_cols[1]:
            if st.button("🗑️", key=f"del_event_{i}"):
                st.session_state.event_types.pop(i)
                st.rerun()
        
        # Add separator between rows
        st.markdown("<hr style='margin: 2px 0; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    # Export buttons at the bottom
    export_cols = st.columns(2)
    with export_cols[0]:
        st.button("Export as CSV", key="export_csv")
    with export_cols[1]:
        st.button("Export as Excel", key="export_excel")
    
    # Help section at the bottom
    help_cols = st.columns([3, 1])
    with help_cols[1]:
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