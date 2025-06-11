# ============================================================================
# FOOTER COMPONENT WITH EXPORT BUTTONS - FIXED & SIMPLIFIED
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
    
    # Simple floating footer using CSS and Streamlit components
    st.markdown("""
    <style>
    .floating-export {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 1000;
        background: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        border: 2px solid #e3051b;
        min-width: 200px;
    }
    .floating-export h4 {
        margin: 0 0 10px 0;
        color: #e3051b;
        font-size: 14px;
        text-align: center;
    }
    </style>
    
    <div class="floating-export">
        <h4>📤 Quick Export</h4>
    </div>
    """, unsafe_allow_html=True)
    
    # Create a sidebar section for export buttons
    with st.sidebar:
        st.markdown("---")
        st.markdown("### 📤 Export Data")
        
        # Export buttons in sidebar
        if st.button("📄 Export CSV", key=f"sidebar_csv_{unique_id}", use_container_width=True):
            csv_data = export_all_data_to_csv()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            st.download_button(
                label="⬇️ Download CSV",
                data=csv_data,
                file_name=f"arcos_sig_complete_{timestamp}.csv",
                mime="text/csv",
                key=f"download_csv_sidebar_{timestamp}",
                use_container_width=True
            )
        
        if st.button("📊 Export Excel", key=f"sidebar_excel_{unique_id}", use_container_width=True):
            excel_data = export_all_data_to_excel()
            if excel_data:  # Only show download if export was successful
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="⬇️ Download Excel",
                    data=excel_data,
                    file_name=f"arcos_sig_complete_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key=f"download_excel_sidebar_{timestamp}",
                    use_container_width=True
                )