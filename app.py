# ============================================================================
# ARCOS SIG FORM - MAIN APPLICATION
# ============================================================================
import streamlit as st
from config.constants import ARCOS_RED, PAGE_TITLE, PAGE_LAYOUT, SIDEBAR_STATE
from utils.session import initialize_session_state
from utils.exports import get_csv_data, get_excel_data
from components.sidebar import render_sidebar
from components.header import render_header
from components.footer import render_footer
from tabs.location_hierarchy import render_location_hierarchy_form
from tabs.trouble_locations import render_trouble_locations_form
from tabs.job_classifications import render_job_classifications
from tabs.callout_reasons import render_callout_reasons_form
from tabs.event_types import render_event_types_form
from tabs.matrix_locations import render_matrix_locations_callout_types
from tabs.generic_tab import render_generic_tab
from datetime import datetime
import uuid

# ============================================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title=PAGE_TITLE,
    layout=PAGE_LAYOUT,
    initial_sidebar_state=SIDEBAR_STATE
)

# ============================================================================
# MAIN APPLICATION FUNCTION 
# ============================================================================
def main():
    """Main application function"""
    # Initialize session state
    initialize_session_state()
    
    # Create a unique ID for this session if it doesn't exist
    if 'session_unique_id' not in st.session_state:
        st.session_state.session_unique_id = str(uuid.uuid4())
    
    # Use the session unique ID for all keys
    unique_id = st.session_state.session_unique_id
    
    # Render sidebar
    with st.sidebar:
        render_sidebar(unique_id)
    
    # Main content area
    main_content = st.container()
    with main_content:
        # Display ARCOS logo and title
        render_header()
        
        # Define available tabs with their descriptions
        tabs = [
            {"name": "Location Hierarchy", "desc": "Configure your 4-level location structure"},
            {"name": "Trouble Locations", "desc": "Set up trouble locations and pronunciations"},
            {"name": "Job Classifications", "desc": "Define job roles and IDs"},
            {"name": "Callout Reasons", "desc": "Configure callout reasons and verbiage"},
            {"name": "Event Types", "desc": "Set up event types and exceptions"},
            {"name": "Callout Type Configuration", "desc": "Configure callout types and behaviors"},
            {"name": "Global Configuration Options", "desc": "Global settings and options"},
            {"name": "Data and Interfaces", "desc": "Configure data flows and integrations"},
            {"name": "Additions", "desc": "Additional configuration options"}
        ]
        
        # Calculate progress
        completed_tabs = sum(1 for tab in tabs if any(key.startswith(tab["name"].replace(" ", "_").lower()) for key in st.session_state.responses))
        progress = completed_tabs / len(tabs)
        st.progress(progress)
        st.write(f"{int(progress * 100)}% complete")
        
        # Custom CSS for smaller, more compact buttons
        st.markdown("""
        <style>
        /* Make tab buttons smaller and more compact */
        div[data-testid="column"] button[kind] {
            font-size: 12px !important;
            padding: 5px 8px !important;
            height: auto !important;
            min-height: 0 !important;
            white-space: normal !important;
            line-height: 1.2 !important;
        }
        
        /* Add icons using emoji for simplicity */
        .tab-label {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 10px;
            line-height: 1.2;
        }
        
        .tab-icon {
            font-size: 18px;
            margin-bottom: 2px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navigation section header
        st.write("Select section:")
        
        # Use Streamlit's built-in columns for a 3x3 grid
        col1, col2, col3 = st.columns(3)
        
        # Define icons using emoji (more reliable than external images)
        icons = ["🗺️", "📍", "📄", "🔔", "📅", "🔧", "🌐", "🔄", "➕"]
        
        # Create tabs as a 3x3 grid of small buttons with icons
        for i, tab in enumerate(tabs):
            # Determine which column to place the button in
            col = [col1, col2, col3][i % 3]
            
            # Create a button with emoji icon and text
            with col:
                # Create a label with icon and text
                button_label = f"""
                <div class="tab-label">
                    <div class="tab-icon">{icons[i]}</div>
                    {tab["name"]}
                </div>
                """
                
                # Create the button
                button_type = "primary" if tab["name"] == st.session_state.current_tab else "secondary"
                if st.button(tab["name"], key=f"tab_{i}", help=tab["desc"], type=button_type, use_container_width=True):
                    st.session_state.current_tab = tab["name"]
                    st.rerun()
        
        # Add a separator between navigation and content
        st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)
        
        # Main content area - render the appropriate tab
        content_container = st.container()
        with content_container:
            try:
                selected_tab = st.session_state.current_tab
                if selected_tab == "Location Hierarchy":
                    render_location_hierarchy_form()
                elif selected_tab == "Trouble Locations":
                    render_trouble_locations_form()
                elif selected_tab == "Job Classifications":
                    render_job_classifications()
                elif selected_tab == "Callout Reasons":
                    render_callout_reasons_form()
                elif selected_tab == "Event Types":
                    render_event_types_form()
                elif selected_tab == "Callout Type Configuration":
                    render_matrix_locations_callout_types()
                else:
                    # For other tabs, use the generic form renderer
                    render_generic_tab(selected_tab)
            except Exception as e:
                st.error(f"Error rendering tab: {str(e)}")
                # Print more detailed error for debugging
                import traceback
                print(f"Error details: {traceback.format_exc()}")
        
        # Create empty space for the fixed footer
        st.markdown("<div style='height: 80px;'></div>", unsafe_allow_html=True)
    
    # Render footer with export buttons
    render_footer(unique_id)

# Run the application
if __name__ == "__main__":
    main()