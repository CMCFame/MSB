# ============================================================================
# ENHANCED EXPORT FUNCTIONS - INCLUDES ALL SECTIONS
# ============================================================================
import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime

def get_csv_data(df: pd.DataFrame) -> str:
    """Return the CSV data (as a string) for a given DataFrame."""
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def get_excel_data(df: pd.DataFrame) -> bytes:
    """Return the Excel data (as bytes) for a given DataFrame."""
    excel_buffer = io.BytesIO()
    df.to_excel(excel_buffer, index=False, engine='xlsxwriter')
    excel_buffer.seek(0)
    return excel_buffer.read()

def export_location_hierarchy_to_csv():
    """Export location hierarchy data to CSV"""
    if 'hierarchy_data' in st.session_state:
        df_export = pd.DataFrame(st.session_state.hierarchy_data["entries"])
        return get_csv_data(df_export)
    return ""

def export_location_hierarchy_to_excel():
    """Export location hierarchy data to Excel"""
    if 'hierarchy_data' in st.session_state:
        df_export = pd.DataFrame(st.session_state.hierarchy_data["entries"])
        return get_excel_data(df_export)
    return b""

def export_job_classifications_to_csv():
    """Export job classifications data to CSV"""
    if 'job_classifications' in st.session_state:
        data = []
        for job in st.session_state.job_classifications:
            row = {
                "Type": job["type"],
                "Title": job["title"],
                "Recording": job["recording"]
            }
            for i, id_val in enumerate(job["ids"]):
                row[f"ID_{i+1}"] = id_val
            data.append(row)
        
        df_export = pd.DataFrame(data)
        return get_csv_data(df_export)
    return ""

def export_job_classifications_to_excel():
    """Export job classifications data to Excel"""
    if 'job_classifications' in st.session_state:
        data = []
        for job in st.session_state.job_classifications:
            row = {
                "Type": job["type"],
                "Title": job["title"],
                "Recording": job["recording"]
            }
            for i, id_val in enumerate(job["ids"]):
                row[f"ID_{i+1}"] = id_val
            data.append(row)
        
        df_export = pd.DataFrame(data)
        return get_excel_data(df_export)
    return b""

def export_trouble_locations_to_csv():
    """Export trouble locations data to CSV"""
    if 'trouble_locations' in st.session_state:
        df_export = pd.DataFrame(st.session_state.trouble_locations)
        return get_csv_data(df_export)
    return ""

def export_trouble_locations_to_excel():
    """Export trouble locations data to Excel"""
    if 'trouble_locations' in st.session_state:
        df_export = pd.DataFrame(st.session_state.trouble_locations)
        return get_excel_data(df_export)
    return b""

def export_event_types_to_csv():
    """Export event types data to CSV"""
    if 'event_types' in st.session_state:
        df_export = pd.DataFrame(st.session_state.event_types)
        return get_csv_data(df_export)
    return ""

def export_event_types_to_excel():
    """Export event types data to Excel"""
    if 'event_types' in st.session_state:
        df_export = pd.DataFrame(st.session_state.event_types)
        return get_excel_data(df_export)
    return b""

def export_callout_reasons_to_csv():
    """Export callout reasons data to CSV"""
    if 'selected_callout_reasons' in st.session_state:
        # Get the actual callout reasons data
        from utils.session import load_callout_reasons
        try:
            callout_reasons = load_callout_reasons()
            selected_reasons = [r for r in callout_reasons if r["ID"] in st.session_state.selected_callout_reasons]
            df_export = pd.DataFrame(selected_reasons)
            return get_csv_data(df_export)
        except:
            pass
    return ""

def export_callout_reasons_to_excel():
    """Export callout reasons data to Excel"""
    if 'selected_callout_reasons' in st.session_state:
        from utils.session import load_callout_reasons
        try:
            callout_reasons = load_callout_reasons()
            selected_reasons = [r for r in callout_reasons if r["ID"] in st.session_state.selected_callout_reasons]
            df_export = pd.DataFrame(selected_reasons)
            return get_excel_data(df_export)
        except:
            pass
    return b""

