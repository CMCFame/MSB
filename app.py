# ============================================================================
# ARCOS SIG FORM - MAIN APPLICATION
# ============================================================================
import streamlit as st
import os
import base64
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
# ICON UTILITIES
# ============================================================================
def get_icon_path(icon_name):
    """Get the path to an icon file"""
    return os.path.join("static", "icons", icon_name)

def get_icon_html(icon_name, active=False):
    """Get the HTML for an icon, with optional active state"""
    if not os.path.exists(get_icon_path(icon_name)):
        # If the icon doesn't exist, return a placeholder
        return f'<span style="font-size: 24px;">📄</span>'
    
    # Read the image file
    with open(get_icon_path(icon_name), "rb") as f:
        icon_data = f.read()
    
    # Base64 encode the image data
    encoded_icon = base64.b64encode(icon_data).decode()
    
    # Create the HTML img tag with the base64 encoded image
    filter_style = "filter: brightness(10);" if active else "filter: brightness(0.4);"
    return f'<img src="data:image/png;base64,{encoded_icon}" style="width: 28px; height: 28px; {filter_style}">'

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
        
        # Define available tabs with icons
        tabs_with_icons = [
            {
                "name": "Location Hierarchy", 
                "icon": "map-location.png",
                "description": "Configure your 4-level location structure"
            },
            {
                "name": "Trouble Locations", 
                "icon": "map.png",
                "description": "Set up trouble locations and pronunciations"
            },
            {
                "name": "Job Classifications", 
                "icon": "document-add.png",
                "description": "Define job roles and IDs"
            },
            {
                "name": "Callout Reasons", 
                "icon": "alert.png",
                "description": "Configure callout reasons and verbiage"
            },
            {
                "name": "Event Types", 
                "icon": "calendar.png",
                "description": "Set up event types and exceptions"
            },
            {
                "name": "Callout Type Configuration", 
                "icon": "settings.png",
                "description": "Configure callout types and behaviors"
            },
            {
                "name": "Global Configuration Options", 
                "icon": "globe-settings.png",
                "description": "Global settings and options"
            },
            {
                "name": "Data and Interfaces", 
                "icon": "hierarchy.png",
                "description": "Configure data flows and integrations"
            },
            {
                "name": "Additions", 
                "icon": "plus.png",
                "description": "Additional configuration options"
            }
        ]
        
        # Get tab names for simpler access
        tab_names = [tab["name"] for tab in tabs_with_icons]
        
        # Calculate progress
        completed_tabs = sum(1 for tab in tab_names if any(key.startswith(tab.replace(" ", "_").lower()) for key in st.session_state.responses))
        progress = completed_tabs / len(tab_names)
        st.progress(progress)
        st.write(f"{int(progress * 100)}% complete")
        
        # Navigation section header
        st.write("Select section:")
        
        # Custom CSS for icon navigation
        st.markdown("""
        <style>
        /* Icon grid layout */
        .icon-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 10px;
            margin-bottom: 20px;
        }
        
        /* Individual icon box */
        .icon-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 10px 5px;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.2s ease;
            height: 80px;
            background-color: #f8f8f8;
            margin-bottom: 5px;
        }
        
        /* Active icon box */
        .icon-box.active {
            background-color: #e3051b;
            color: white;
            border-color: #e3051b;
        }
        
        /* Icon box on hover */
        .icon-box:hover:not(.active) {
            background-color: #f0f0f0;
            border-color: #ccc;
        }
        
        /* Icon image container */
        .icon-img {
            margin-bottom: 5px;
        }
        
        /* Icon text label */
        .icon-label {
            font-size: 10px;
            text-align: center;
            line-height: 1.2;
            max-width: 100%;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }
        
        /* Hide buttons when using icon navigation */
        div[data-testid="stHorizontalBlock"] div[data-testid="column"] button[kind] {
            display: none;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Create icon grid HTML
        selected_tab = st.session_state.current_tab
        
        icon_grid_html = '<div class="icon-grid">'
        
        for i, tab in enumerate(tabs_with_icons):
            is_active = tab["name"] == selected_tab
            active_class = "active" if is_active else ""
            
            # Get the icon HTML
            icon_html = get_icon_html(tab["icon"], is_active)
            
            # Create the icon box
            icon_grid_html += f"""
            <div class="icon-box {active_class}" title="{tab['description']}" onclick="document.getElementById('btn_tab_{i}').click()">
                <div class="icon-img">{icon_html}</div>
                <div class="icon-label">{tab['name']}</div>
            </div>
            """
        
        icon_grid_html += '</div>'
        
        # Display the icon grid
        st.markdown(icon_grid_html, unsafe_allow_html=True)
        
        # Create hidden buttons for each tab
        # These will be clicked by the JavaScript in the icon grid
        button_cols = st.columns(3)
        for i, tab in enumerate(tabs_with_icons):
            with button_cols[i % 3]:
                button_type = "primary" if tab["name"] == selected_tab else "secondary"
                if st.button(tab["name"], key=f"btn_tab_{i}", use_container_width=True, type=button_type):
                    st.session_state.current_tab = tab["name"]
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