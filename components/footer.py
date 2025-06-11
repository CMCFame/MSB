# ============================================================================
# FOOTER COMPONENT WITH EXPORT BUTTONS - FIXED
# ============================================================================
import streamlit as st
from datetime import datetime
from utils.exports import (
    export_location_hierarchy_to_csv,
    export_location_hierarchy_to_excel,
    export_all_data_to_excel,
    export_all_data_to_csv
)

def render_footer(unique_id):
    """Render the footer with working export buttons"""
    
    # Create a container for the floating buttons
    st.markdown("""
    <style>
    .floating-footer {
        position: fixed;
        bottom: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 1000;
        background: white;
        padding: 10px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 1px solid #ddd;
    }
    .export-btn {
        background-color: #e3051b;
        color: white;
        border: none;
        padding: 8px 16px;
        margin: 0 5px;
        border-radius: 5px;
        cursor: pointer;
        font-size: 14px;
    }
    .export-btn:hover {
        background-color: #b30000;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Create the actual working buttons using Streamlit's session state
    button_container = st.container()
    with button_container:
        # Position the container at the bottom
        st.markdown('<div class="floating-footer">', unsafe_allow_html=True)
        
        export_cols = st.columns(2)
        
        with export_cols[0]:
            if st.button("📄 Export as CSV", key=f"floating_csv_{unique_id}", type="secondary"):
                csv_data = export_all_data_to_csv()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv_data,
                    file_name=f"arcos_sig_complete_{timestamp}.csv",
                    mime="text/csv",
                    key=f"download_csv_floating_{timestamp}"
                )
                st.success("CSV export ready for download!")
        
        with export_cols[1]:
            if st.button("📊 Export as Excel", key=f"floating_excel_{unique_id}", type="secondary"):
                excel_data = export_all_data_to_excel()
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_data,
                    file_name=f"arcos_sig_complete_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_excel_floating_{timestamp}"
                )
                st.success("Excel export ready for download!")
        
        st.markdown('</div>', unsafe_allow_html=True)