# app.py

import streamlit as st
from config.constants import ARCOS_RED, PAGE_TITLE, PAGE_LAYOUT, SIDEBAR_STATE
from utils.session import initialize_session_state
from utils.exports import get_csv_data, get_excel_data
from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from utils.ui_helpers import render_icon_tabs
from tabs.location_hierarchy import render_location_hierarchy_form
from tabs.trouble_locations import render_trouble_locations_form
from tabs.job_classifications import render_job_classifications
from tabs.callout_reasons import render_callout_reasons_form
from tabs.event_types import render_event_types_form
from tabs.matrix_locations import render_matrix_locations_callout_types
from tabs.generic_tab import render_generic_tab
from datetime import datetime
import uuid

st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

def main():
    initialize_session_state()

    if 'session_unique_id' not in st.session_state:
        st.session_state.session_unique_id = str(uuid.uuid4())

    unique_id = st.session_state.session_unique_id

    with st.sidebar:
        render_sidebar(unique_id)

    main_content = st.container()
    with main_content:
        render_header()

        tabs = [
            "Location Hierarchy", "Trouble Locations", "Job Classifications",
            "Callout Reasons", "Event Types", "Callout Type Configuration",
            "Global Configuration Options", "Data and Interfaces", "Additions"
        ]

        tab_icons = {
            "Location Hierarchy": "🏢", "Trouble Locations": "📍", "Job Classifications": "👷",
            "Callout Reasons": "📞", "Event Types": "📆", "Callout Type Configuration": "⚙️",
            "Global Configuration Options": "🌐", "Data and Interfaces": "🔗", "Additions": "➕"
        }

        completed_tabs = sum(1 for tab in tabs if any(k.startswith(tab.replace(" ", "_").lower()) for k in st.session_state.get("responses", {})))
        progress = completed_tabs / len(tabs)
        st.progress(progress)
        st.write(f"{int(progress * 100)}% complete")

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
            else:
                render_generic_tab(current_tab)
        except Exception as e:
            st.error(f"Error rendering tab: {str(e)}")
            import traceback
            print(traceback.format_exc())

        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)

    render_footer(unique_id)

if __name__ == "__main__":
    main()
