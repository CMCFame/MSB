# ============================================================================
# FOOTER COMPONENT WITH EXPORT BUTTONS
# ============================================================================
import streamlit as st
from datetime import datetime
from utils.exports import (
    export_location_hierarchy_to_csv,
    export_location_hierarchy_to_excel,
    export_all_data_to_excel
)
from utils.ui_helpers import create_export_button_script

def render_footer(unique_id):
    """Render the footer with export buttons"""
    # Export buttons at the bottom of the page
    # We use st.markdown to create a fixed position footer for the export buttons
    st.markdown("""
    <div class="footer-container">
        <div class="export-container">
            <button id="btn-csv" class="small-export-btn">Export as CSV</button>
            <button id="btn-excel" class="small-export-btn">Export as Excel</button>
        </div>
    </div>
    """ + create_export_button_script(), unsafe_allow_html=True)
    
    # Hidden buttons that will be triggered by the custom buttons
    button_container = st.container()
    with button_container:
        # Set visibility to hidden
        st.markdown("""
        <style>
        #button-container {
            visibility: hidden;
            position: absolute;
        }
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            # CSV export
            if st.button("Export CSV", key=f"export_csv_{unique_id}", type="secondary", use_container_width=True, 
                        help="export_csv"):
                # Determine what to export based on current tab
                csv_data = ""
                if st.session_state.current_tab == "Location Hierarchy":
                    csv_data = export_location_hierarchy_to_csv()
                else:
                    # Default to location hierarchy export if tab isn't recognized
                    csv_data = export_location_hierarchy_to_csv()
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="Download CSV",
                    data=csv_data,
                    file_name=f"arcos_sig_{timestamp}.csv",
                    mime="text/csv",
                    key=f"download_csv_{timestamp}"
                )
        
        with col2:
            # Excel export
            if st.button("Export Excel", key=f"export_excel_{unique_id}", type="secondary", use_container_width=True,
                        help="export_excel"):
                excel_data = export_all_data_to_excel()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="Download Excel",
                    data=excel_data,
                    file_name=f"arcos_sig_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_excel_{timestamp}"
                )