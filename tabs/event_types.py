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
    
    # Add button for new event type
    if st.button("➕ Add New Event Type"):
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
    filter_cols = st.columns([3, 1])
    with filter_cols[0]:
        st.write("Filter Event Types:")
    with filter_cols[1]:
        show_active_only = st.checkbox("Show active only", value=False, key="show_active_events")
    
    # Apply filter
    filtered_events = st.session_state.event_types
    if show_active_only:
        filtered_events = [event for event in filtered_events if event["use"]]
    
    # Table header
    st.markdown("""
    <div style="display: flex; margin-bottom: 10px; font-weight: bold; background-color: #f0f0f0; padding: 8px 0;">
        <div style="flex: 2; padding: 0 5px;">Event Description</div>
        <div style="flex: 1; padding: 0 5px; text-align: center;">Use?</div>
        <div style="flex: 1; padding: 0 5px; text-align: center;">Use in Dropdown</div>
        <div style="flex: 1.5; padding: 0 5px; text-align: center;">Include in Override ALL?</div>
        <div style="flex: 2; padding: 0 5px; text-align: center;">If override occurs...</div>
        <div style="flex: 2; padding: 0 5px; text-align: center;">If employee is skipped...</div>
        <div style="flex: 2; padding: 0 5px; text-align: center;">Can employee place on Inbound?</div>
        <div style="flex: 0.5; padding: 0 5px; text-align: center;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create each row for event types
    for i, event in enumerate(filtered_events):
        # Main row for basic settings
        event_container = st.container()
        with event_container:
            cols = st.columns([2, 1, 1, 1.5, 2, 2, 2, 0.5])
            
            with cols[0]:
                # Description
                event["description"] = st.text_input(
                    "Description", 
                    value=event["description"], 
                    key=f"event_desc_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[1]:
                # Use checkbox
                event["use"] = st.checkbox(
                    "Use", 
                    value=event["use"], 
                    key=f"event_use_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[2]:
                # Use in dropdown checkbox
                event["use_in_dropdown"] = st.checkbox(
                    "Use in Dropdown", 
                    value=event["use_in_dropdown"], 
                    key=f"event_dropdown_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[3]:
                # Override checkbox
                event["include_in_override"] = st.checkbox(
                    "Include in Override", 
                    value=event["include_in_override"], 
                    key=f"event_override_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[4]:
                # Charged or excused selection for non-accept
                event["charged_or_excused_override"] = st.selectbox(
                    "If override occurs", 
                    ["", "Charged", "Excused"], 
                    index=0 if not event["charged_or_excused_override"] else 
                          (1 if event["charged_or_excused_override"] == "Charged" else 2),
                    key=f"event_charge1_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[5]:
                # Charged or excused selection for skipped
                event["charged_or_excused_skipped"] = st.selectbox(
                    "If employee is skipped", 
                    ["", "Charged", "Excused"], 
                    index=0 if not event["charged_or_excused_skipped"] else 
                          (1 if event["charged_or_excused_skipped"] == "Charged" else 2),
                    key=f"event_charge2_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[6]:
                # Can place on inbound selection
                event["available_on_inbound"] = st.selectbox(
                    "Available on Inbound", 
                    ["", "Yes", "No"], 
                    index=0 if not event["available_on_inbound"] else 
                          (1 if event["available_on_inbound"] == "Yes" else 2),
                    key=f"event_inbound_{i}",
                    label_visibility="collapsed"
                )
            
            with cols[7]:
                # Expand/collapse button
                expand = st.button("⮟", key=f"expand_{i}")
        
        # Expanded section for mobile settings
        # Use a separate container for the expanded section
        expanded_container = st.container()
        
        # Store expansion state in session state
        if f"expanded_{i}" not in st.session_state:
            st.session_state[f"expanded_{i}"] = False
        
        # Toggle expansion state when button is clicked
        if expand:
            st.session_state[f"expanded_{i}"] = not st.session_state[f"expanded_{i}"]
        
        # Show expanded content if expanded
        if st.session_state[f"expanded_{i}"]:
            with expanded_container:
                st.markdown(f"""
                <div style="background-color: #f9f9f9; padding: 10px; margin-bottom: 15px; border-left: 3px solid #e3051b;">
                    <h4>Mobile Settings for: {event["description"]}</h4>
                </div>
                """, unsafe_allow_html=True)
                
                mobile_cols = st.columns([2, 2, 2, 2, 2, 2])
                
                with mobile_cols[0]:
                    # Release via mobile
                    event["release_mobile"] = st.checkbox(
                        "Release via Mobile", 
                        value=event["release_mobile"], 
                        key=f"event_release_{i}"
                    )
                
                with mobile_cols[1]:
                    # Auto rest status
                    event["auto_rest"] = st.checkbox(
                        "Auto Enter Rest Status", 
                        value=event["auto_rest"], 
                        key=f"event_auto_{i}"
                    )
                
                with mobile_cols[2]:
                    # Make unavailable
                    event["make_unavailable"] = st.checkbox(
                        "Make Unavailable via Mobile", 
                        value=event["make_unavailable"], 
                        key=f"event_unavail_{i}"
                    )
                
                with mobile_cols[3]:
                    # Place on status
                    event["place_status"] = st.checkbox(
                        "Place on Rest Status", 
                        value=event["place_status"], 
                        key=f"event_status_{i}"
                    )
                
                with mobile_cols[4]:
                    # Min duration
                    event["min_duration"] = st.text_input(
                        "Min Duration (hours)", 
                        value=event["min_duration"], 
                        key=f"event_min_{i}"
                    )
                
                with mobile_cols[5]:
                    # Max duration
                    event["max_duration"] = st.text_input(
                        "Max Duration (hours)", 
                        value=event["max_duration"], 
                        key=f"event_max_{i}"
                    )
            
                # Remove button
                if st.button("🗑️ Remove Event Type", key=f"remove_event_{i}"):
                    st.session_state.event_types.pop(i)
                    st.rerun()
        
        # Add a horizontal line between rows for better readability
        st.markdown("<hr style='margin: 5px 0; border: none; border-top: 1px solid #ddd;'>", unsafe_allow_html=True)
    
    # Export to CSV/Excel section
    st.markdown("<hr>", unsafe_allow_html=True)
    export_cols = st.columns(2)
    
    with export_cols[0]:
        if st.button("Export to CSV"):
            # Create DataFrame for export
            export_data = []
            for event in st.session_state.event_types:
                export_data.append({
                    "ID": event["id"],
                    "Description": event["description"],
                    "Use": "X" if event["use"] else "",
                    "Use in Dropdown": "X" if event["use_in_dropdown"] else "",
                    "Include in Override": "X" if event["include_in_override"] else "",
                    "Charged/Excused (Override)": event["charged_or_excused_override"],
                    "Charged/Excused (Skipped)": event["charged_or_excused_skipped"],
                    "Available on Inbound": event["available_on_inbound"],
                    "Release via Mobile": "X" if event["release_mobile"] else "",
                    "Auto Rest": "X" if event["auto_rest"] else "",
                    "Make Unavailable": "X" if event["make_unavailable"] else "",
                    "Place on Status": "X" if event["place_status"] else "",
                    "Min Duration": event["min_duration"],
                    "Max Duration": event["max_duration"]
                })
            
            export_df = pd.DataFrame(export_data)
            csv = export_df.to_csv(index=False)
            
            # Generate download link
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="event_types.csv",
                mime="text/csv"
            )
    
    with export_cols[1]:
        if st.button("Export to Excel"):
            # Create DataFrame for export
            export_data = []
            for event in st.session_state.event_types:
                export_data.append({
                    "ID": event["id"],
                    "Description": event["description"],
                    "Use": "X" if event["use"] else "",
                    "Use in Dropdown": "X" if event["use_in_dropdown"] else "",
                    "Include in Override": "X" if event["include_in_override"] else "",
                    "Charged/Excused (Override)": event["charged_or_excused_override"],
                    "Charged/Excused (Skipped)": event["charged_or_excused_skipped"],
                    "Available on Inbound": event["available_on_inbound"],
                    "Release via Mobile": "X" if event["release_mobile"] else "",
                    "Auto Rest": "X" if event["auto_rest"] else "",
                    "Make Unavailable": "X" if event["make_unavailable"] else "",
                    "Place on Status": "X" if event["place_status"] else "",
                    "Min Duration": event["min_duration"],
                    "Max Duration": event["max_duration"]
                })
            
            export_df = pd.DataFrame(export_data)
            
            # Use BytesIO to create Excel file
            import io
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                export_df.to_excel(writer, sheet_name='Event Types', index=False)
                
                # Auto-adjust column widths
                worksheet = writer.sheets['Event Types']
                for i, col in enumerate(export_df.columns):
                    # Find the maximum length in this column
                    column_len = max(export_df[col].astype(str).map(len).max(), len(col))
                    # Set the width to this length plus some padding
                    worksheet.set_column(i, i, column_len + 2)
            
            # Generate download link
            st.download_button(
                label="Download Excel",
                data=buffer.getvalue(),
                file_name="event_types.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
    
    # Help section
    st.markdown("<hr>", unsafe_allow_html=True)
    help_container = st.container()
    with help_container:
        st.markdown('<div class="section-header" style="margin-top: 20px;">Need Help?</div>', unsafe_allow_html=True)
        help_topic = st.selectbox(
            "Select topic for help",
            ["Event Types Overview", "Schedule Exceptions", "Override Configuration", 
             "Mobile Configuration", "Charged vs Excused"]
        )
        
        if st.button("Get Help"):
            help_query = f"Explain in detail what I need to know about {help_topic} when configuring ARCOS Event Types. Include examples and best practices."
            with st.spinner("Loading help..."):
                help_response = get_openai_response(help_query)
                save_chat_history(f"Help with {help_topic}", help_response)
            
            st.info(help_response)