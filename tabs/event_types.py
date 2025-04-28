# ============================================================================
# EVENT TYPES TAB
# ============================================================================
import streamlit as st
from datetime import datetime
import pandas as pd
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
        - Answer the questions in columns D-G, where appropriate.
        """)
    
    # Initialize event types if not in session state
    if 'event_types' not in st.session_state:
        st.session_state.event_types = [
            {
                "id": "1001",
                "description": "Working - Normal Shift",
                "use": True,
                "use_in_dropdown": True,
                "include_in_override": False,
                "charged_or_excused_override": "Excused",
                "charged_or_excused_skipped": "Excused",
                "available_on_inbound": "No",
                "release_mobile": False,
                "auto_rest": False,
                "make_unavailable": False,
                "place_status": False,
                "min_duration": "0",
                "max_duration": "16"
            },
            {
                "id": "1002",
                "description": "Discipline",
                "use": True,
                "use_in_dropdown": True,
                "include_in_override": True,
                "charged_or_excused_override": "Excused",
                "charged_or_excused_skipped": "Excused",
                "available_on_inbound": "No",
                "release_mobile": True,
                "auto_rest": False,
                "make_unavailable": True,
                "place_status": False,
                "min_duration": "1",
                "max_duration": "24"
            },
            {
                "id": "1003",
                "description": "Sick",
                "use": True,
                "use_in_dropdown": True,
                "include_in_override": True,
                "charged_or_excused_override": "Excused",
                "charged_or_excused_skipped": "Excused",
                "available_on_inbound": "No",
                "release_mobile": True,
                "auto_rest": False,
                "make_unavailable": True,
                "place_status": False,
                "min_duration": "1",
                "max_duration": "24"
            },
            {
                "id": "1004",
                "description": "Vacation",
                "use": True,
                "use_in_dropdown": True,
                "include_in_override": False,
                "charged_or_excused_override": "Excused",
                "charged_or_excused_skipped": "Excused",
                "available_on_inbound": "No",
                "release_mobile": True,
                "auto_rest": False,
                "make_unavailable": True,
                "place_status": False,
                "min_duration": "8",
                "max_duration": "168"
            }
        ]
    
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
    
    # Add New Event Type button - consistent with screenshot
    if st.button("➕ Add New Event Type", key="add_event_type"):
        # Generate new ID (just increment the highest existing ID)
        existing_ids = [int(event["id"]) for event in st.session_state.event_types]
        new_id = str(max(existing_ids) + 1) if existing_ids else "1001"
        
        # Add new empty event type
        st.session_state.event_types.append({
            "id": new_id,
            "description": "",
            "use": False,
            "use_in_dropdown": False,
            "include_in_override": False,
            "charged_or_excused_override": "",
            "charged_or_excused_skipped": "",
            "available_on_inbound": "",
            "release_mobile": False,
            "auto_rest": False,
            "make_unavailable": False,
            "place_status": False,
            "min_duration": "",
            "max_duration": ""
        })
        st.rerun()
    
    # Filter options
    st.markdown('<div style="margin-top: 10px;"></div>', unsafe_allow_html=True)
    filter_cols = st.columns([3, 1])
    with filter_cols[0]:
        st.write("Filter Event Types:")
    with filter_cols[1]:
        show_active_only = st.checkbox("Show active only", value=False, key="show_active_events")
    
    # Apply filter
    filtered_events = st.session_state.event_types
    if show_active_only:
        filtered_events = [event for event in filtered_events if event["use"]]
    
    # Table header - matches screenshot format
    event_cols = st.columns([4, 1, 1, 2, 2, 2, 2])
    
    with event_cols[0]:
        st.markdown('<div style="font-weight: bold;">Event Description</div>', unsafe_allow_html=True)
    with event_cols[1]:
        st.markdown('<div style="font-weight: bold;">Use?</div>', unsafe_allow_html=True)
    with event_cols[2]:
        st.markdown('<div style="font-weight: bold;">Use in Dropdown</div>', unsafe_allow_html=True)
    with event_cols[3]:
        st.markdown('<div style="font-weight: bold;">Include in Override ALL?</div>', unsafe_allow_html=True)
    with event_cols[4]:
        st.markdown('<div style="font-weight: bold;">If override occurs...</div>', unsafe_allow_html=True)
    with event_cols[5]:
        st.markdown('<div style="font-weight: bold;">If employee is skipped...</div>', unsafe_allow_html=True)
    with event_cols[6]:
        st.markdown('<div style="font-weight: bold;">Can employee place on Inbound?</div>', unsafe_allow_html=True)
    
    # Create each row for event types
    for i, event in enumerate(filtered_events):
        # Main row for basic settings
        event_cols = st.columns([4, 1, 1, 2, 2, 2, 2])
        
        with event_cols[0]:
            # Description
            event["description"] = st.text_input(
                "Description", 
                value=event["description"], 
                key=f"event_desc_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[1]:
            # Use checkbox
            event["use"] = st.checkbox(
                "Use", 
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
            if "charged_or_excused_override" not in event:
                event["charged_or_excused_override"] = ""
                
            selected_index = 0
            if event["charged_or_excused_override"] == "Charged":
                selected_index = 1
            elif event["charged_or_excused_override"] == "Excused":
                selected_index = 2
                
            event["charged_or_excused_override"] = st.selectbox(
                "If override occurs", 
                ["", "Charged", "Excused"], 
                index=selected_index,
                key=f"event_charge1_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[5]:
            # Charged or excused selection for skipped
            if "charged_or_excused_skipped" not in event:
                event["charged_or_excused_skipped"] = ""
                
            selected_index = 0
            if event["charged_or_excused_skipped"] == "Charged":
                selected_index = 1
            elif event["charged_or_excused_skipped"] == "Excused":
                selected_index = 2
                
            event["charged_or_excused_skipped"] = st.selectbox(
                "If employee is skipped", 
                ["", "Charged", "Excused"], 
                index=selected_index,
                key=f"event_charge2_{i}",
                label_visibility="collapsed"
            )
        
        with event_cols[6]:
            # Can place on inbound selection
            if "available_on_inbound" not in event:
                event["available_on_inbound"] = ""
                
            selected_index = 0
            if event["available_on_inbound"] == "Yes":
                selected_index = 1
            elif event["available_on_inbound"] == "No":
                selected_index = 2
                
            event["available_on_inbound"] = st.selectbox(
                "Available on Inbound", 
                ["", "Yes", "No"], 
                index=selected_index,
                key=f"event_inbound_{i}",
                label_visibility="collapsed"
            )
        
        # Mobile settings in an additional row (hidden by default)
        mobile_settings_col = st.columns([1])
        with mobile_settings_col[0]:
            mobile_container = st.expander(f"Additional settings for {event['description']}", expanded=False)
            with mobile_container:
                m_cols1 = st.columns([3, 3, 3, 3])
                m_cols2 = st.columns([3, 3, 6])
                
                with m_cols1[0]:
                    # Release via mobile
                    event["release_mobile"] = st.checkbox(
                        "Allow users to be released from this schedule record via Mobile?", 
                        value=event["release_mobile"], 
                        key=f"event_release_{i}"
                    )
                
                with m_cols1[1]:
                    # Auto rest status
                    event["auto_rest"] = st.checkbox(
                        "Allow users to automatically enter rest status from this schedule record via Mobile?", 
                        value=event["auto_rest"], 
                        key=f"event_auto_{i}"
                    )
                
                with m_cols1[2]:
                    # Make unavailable
                    event["make_unavailable"] = st.checkbox(
                        "Allow users to make themselves unavailable using this schedule record via Mobile?", 
                        value=event["make_unavailable"], 
                        key=f"event_unavail_{i}"
                    )
                
                with m_cols1[3]:
                    # Place on status
                    event["place_status"] = st.checkbox(
                        "Allow users to place themselves on this status via rest status via Mobile?", 
                        value=event["place_status"], 
                        key=f"event_status_{i}"
                    )
                
                with m_cols2[0]:
                    # Min duration
                    event["min_duration"] = st.text_input(
                        "What is the minimum duration users can place themselves on this schedule record? (In Hours)", 
                        value=event["min_duration"], 
                        key=f"event_min_{i}"
                    )
                
                with m_cols2[1]:
                    # Max duration
                    event["max_duration"] = st.text_input(
                        "What is the maximum duration users can place themselves on this schedule record? (In Hours)", 
                        value=event["max_duration"], 
                        key=f"event_max_{i}"
                    )
                
                with m_cols2[2]:
                    # Remove button
                    if st.button("🗑️ Remove Event Type", key=f"remove_event_{i}"):
                        st.session_state.event_types.pop(i)
                        st.rerun()
    
.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Simpler help section - button only as in screenshot
    help_container = st.container()
    with help_container:
        st.markdown('<div style="text-align: right;">Need Help?</div>', unsafe_allow_html=True)
        help_topic = st.selectbox(
            "Select topic for help",
            ["Event Types", "Schedule Exceptions", "Override Configuration", "Mobile Configuration"]
        )
        
        if st.button("Get Help", key="get_help_btn"):
            help_query = f"Explain in detail what I need to know about {help_topic} when configuring ARCOS Event Types. Include examples and best practices."
            with st.spinner("Getting help..."):
                help_response = get_openai_response(help_query)
                save_chat_history(f"Help with {help_topic}", help_response)
            
            st.info(help_response)