def export_callout_type_configuration_to_csv():
    """Export callout type configuration (matrix) data to CSV"""
    data = []
    if 'hierarchy_data' in st.session_state and 'responses' in st.session_state:
        for entry in st.session_state.hierarchy_data["entries"]:
            if entry["level4"]:
                row = {
                    "Location": entry["level4"],
                    "Full_Path": f"{entry.get('level1', '')} > {entry.get('level2', '')} > {entry.get('level3', '')} > {entry['level4']}"
                }
                
                # Add callout types
                if 'callout_types' in st.session_state:
                    for ct in st.session_state.callout_types:
                        key = f"matrix_{entry['level4']}_{ct}".replace(" ", "_")
                        row[f"CT_{ct}"] = "X" if st.session_state.responses.get(key, False) else ""
                
                data.append(row)
    
    if data:
        df_export = pd.DataFrame(data)
        return get_csv_data(df_export)
    return ""

def export_global_configuration_to_csv():
    """Export global configuration data to CSV"""
    if 'global_config_answers' in st.session_state:
        data = []
        for key, value in st.session_state.global_config_answers.items():
            data.append({
                "Configuration_Key": key,
                "Value": str(value)
            })
        
        if data:
            df_export = pd.DataFrame(data)
            return get_csv_data(df_export)
    return ""

def export_data_interfaces_to_csv():
    """Export data and interfaces data to CSV"""
    if 'data_interfaces' in st.session_state:
        data = []
        
        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, ', '.join(map(str, v))))
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat_data = flatten_dict(st.session_state.data_interfaces)
        for key, value in flat_data.items():
            data.append({
                "Interface_Setting": key,
                "Value": str(value)
            })
        
        if data:
            df_export = pd.DataFrame(data)
            return get_csv_data(df_export)
    return ""

def export_additions_to_csv():
    """Export additions data to CSV"""
    if 'additions' in st.session_state:
        data = []
        
        def flatten_dict(d, parent_key='', sep='_'):
            items = []
            for k, v in d.items():
                new_key = f"{parent_key}{sep}{k}" if parent_key else k
                if isinstance(v, dict):
                    items.extend(flatten_dict(v, new_key, sep=sep).items())
                elif isinstance(v, list):
                    items.append((new_key, ', '.join(map(str, v))))
                else:
                    items.append((new_key, v))
            return dict(items)
        
        flat_data = flatten_dict(st.session_state.additions)
        for key, value in flat_data.items():
            data.append({
                "Addition_Setting": key,
                "Value": str(value)
            })
        
        if data:
            df_export = pd.DataFrame(data)
            return get_csv_data(df_export)
    return ""

def export_all_data_to_csv():
    """Export all configuration data to a single CSV file"""
    all_sections = []
    
    # Section 1: Location Hierarchy
    if 'hierarchy_data' in st.session_state and st.session_state.hierarchy_data["entries"]:
        locations_df = pd.DataFrame(st.session_state.hierarchy_data["entries"])
        locations_df['Section'] = 'Location Hierarchy'
        all_sections.append(locations_df)
    
    # Section 2: Job Classifications
    if 'job_classifications' in st.session_state:
        jobs_data = []
        for job in st.session_state.job_classifications:
            row = {
                "Section": "Job Classifications",
                "Type": job["type"],
                "Title": job["title"],
                "Recording": job["recording"]
            }
            for i, id_val in enumerate(job["ids"]):
                row[f"ID_{i+1}"] = id_val
            jobs_data.append(row)
        
        if jobs_data:
            jobs_df = pd.DataFrame(jobs_data)
            all_sections.append(jobs_df)
    
    # Continue with other sections...
    if all_sections:
        combined_df = pd.concat(all_sections, ignore_index=True, sort=False)
        return get_csv_data(combined_df)
    
    return ""

