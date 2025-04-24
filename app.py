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
        
        # Define available tabs
        tabs = [
            "Location Hierarchy",
            "Trouble Locations",
            "Job Classifications",
            "Callout Reasons",
            "Event Types",
            "Callout Type Configuration",
            "Global Configuration Options",
            "Data and Interfaces",
            "Additions"
        ]
        
        # Calculate progress
        completed_tabs = sum(1 for tab in tabs if any(key.startswith(tab.replace(" ", "_").lower()) for key in st.session_state.responses))
        progress = completed_tabs / len(tabs)
        st.progress(progress)
        st.write(f"{int(progress * 100)}% complete")
        
        # Custom CSS for more compact buttons
        st.markdown("""
        <style>
        /* Make buttons smaller and more visually appealing */
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind="secondary"] {
            background-color: #f8f9fa !important;
            color: #333 !important;
            border: 1px solid #ddd !important;
            border-radius: 8px !important;
            font-size: 13px !important;
            padding: 10px 4px !important;
            min-height: 40px !important;
            height: auto !important;
            transition: all 0.2s ease;
            line-height: 1.2;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind="secondary"]:hover {
            background-color: #e9ecef !important;
            border-color: #ced4da !important;
        }
        
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind="primary"] {
            background-color: #e3051b !important;
            color: white !important;
            border: 1px solid #e3051b !important;
            border-radius: 8px !important;
            font-size: 13px !important;
            padding: 10px 4px !important;
            min-height: 40px !important;
            height: auto !important;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Navigation section header
        st.write("Select section:")
        
        # The current tab
        selected_tab = st.session_state.current_tab
        
        # Create 3 rows of 3 buttons each for the navigation
        # Row 1
        col1, col2, col3 = st.columns(3)
        with col1:
            button_type = "primary" if tabs[0] == selected_tab else "secondary"
            if st.button(tabs[0], key=f"tab_0_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[0]
                st.rerun()
        
        with col2:
            button_type = "primary" if tabs[1] == selected_tab else "secondary"
            if st.button(tabs[1], key=f"tab_1_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[1]
                st.rerun()
                
        with col3:
            button_type = "primary" if tabs[2] == selected_tab else "secondary"
            if st.button(tabs[2], key=f"tab_2_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[2]
                st.rerun()
        
        # Row 2
        col1, col2, col3 = st.columns(3)
        with col1:
            button_type = "primary" if tabs[3] == selected_tab else "secondary"
            if st.button(tabs[3], key=f"tab_3_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[3]
                st.rerun()
                
        with col2:
            button_type = "primary" if tabs[4] == selected_tab else "secondary"
            if st.button(tabs[4], key=f"tab_4_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[4]
                st.rerun()
                
        with col3:
            button_type = "primary" if tabs[5] == selected_tab else "secondary"
            if st.button(tabs[5], key=f"tab_5_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[5]
                st.rerun()
        
        # Row 3
        col1, col2, col3 = st.columns(3)
        with col1:
            button_type = "primary" if tabs[6] == selected_tab else "secondary"
            if st.button(tabs[6], key=f"tab_6_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[6]
                st.rerun()
                
        with col2:
            button_type = "primary" if tabs[7] == selected_tab else "secondary"
            if st.button(tabs[7], key=f"tab_7_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[7]
                st.rerun()
                
        with col3:
            button_type = "primary" if tabs[8] == selected_tab else "secondary"
            if st.button(tabs[8], key=f"tab_8_{unique_id}", use_container_width=True, type=button_type):
                st.session_state.current_tab = tabs[8]
                st.rerun()
                
        # Add a separator between navigation and content
        st.markdown("<hr style='margin: 12px 0;'>", unsafe_allow_html=True)
        
        # Main content area - render the appropriate tab
        content_container = st.container()
        with content_container:
            try:
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