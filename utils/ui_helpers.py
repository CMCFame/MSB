# ============================================================================
# UI HELPER FUNCTIONS
# ============================================================================
import streamlit as st
from config.constants import CUSTOM_CSS

def render_css():
    """Render the custom CSS for the application"""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
        st.markdown("""
        <style>
        button[kind="secondary"] {
            padding-top: 8px !important;
            padding-bottom: 8px !important;
            font-size: 12px !important;
            min-height: 32px !important;
        }
        </style>
    """, unsafe_allow_html=True)

def render_color_key():
    """Render the color key header similar to the Excel file"""
    st.markdown("""
    <div style="margin-bottom: 15px; border: 1px solid #ddd; padding: 10px;">
        <h3>Color Key</h3>
        <div style="display: flex; flex-wrap: wrap; gap: 5px;">
            <div class="color-key-box" style="background-color: #ffcccc;">Delete</div>
            <div class="color-key-box" style="background-color: #99cc99;">Changes</div>
            <div class="color-key-box" style="background-color: #6699ff;">Moves</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_export_button_script():
    """Create JavaScript for custom export buttons"""
    return """
    <script>
        // Add click handlers for the custom buttons
        document.getElementById('btn-csv').addEventListener('click', function() {
            // Find the hidden Streamlit button and click it
            document.querySelector('[data-testid="stButton"] button[kind="secondary"][aria-label="export_csv"]').click();
        });
        
        document.getElementById('btn-excel').addEventListener('click', function() {
            // Find the hidden Streamlit button and click it
            document.querySelector('[data-testid="stButton"] button[kind="secondary"][aria-label="export_excel"]').click();
        });
    </script>
    """

def local_css(css_string):
    """Apply custom CSS styles within a specific section"""
    st.markdown(f"<style>{css_string}</style>", unsafe_allow_html=True)

def make_grid(columns, rows):
    """Create a grid of elements using st.columns and return a list of cells"""
    grid = [st.columns(columns) for _ in range(rows)]
    cells = [cell for row in grid for cell in row]
    return cells

def create_table_header(columns, widths):
    """Create a table header using HTML/CSS"""
    header_html = '<div style="display: flex; margin-bottom: 10px; font-weight: bold;">'
    
    for i, col in enumerate(columns):
        width = widths[i] if i < len(widths) else 1
        header_html += f'<div style="flex: {width};">{col}</div>'
    
    header_html += '</div>'
    
    return st.markdown(header_html, unsafe_allow_html=True)

def create_empty_space(height=10):
    """Create empty vertical space"""
    st.markdown(f"<div style='height: {height}px;'></div>", unsafe_allow_html=True)

def create_horizontal_rule():
    """Create a horizontal rule (separator line)"""
    st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)

def show_info_box(message):
    """Display an information box with custom styling"""
    st.markdown(f"<div class='info-box'>{message}</div>", unsafe_allow_html=True)

def show_success_message(message):
    """Display a success message with custom styling"""
    st.markdown(f"<div style='background-color: {ARCOS_GREEN}; padding: 10px; border-radius: 5px;'>{message}</div>", unsafe_allow_html=True)

def show_warning_message(message):
    """Display a warning message with custom styling"""
    st.markdown(f"<div style='background-color: {ARCOS_LIGHT_RED}; padding: 10px; border-radius: 5px;'>{message}</div>", unsafe_allow_html=True)
    
def render_icon_tabs(tabs, tab_icons):
    """Render compact Streamlit-native icon tabs"""
    current_tab = st.session_state.get("current_tab", tabs[0])
    cols = st.columns(len(tabs))

    for i, tab in enumerate(tabs):
        label = f"{tab_icons.get(tab, '')} {tab}"
        if cols[i].button(label, use_container_width=True):
            st.session_state.current_tab = tab
            st.rerun()
