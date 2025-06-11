# ============================================================================
# DATA IMPORT MODULE - utils/data_import.py
# ============================================================================
import streamlit as st
import pandas as pd
import json
import io
from typing import Dict, Any
from datetime import datetime

def parse_excel_import(uploaded_file) -> Dict[str, Any]:
    """Parse uploaded Excel file and return session state data"""
    try:
        # Check if openpyxl is available
        try:
            import openpyxl
        except ImportError:
            st.error("❌ **Missing Dependency**: The `openpyxl` library is required to read Excel files.")
            st.info("📋 **Solutions:**")
            st.code("pip install openpyxl", language="bash")
            st.markdown("**Alternative:** Export as JSON format instead of Excel for now.")
            return {}
        
        # Read all sheets from the Excel file
        excel_data = pd.read_excel(uploaded_file, sheet_name=None, engine='openpyxl')
        
        session_data = {}
        
        # Parse Location Hierarchy
        if 'Location Hierarchy' in excel_data:
            df = excel_data['Location Hierarchy']
            entries = []
            for _, row in df.iterrows():
                # Handle codes properly - look for codes columns or list representation
                codes = ["", "", "", "", ""]
                for i in range(5):
                    code_val = row.get(f'codes[{i}]', row.get(f'code_{i}', ''))
                    if pd.notna(code_val):
                        codes[i] = str(code_val)
                
                # Handle callout_types properly
                callout_types = {
                    "Normal": bool(row.get('callout_types[Normal]', row.get('Normal', False))),
                    "All Hands on Deck": bool(row.get('callout_types[All Hands on Deck]', row.get('All Hands on Deck', False))),
                    "Fill Shift": bool(row.get('callout_types[Fill Shift]', row.get('Fill Shift', False))),
                    "Travel": bool(row.get('callout_types[Travel]', row.get('Travel', False))),
                    "Notification": bool(row.get('callout_types[Notification]', row.get('Notification', False))),
                    "Notification (No Response)": bool(row.get('callout_types[Notification (No Response)]', row.get('Notification (No Response)', False)))
                }
                
                entry = {
                    "level1": str(row.get('level1', '')) if pd.notna(row.get('level1')) else '',
                    "level2": str(row.get('level2', '')) if pd.notna(row.get('level2')) else '',
                    "level3": str(row.get('level3', '')) if pd.notna(row.get('level3')) else '',
                    "level4": str(row.get('level4', '')) if pd.notna(row.get('level4')) else '',
                    "timezone": str(row.get('timezone', '')) if pd.notna(row.get('timezone')) else '',
                    "codes": codes,
                    "callout_types": callout_types,
                    "callout_reasons": str(row.get('callout_reasons', '')) if pd.notna(row.get('callout_reasons')) else ''
                }
                entries.append(entry)
            
            session_data['hierarchy_data'] = {
                "levels": ["Level 1", "Level 2", "Level 3", "Level 4"],
                "labels": ["Parent Company", "Business Unit", "Division", "OpCenter"],
                "entries": entries,
                "timezone": "ET / CT / MT / AZ / PT"
            }
        
        # Parse Job Classifications
        if 'Job Classifications' in excel_data:
            df = excel_data['Job Classifications']
            job_classifications = []
            for _, row in df.iterrows():
                ids = ["", "", "", "", ""]
                for i in range(5):
                    id_val = row.get(f'ID_{i+1}', '')
                    if pd.notna(id_val):
                        ids[i] = str(id_val)
                
                job = {
                    "type": str(row.get('Type', '')) if pd.notna(row.get('Type')) else '',
                    "title": str(row.get('Title', '')) if pd.notna(row.get('Title')) else '',
                    "recording": str(row.get('Recording', '')) if pd.notna(row.get('Recording')) else '',
                    "ids": ids
                }
                job_classifications.append(job)
            session_data['job_classifications'] = job_classifications
        
        # Parse Trouble Locations
        if 'Trouble Locations' in excel_data:
            df = excel_data['Trouble Locations']
            trouble_locations = []
            for _, row in df.iterrows():
                location = {
                    "recording_needed": bool(row.get('recording_needed', True)),
                    "id": str(row.get('id', '')) if pd.notna(row.get('id')) else '',
                    "location": str(row.get('location', '')) if pd.notna(row.get('location')) else '',
                    "verbiage": str(row.get('verbiage', '')) if pd.notna(row.get('verbiage')) else ''
                }
                trouble_locations.append(location)
            session_data['trouble_locations'] = trouble_locations
        
        # Parse Event Types
        if 'Event Types' in excel_data:
            df = excel_data['Event Types']
            event_types = []
            for _, row in df.iterrows():
                event = {
                    "id": str(row.get('id', '')) if pd.notna(row.get('id')) else '',
                    "description": str(row.get('description', '')) if pd.notna(row.get('description')) else '',
                    "use": bool(row.get('use', False)),
                    "use_in_dropdown": bool(row.get('use_in_dropdown', False)),
                    "include_in_override": bool(row.get('include_in_override', False)),
                    "charged_or_excused": str(row.get('charged_or_excused', '')) if pd.notna(row.get('charged_or_excused')) else '',
                    "available_on_inbound": str(row.get('available_on_inbound', '')) if pd.notna(row.get('available_on_inbound')) else '',
                    "employee_on_exception": str(row.get('employee_on_exception', '')) if pd.notna(row.get('employee_on_exception')) else '',
                    "release_mobile": bool(row.get('release_mobile', False)),
                    "release_auto": bool(row.get('release_auto', False)),
                    "make_unavailable": bool(row.get('make_unavailable', False)),
                    "place_status": bool(row.get('place_status', False)),
                    "min_duration": str(row.get('min_duration', '')) if pd.notna(row.get('min_duration')) else '',
                    "max_duration": str(row.get('max_duration', '')) if pd.notna(row.get('max_duration')) else ''
                }
                event_types.append(event)
            session_data['event_types'] = event_types
        
        # Parse Callout Reasons
        if 'Callout Reasons' in excel_data:
            df = excel_data['Callout Reasons']
            selected_reasons = []
            default_reason = ""
            for _, row in df.iterrows():
                if str(row.get('Use?', '')).strip().lower() == 'x':
                    selected_reasons.append(str(row.get('ID', '')))
                if str(row.get('Default?', '')).strip().lower() == 'x':
                    default_reason = str(row.get('ID', ''))
            session_data['selected_callout_reasons'] = selected_reasons
            session_data['default_callout_reason'] = default_reason
        
        # Parse Callout Type Configuration
        if 'Callout Type Config' in excel_data:
            df = excel_data['Callout Type Config']
            responses = {}
            for _, row in df.iterrows():
                location = str(row.get('Location', ''))
                for col in df.columns:
                    if col.startswith('CT_'):
                        callout_type = col[3:]  # Remove 'CT_' prefix
                        key = f"matrix_{location}_{callout_type}".replace(" ", "_")
                        responses[key] = (str(row[col]).strip().upper() == 'X')
            if 'responses' not in session_data:
                session_data['responses'] = {}
            session_data['responses'].update(responses)
        
        # Parse Global Configuration
        if 'Global Configuration' in excel_data:
            df = excel_data['Global Configuration']
            global_config = {}
            for _, row in df.iterrows():
                key = str(row.get('Configuration_Key', ''))
                value = row.get('Value', '')
                # Try to convert value to appropriate type
                if pd.notna(value):
                    if str(value).lower() in ['true', 'false']:
                        value = str(value).lower() == 'true'
                    elif str(value).isdigit():
                        value = int(value)
                    else:
                        value = str(value)
                global_config[key] = value
            session_data['global_config_answers'] = global_config
        
        # Parse Data Interfaces
        if 'Data Interfaces' in excel_data:
            df = excel_data['Data Interfaces']
            data_interfaces = {}
            
            def unflatten_dict(flat_dict, sep='_'):
                """Convert flattened dictionary back to nested structure"""
                result = {}
                for key, value in flat_dict.items():
                    if pd.notna(value):
                        parts = key.split(sep)
                        d = result
                        for part in parts[:-1]:
                            if part not in d:
                                d[part] = {}
                            d = d[part]
                        d[parts[-1]] = str(value)
                return result
            
            flat_data = {}
            for _, row in df.iterrows():
                key = str(row.get('Interface_Setting', ''))
                value = row.get('Value', '')
                if pd.notna(value):
                    flat_data[key] = value
            
            session_data['data_interfaces'] = unflatten_dict(flat_data)
        
        # Parse Additions
        if 'Additions' in excel_data:
            df = excel_data['Additions']
            additions = {}
            
            def unflatten_dict(flat_dict, sep='_'):
                result = {}
                for key, value in flat_dict.items():
                    if pd.notna(value):
                        parts = key.split(sep)
                        d = result
                        for part in parts[:-1]:
                            if part not in d:
                                d[part] = {}
                            d = d[part]
                        d[parts[-1]] = str(value)
                return result
            
            flat_data = {}
            for _, row in df.iterrows():
                key = str(row.get('Addition_Setting', ''))
                value = row.get('Value', '')
                if pd.notna(value):
                    flat_data[key] = value
            
            session_data['additions'] = unflatten_dict(flat_data)
        
        # Parse Other Responses
        if 'Other Responses' in excel_data:
            df = excel_data['Other Responses']
            if 'responses' not in session_data:
                session_data['responses'] = {}
            for _, row in df.iterrows():
                key = str(row.get('Key', ''))
                value = row.get('Value', '')
                if pd.notna(value):
                    session_data['responses'][key] = str(value)
        
        return session_data
        
    except Exception as e:
        st.error(f"Error parsing Excel file: {str(e)}")
        import traceback
        st.text(traceback.format_exc())
        return {}

