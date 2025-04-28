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
    
    # Add button for new event type
    if st.button("➕ Add New Event Type", key="add_new_event_type"):
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
            "available_on_inbound": "",
            "employee_on_exception": "",
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
    
    # Create better readable headers - each in its own container to avoid text cutoff
    # Create a horizontal scroll container for all headers
    st.markdown("""
    <style>
    .scrollable-header {
        overflow-x: auto;
        white-space: nowrap;
        display: flex;
        margin-bottom: 10px;
        background-color: #f0f0f0; 
        padding: 8px 0;
    }
    .header-cell {
        display: inline-block;
        padding: 5px 10px;
        font-weight: bold;
        text-align: center;
        min-width: 150px;
        max-width: 200px;
        word-wrap: break-word;
        white-space: normal;
        vertical-align: top;
    }
    </style>
    
    <div class="scrollable-header">
        <div class="header-cell" style="width: 200px;">Event Description</div>
        <div class="header-cell" style="width: 60px;">Use?</div>
        <div class="header-cell" style="width: 130px;">Use in Schedule Module Dropdown</div>
        <div class="header-cell" style="width: 130px;">Include in Override ALL?</div>
        <div class="header-cell" style="width: 200px;">If an override occurs on this Schedule Exception and the employee is called and results in a non-accept, should the employee be Charged or Excused?</div>
        <div class="header-cell" style="width: 200px;">If an employee is skipped during a callout due to being on this Schedule Exception, should he be Charged or Excused?</div>
        <div class="header-cell" style="width: 180px;">Can the employee place themselves on this Exception on Inbound?</div>
        <div class="header-cell" style="width: 140px;">Allow users to be released from this schedule record via Mobile?</div>
        <div class="header-cell" style="width: 140px;">Allow users to automatically enter rest status from this schedule record via Mobile?</div>
        <div class="header-cell" style="width: 140px;">Allow users to make themselves unavailable using this schedule record via Mobile?</div>
        <div class="header-cell" style="width: 140px;">Allow users to place themselves on this status via rest status via Mobile?</div>
        <div class="header-cell" style="width: 140px;">What is the minimum duration users can place themselves on this schedule record? (In Hours)</div>
        <div class="header-cell" style="width: 140px;">What is the maximum duration users can place themselves on this schedule record? (In Hours)</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create scrollable container for the event data rows
    st.markdown("""
    <style>
    .scrollable-content {
        overflow-x: auto;
        white-space: nowrap;
    }
    .data-row {
        display: flex;
        margin-bottom: 10px;
        background-color: #fff;
        border-bottom: 1px solid #eee;
        padding: 8px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Divider
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    # For regular form elements, we still need to use Streamlit's built-in components
    # Create each row for event types in a more structured way
    for i, event in enumerate(filtered_events):
        # Event row using columns to maintain structure
        event_cols = st.columns([2, 1, 1.5, 1.5, 3, 3, 2, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5])
        
        with event_cols[0]:
            # Description
            event["description"] = st.text_input(
                "Event Description", 
                value=event["description"], 
                key=f"event_desc_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[1]:
            # Use checkbox
            event["use"] = st.checkbox(
                "Use?", 
                value=event["use"], 
                key=f"event_use_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[2]:
            # Use in dropdown checkbox
            event["use_in_dropdown"] = st.checkbox(
                "Use in Dropdown", 
                value=event["use_in_dropdown"], 
                key=f"event_dropdown_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[3]:
            # Override checkbox
            event["include_in_override"] = st.checkbox(
                "Include in Override", 
                value=event["include_in_override"], 
                key=f"event_override_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[4]:
            # Charged or excused selection for non-accept
            event["charged_or_excused"] = st.selectbox(
                "If override occurs...", 
                ["", "Charged", "Excused"], 
                index=0 if not event.get("charged_or_excused") else 
                      (1 if event["charged_or_excused"] == "Charged" else 2),
                key=f"event_charge1_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[5]:
            # Charged or excused selection for skipped
            event["employee_on_exception"] = st.selectbox(
                "If employee is skipped...", 
                ["", "Charged", "Excused"], 
                index=0 if not event.get("employee_on_exception") else 
                      (1 if event["employee_on_exception"] == "Charged" else 2),
                key=f"event_charge2_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[6]:
            # Can place on inbound selection
            event["available_on_inbound"] = st.selectbox(
                "Can place on Inbound?", 
                ["", "Yes", "No"], 
                index=0 if not event.get("available_on_inbound") else 
                      (1 if event["available_on_inbound"] == "Yes" else 2),
                key=f"event_inbound_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[7]:
            # Release via mobile
            event["release_mobile"] = st.checkbox(
                "Release via Mobile", 
                value=event.get("release_mobile", False), 
                key=f"event_release_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[8]:
            # Auto rest status
            event["release_auto"] = st.checkbox(
                "Auto Rest", 
                value=event.get("release_auto", False), 
                key=f"event_auto_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[9]:
            # Make unavailable
            event["make_unavailable"] = st.checkbox(
                "Make Unavailable", 
                value=event.get("make_unavailable", False), 
                key=f"event_unavail_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[10]:
            # Place on status
            event["place_status"] = st.checkbox(
                "Place Status", 
                value=event.get("place_status", False), 
                key=f"event_status_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[11]:
            # Min duration
            event["min_duration"] = st.text_input(
                "Min Duration", 
                value=event.get("min_duration", ""), 
                key=f"event_min_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[12]:
            # Max duration
            event["max_duration"] = st.text_input(
                "Max Duration", 
                value=event.get("max_duration", ""), 
                key=f"event_max_{i}",
                label_visibility="collapsed"
            )
        
        # Add remove button for this event type in a separate row
        remove_cols = st.columns([12, 1])
        with remove_cols[1]:
            if st.button("🗑️", key=f"remove_event_{i}", help="Remove this event type"):
                st.session_state.event_types.pop(i)
                st.rerun()
        
        # Add a horizontal line between rows for better readability
        st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    # Export buttons at the bottom
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
        
        if st.button("Get Help"):
            help_query = f"Explain in detail what I need to know about {help_topic} when configuring ARCOS. Include examples and best practices."
            with st.spinner("Loading help..."):
                help_response = get_openai_response(help_query)
                save_chat_history(f"Help with {help_topic}", help_response)
            
            st.info(help_response)