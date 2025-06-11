# app.py - Updated with Import/Export functionality

import streamlit as st
from config.constants import ARCOS_RED, PAGE_TITLE, PAGE_LAYOUT, SIDEBAR_STATE
from utils.session import initialize_session_state
from utils.exports import get_csv_data, get_excel_data
from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from utils.ui_helpers import render_icon_tabs, render_css
from tabs.location_hierarchy import render_location_hierarchy_form
from tabs.trouble_locations import render_trouble_locations_form
from tabs.job_classifications import render_job_classifications
from tabs.callout_reasons import render_callout_reasons_form
from tabs.event_types import render_event_types_form
from tabs.matrix_locations import render_matrix_locations_callout_types
from tabs.global_config import render_global_config
from tabs.data_interfaces import render_data_interfaces
from tabs.additions import render_additions
from datetime import datetime
import uuid

# Import the new data import module
try:
    from utils.data_import import render_import_export_section
    IMPORT_EXPORT_AVAILABLE = True
except ImportError:
    IMPORT_EXPORT_AVAILABLE = False

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

def main():
    initialize_session_state()
    render_css()

    if 'session_unique_id' not in st.session_state:
        st.session_state.session_unique_id = str(uuid.uuid4())

    unique_id = st.session_state.session_unique_id

    with st.sidebar:
        render_sidebar(unique_id)

    main_content = st.container()
    with main_content:
        render_header()
        
        # Add Import/Export section at the top
        if IMPORT_EXPORT_AVAILABLE:
            with st.expander("📁 Import/Export Data", expanded=False):
                render_import_export_section()
            st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)

        tabs = [
            "Location Hierarchy", "Trouble Locations", "Job Classifications",
            "Callout Reasons", "Event Types", "Callout Type Configuration",
            "Global Configuration", "Data and Interfaces", "Additions"
        ]

        tab_icons = {
            "Location Hierarchy": "🏢", "Trouble Locations": "📍", 
            "Job Classifications": "👷", "Callout Reasons": "📞", 
            "Event Types": "📆", "Callout Type Configuration": "⚙️",
            "Global Configuration": "🌐", 
            "Data and Interfaces": "🔗", "Additions": "➕"
        }

        # Calculate completion progress
        completed_tabs = 0
        total_tabs = len(tabs)
        
        # Check each tab for completion
        if 'hierarchy_data' in st.session_state and st.session_state.hierarchy_data.get("entries"):
            completed_tabs += 1
        if 'trouble_locations' in st.session_state and any(loc.get("location") for loc in st.session_state.trouble_locations):
            completed_tabs += 1
        if 'job_classifications' in st.session_state and any(job.get("title") for job in st.session_state.job_classifications):
            completed_tabs += 1
        if 'selected_callout_reasons' in st.session_state and st.session_state.selected_callout_reasons:
            completed_tabs += 1
        if 'event_types' in st.session_state and any(event.get("use") for event in st.session_state.event_types):
            completed_tabs += 1
        if 'responses' in st.session_state and any(k.startswith("matrix_") for k in st.session_state.responses):
            completed_tabs += 1
        if 'global_config_answers' in st.session_state and st.session_state.global_config_answers:
            completed_tabs += 1
        if 'data_interfaces' in st.session_state and any(v for v in st.session_state.data_interfaces.values() if v):
            completed_tabs += 1
        if 'additions' in st.session_state and any(v for v in st.session_state.additions.values() if v):
            completed_tabs += 1
        
        progress = completed_tabs / total_tabs
        st.progress(progress)
        st.write(f"📊 Progress: {completed_tabs}/{total_tabs} sections completed ({int(progress * 100)}%)")

        render_icon_tabs(tabs, tab_icons)

        st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)

        try:
            current_tab = st.session_state.get("current_tab", tabs[0])
            
            if current_tab == "Location Hierarchy":
                render_location_hierarchy_form()
            elif current_tab == "Trouble Locations":
                render_trouble_locations_form()
            elif current_tab == "Job Classifications":
                render_job_classifications()
            elif current_tab == "Callout Reasons":
                render_callout_reasons_form()
            elif current_tab == "Event Types":
                render_event_types_form()
            elif current_tab == "Callout Type Configuration":
                render_matrix_locations_callout_types()
            elif current_tab == "Global Configuration":
                render_global_config()
            elif current_tab == "Data and Interfaces":
                render_data_interfaces()
            elif current_tab == "Additions":
                render_additions()
                
        except Exception as e:
            st.error(f"Error rendering tab: {str(e)}")
            import traceback
            print(traceback.format_exc())
            # Show basic error recovery options
            st.markdown("### 🔧 Error Recovery")
            st.info("If you're experiencing issues, try refreshing the page or importing a backup file.")

        # Add some space for the floating footer
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    # Render the fixed footer with working export buttons
    render_footer(unique_id)

if __name__ == "__main__":
    main()