def parse_json_import(uploaded_file) -> Dict[str, Any]:
    """Parse uploaded JSON file and return session state data"""
    try:
        # Read JSON file
        json_data = json.load(uploaded_file)
        return json_data
    except Exception as e:
        st.error(f"Error parsing JSON file: {str(e)}")
        return {}

def load_session_data(session_data: Dict[str, Any]):
    """Load session data into Streamlit session state"""
    try:
        # Load each section into session state
        for key, value in session_data.items():
            st.session_state[key] = value
        
        st.success("✅ Data loaded successfully! All sections have been restored.")
        return True
    except Exception as e:
        st.error(f"Error loading session data: {str(e)}")
        return False

def export_session_to_json():
    """Export current session state to JSON for backup"""
    try:
        # Collect all relevant session state data
        export_data = {}
        
        keys_to_export = [
            'hierarchy_data', 'job_classifications', 'trouble_locations',
            'event_types', 'selected_callout_reasons', 'default_callout_reason',
            'responses', 'global_config_answers', 'data_interfaces', 'additions',
            'callout_types'
        ]
        
        for key in keys_to_export:
            if key in st.session_state:
                export_data[key] = st.session_state[key]
        
        # Convert to JSON string
        json_string = json.dumps(export_data, indent=2, default=str)
        return json_string
    except Exception as e:
        st.error(f"Error exporting session to JSON: {str(e)}")
        return ""

