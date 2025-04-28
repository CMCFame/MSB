# ============================================================================
# EVENT TYPES TAB - TABULAR LAYOUT
# ============================================================================
import streamlit as st
from datetime import datetime
import pandas as pd
from utils.ai_assistant import get_openai_response, save_chat_history

def render_event_types_form():
    """Render the Event Types form with a tabular layout for better alignment"""
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
    add_col = st.container()
    with add_col:
        add_button = st.markdown(
            """
            <div style="background-color: #f8f9fa; border-radius: 4px; padding: 8px; text-align: center; margin: 10px 0;">
                <span>➕ Add New Event Type</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Hidden button aligned with design
        if st.button("Add New Event Type", key="add_new_event_type", label_visibility="collapsed"):
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
    
    # More concise and clear question formulations
    questions = [
        # Original question: Event Description
        "Event Description",
        
        # Original question: Use?
        "Use?",
        
        # Original question: Use in Schedule Module Dropdown
        "Use in Module Dropdown",
        
        # Original question: Include in Override ALL?
        "Include in Override?",
        
        # Original question: If an override occurs on this Schedule Exception and the employee is called 
        # and results in a non-accept, should the employee be Charged or Excused?
        "Override occurs → Charged/Excused?",
        
        # Original question: If an employee is skipped during a callout due to being on this 
        # Schedule Exception, should he be Charged or Excused?
        "Skipped in callout → Charged/Excused?",
        
        # Original question: Can the employee place themselves on this Exception on Inbound?
        "Can place on Inbound?",
        
        # Original question: Allow users to be released from this schedule record via Mobile?
        "Released via Mobile?",
        
        # Original question: Allow users to automatically enter rest status from this schedule record via Mobile?
        "Auto rest via Mobile?",
        
        # Original question: Allow users to make themselves unavailable using this schedule record via Mobile?
        "Make unavailable via Mobile?",
        
        # Original question: Allow users to place themselves on this status via rest status via Mobile?
        "Place on rest status via Mobile?",
        
        # Original question: What is the minimum duration users can place themselves on this schedule record? (In Hours)
        "Min duration (Hours)",
        
        # Original question: What is the maximum duration users can place themselves on this schedule record? (In Hours)
        "Max duration (Hours)"
    ]
    
    # CSS for tabular layout
    st.markdown("""
    <style>
    .dataframe {
        width: 100%;
        border-collapse: collapse;
    }
    .dataframe th {
        text-align: center;
        background-color: #f2f2f2;
        padding: 8px 4px;
        border: 1px solid #ddd;
        font-size: 12px;
        font-weight: bold;
        vertical-align: middle;
        height: 50px;
    }
    .dataframe td {
        text-align: center;
        padding: 4px;
        border: 1px solid #ddd;
        background-color: #f9f9f9;
    }
    /* Make sure inputs and checkboxes are centered */
    .dataframe td > div {
        display: flex;
        justify-content: center;
    }
    /* Make delete button look like in screenshot */
    .delete-btn {
        background-color: transparent;
        border: none;
        color: #6c757d;
        cursor: pointer;
        padding: 0;
        font-size: 16px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create a DataFrame to display questions and event data
    # This approach uses an HTML table for better alignment
    st.markdown(
        f"""
        <table class="dataframe">
            <thead>
                <tr>
                    {"".join([f'<th>{q}</th>' for q in questions])}
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
        """
        , unsafe_allow_html=True
    )
    
    # Instead of using Streamlit's built-in components, we'll create form elements explicitly for each event
    for i, event in enumerate(filtered_events):
        # Create form elements with proper form IDs
        description_id = f"event_desc_{i}"
        use_id = f"event_use_{i}"
        dropdown_id = f"event_dropdown_{i}"
        override_id = f"event_override_{i}"
        charged_override_id = f"event_charged1_{i}"
        charged_skipped_id = f"event_charged2_{i}"
        inbound_id = f"event_inbound_{i}"
        release_id = f"event_release_{i}"
        auto_rest_id = f"event_auto_{i}"
        unavailable_id = f"event_unavail_{i}"
        status_id = f"event_status_{i}"
        min_id = f"event_min_{i}"
        max_id = f"event_max_{i}"
        delete_id = f"event_delete_{i}"
        
        # In this row, we'll use Streamlit elements, properly aligned in table cells
        st.markdown(f'<tr id="event_row_{i}">', unsafe_allow_html=True)
        
        # Event description
        st.markdown('<td>', unsafe_allow_html=True)
        event["description"] = st.text_input(
            "Description", 
            value=event.get("description", ""), 
            key=description_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Use checkbox
        st.markdown('<td>', unsafe_allow_html=True)
        event["use"] = st.checkbox(
            "Use", 
            value=event.get("use", False), 
            key=use_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Use in dropdown checkbox
        st.markdown('<td>', unsafe_allow_html=True)
        event["use_in_dropdown"] = st.checkbox(
            "Use in Dropdown", 
            value=event.get("use_in_dropdown", False), 
            key=dropdown_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Include in Override ALL?
        st.markdown('<td>', unsafe_allow_html=True)
        event["include_in_override"] = st.checkbox(
            "Include in Override", 
            value=event.get("include_in_override", False), 
            key=override_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # If override occurs...
        st.markdown('<td>', unsafe_allow_html=True)
        charged_options = ["", "Charged", "Excused"]
        current_value = event.get("charged_or_excused", "")
        current_index = 0
        if current_value in charged_options:
            current_index = charged_options.index(current_value)
            
        event["charged_or_excused"] = st.selectbox(
            "If override occurs", 
            charged_options, 
            index=current_index,
            key=charged_override_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # If employee is skipped...
        st.markdown('<td>', unsafe_allow_html=True)
        skipped_options = ["", "Charged", "Excused"]
        current_value = event.get("employee_on_exception", "")
        current_index = 0
        if current_value in skipped_options:
            current_index = skipped_options.index(current_value)
            
        event["employee_on_exception"] = st.selectbox(
            "If employee is skipped", 
            skipped_options, 
            index=current_index,
            key=charged_skipped_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Can place on inbound
        st.markdown('<td>', unsafe_allow_html=True)
        inbound_options = ["", "Yes", "No"]
        current_value = event.get("available_on_inbound", "")
        current_index = 0
        if current_value in inbound_options:
            current_index = inbound_options.index(current_value)
            
        event["available_on_inbound"] = st.selectbox(
            "Can employee place on Inbound", 
            inbound_options, 
            index=current_index,
            key=inbound_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Release via mobile
        st.markdown('<td>', unsafe_allow_html=True)
        event["release_mobile"] = st.checkbox(
            "Release via Mobile", 
            value=event.get("release_mobile", False), 
            key=release_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Auto rest status
        st.markdown('<td>', unsafe_allow_html=True)
        event["release_auto"] = st.checkbox(
            "Auto Rest", 
            value=event.get("release_auto", False), 
            key=auto_rest_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Make unavailable
        st.markdown('<td>', unsafe_allow_html=True)
        event["make_unavailable"] = st.checkbox(
            "Make Unavailable", 
            value=event.get("make_unavailable", False), 
            key=unavailable_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Place on status
        st.markdown('<td>', unsafe_allow_html=True)
        event["place_status"] = st.checkbox(
            "Place on Rest Status", 
            value=event.get("place_status", False), 
            key=status_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Min duration
        st.markdown('<td>', unsafe_allow_html=True)
        event["min_duration"] = st.text_input(
            "Min Duration", 
            value=event.get("min_duration", ""), 
            key=min_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Max duration
        st.markdown('<td>', unsafe_allow_html=True)
        event["max_duration"] = st.text_input(
            "Max Duration", 
            value=event.get("max_duration", ""), 
            key=max_id,
            label_visibility="collapsed"
        )
        st.markdown('</td>', unsafe_allow_html=True)
        
        # Delete button
        st.markdown('<td>', unsafe_allow_html=True)
        if st.button("🗑️", key=delete_id):
            st.session_state.event_types.pop(i)
            st.rerun()
        st.markdown('</td>', unsafe_allow_html=True)
        
        st.markdown('</tr>', unsafe_allow_html=True)
    
    # Close the table
    st.markdown('</tbody></table>', unsafe_allow_html=True)
    
    # Export buttons
    export_cols = st.columns(2)
    with export_cols[0]:
        st.button("Export as CSV", key="export_csv")
    with export_cols[1]:
        st.button("Export as Excel", key="export_excel")
    
    # Need help section
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