def export_all_data_to_excel():
    """Export all configuration data to a single Excel file with multiple sheets"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Export location hierarchy
        if 'hierarchy_data' in st.session_state and st.session_state.hierarchy_data["entries"]:
            locations_df = pd.DataFrame(st.session_state.hierarchy_data["entries"])
            locations_df.to_excel(writer, sheet_name='Location Hierarchy', index=False)
        
        # Export job classifications
        if 'job_classifications' in st.session_state:
            jobs_data = []
            for job in st.session_state.job_classifications:
                row = {
                    "Type": job["type"],
                    "Title": job["title"],
                    "Recording": job["recording"]
                }
                for i, id_val in enumerate(job["ids"]):
                    row[f"ID_{i+1}"] = id_val
                jobs_data.append(row)
            
            if jobs_data:
                jobs_df = pd.DataFrame(jobs_data)
                jobs_df.to_excel(writer, sheet_name='Job Classifications', index=False)
        
        # Export trouble locations
        if 'trouble_locations' in st.session_state and st.session_state.trouble_locations:
            trouble_df = pd.DataFrame(st.session_state.trouble_locations)
            trouble_df.to_excel(writer, sheet_name='Trouble Locations', index=False)
        
        # Export event types
        if 'event_types' in st.session_state and st.session_state.event_types:
            events_df = pd.DataFrame(st.session_state.event_types)
            events_df.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Export callout reasons
        if 'selected_callout_reasons' in st.session_state:
            from utils.session import load_callout_reasons
            try:
                callout_reasons = load_callout_reasons()
                selected_reasons = [r for r in callout_reasons if r["ID"] in st.session_state.selected_callout_reasons]
                if selected_reasons:
                    reasons_df = pd.DataFrame(selected_reasons)
                    reasons_df.to_excel(writer, sheet_name='Callout Reasons', index=False)
            except:
                pass
        
        # Export callout type configuration (matrix)
        matrix_data = []
        if 'hierarchy_data' in st.session_state and 'responses' in st.session_state:
            for entry in st.session_state.hierarchy_data["entries"]:
                if entry["level4"]:
                    row = {
                        "Location": entry["level4"],
                        "Full_Path": f"{entry.get('level1', '')} > {entry.get('level2', '')} > {entry.get('level3', '')} > {entry['level4']}"
                    }
                    
                    # Add callout types
                    if 'callout_types' in st.session_state:
                        for ct in st.session_state.callout_types:
                            key = f"matrix_{entry['level4']}_{ct}".replace(" ", "_")
                            row[f"CT_{ct}"] = "X" if st.session_state.responses.get(key, False) else ""
                    
                    matrix_data.append(row)
        
        if matrix_data:
            matrix_df = pd.DataFrame(matrix_data)
            matrix_df.to_excel(writer, sheet_name='Callout Type Config', index=False)
        
        # Export global configuration
        if 'global_config_answers' in st.session_state and st.session_state.global_config_answers:
            config_data = []
            for key, value in st.session_state.global_config_answers.items():
                config_data.append({
                    "Configuration_Key": key,
                    "Value": str(value)
                })
            
            if config_data:
                config_df = pd.DataFrame(config_data)
                config_df.to_excel(writer, sheet_name='Global Configuration', index=False)
        
        # Export data interfaces
        if 'data_interfaces' in st.session_state:
            def flatten_dict(d, parent_key='', sep='_'):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    elif isinstance(v, list):
                        items.append((new_key, ', '.join(map(str, v))))
                    else:
                        items.append((new_key, v))
                return dict(items)
            
            flat_data = flatten_dict(st.session_state.data_interfaces)
            interface_data = []
            for key, value in flat_data.items():
                interface_data.append({
                    "Interface_Setting": key,
                    "Value": str(value)
                })
            
            if interface_data:
                interface_df = pd.DataFrame(interface_data)
                interface_df.to_excel(writer, sheet_name='Data Interfaces', index=False)
        
        # Export additions
        if 'additions' in st.session_state:
            def flatten_dict(d, parent_key='', sep='_'):
                items = []
                for k, v in d.items():
                    new_key = f"{parent_key}{sep}{k}" if parent_key else k
                    if isinstance(v, dict):
                        items.extend(flatten_dict(v, new_key, sep=sep).items())
                    elif isinstance(v, list):
                        items.append((new_key, ', '.join(map(str, v))))
                    else:
                        items.append((new_key, v))
                return dict(items)
            
            flat_data = flatten_dict(st.session_state.additions)
            additions_data = []
            for key, value in flat_data.items():
                additions_data.append({
                    "Addition_Setting": key,
                    "Value": str(value)
                })
            
            if additions_data:
                additions_df = pd.DataFrame(additions_data)
                additions_df.to_excel(writer, sheet_name='Additions', index=False)
        
        # Export generic responses (other form data)
        if 'responses' in st.session_state and st.session_state.responses:
            responses_data = [{"Key": k, "Value": v} for k, v in st.session_state.responses.items()]
            responses_df = pd.DataFrame(responses_data)
            responses_df.to_excel(writer, sheet_name='Other Responses', index=False)
    
    output.seek(0)
    return output.getvalue()