def render_import_export_section():
    """Render the import/export section in the main app"""
    st.markdown("### 📁 Data Import/Export")
    
    # Check available dependencies
    try:
        import openpyxl
        excel_available = True
    except ImportError:
        excel_available = False
    
    # Show dependency status
    if not excel_available:
        st.warning("⚠️ **Excel Import Unavailable**: Missing `openpyxl` dependency. JSON import/export is still available.")
        with st.expander("🔧 Fix Excel Import"):
            st.markdown("**To enable Excel import, install the missing dependency:**")
            st.code("pip install openpyxl", language="bash")
            st.markdown("**Or add to your requirements.txt:**")
            st.code("openpyxl>=3.0.0", language="text")
    
    # Create two columns for import and export
    import_col, export_col = st.columns(2)
    
    with import_col:
        st.markdown("#### 📤 Import Data")
        st.info("Upload a previously exported file to resume your work")
        
        # Adjust file types based on available dependencies
        allowed_types = ['json']
        help_text = "Upload a JSON file exported from this application"
        
        if excel_available:
            allowed_types.append('xlsx')
            help_text = "Upload an Excel file or JSON file exported from this application"
        
        uploaded_file = st.file_uploader(
            "Choose a file to import",
            type=allowed_types,
            help=help_text
        )
        
        if uploaded_file is not None:
            st.write(f"📄 Selected file: {uploaded_file.name}")
            
            # Show warning if trying to upload Excel without openpyxl
            if uploaded_file.name.endswith('.xlsx') and not excel_available:
                st.error("❌ Cannot process Excel files. Please use JSON format or install `openpyxl`.")
                return
            
            if st.button("🔄 Load Data", type="primary"):
                with st.spinner("Loading data..."):
                    if uploaded_file.name.endswith('.xlsx'):
                        session_data = parse_excel_import(uploaded_file)
                    elif uploaded_file.name.endswith('.json'):
                        session_data = parse_json_import(uploaded_file)
                    else:
                        st.error("Unsupported file format")
                        return
                    
                    if session_data:
                        success = load_session_data(session_data)
                        if success:
                            st.rerun()
    
    with export_col:
        st.markdown("#### 💾 Export Data")
        st.info("Save your current progress for later")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Show Excel export status
            excel_btn_disabled = not excel_available
            excel_btn_help = "Excel export requires openpyxl" if not excel_available else "Export all data to Excel with multiple sheets"
            
            if st.button("📊 Export Excel", type="secondary", disabled=excel_btn_disabled, help=excel_btn_help):
                if excel_available:
                    from utils.exports import export_all_data_to_excel
                    excel_data = export_all_data_to_excel()
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="⬇️ Download Excel",
                        data=excel_data,
                        file_name=f"arcos_sig_backup_{timestamp}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        key=f"export_excel_backup_{timestamp}"
                    )
        
        with col2:
            if st.button("📄 Export JSON", type="secondary", help="Export all data to JSON format (recommended)"):
                json_data = export_session_to_json()
                if json_data:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    st.download_button(
                        label="⬇️ Download JSON",
                        data=json_data,
                        file_name=f"arcos_sig_backup_{timestamp}.json",
                        mime="application/json",
                        key=f"export_json_backup_{timestamp}"
                    )
        
        # Recommend JSON format if Excel is unavailable
        if not excel_available:
            st.info("💡 **Tip**: Use JSON format for reliable import/export without additional dependencies.")