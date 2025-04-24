# ============================================================================
# EXPORT FUNCTIONS
# ============================================================================
import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime

def get_csv_data(df: pd.DataFrame) -> str:
    """
    Return the CSV data (as a string) for a given DataFrame.
    """
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    return csv_buffer.getvalue()

def get_excel_data(df: pd.DataFrame) -> bytes:
    """
    Return the Excel data (as bytes) for a given DataFrame.
    """
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
        # Create a flattened version of the job classifications data
        data = []
        for job in st.session_state.job_classifications:
            row = {
                "Type": job["type"],
                "Title": job["title"],
                "Recording": job["recording"]
            }
            # Add IDs as separate columns
            for i, id_val in enumerate(job["ids"]):
                row[f"ID_{i+1}"] = id_val
            data.append(row)
        
        df_export = pd.DataFrame(data)
        return get_csv_data(df_export)
    return ""

def export_job_classifications_to_excel():
    """Export job classifications data to Excel"""
    if 'job_classifications' in st.session_state:
        # Create a flattened version of the job classifications data
        data = []
        for job in st.session_state.job_classifications:
            row = {
                "Type": job["type"],
                "Title": job["title"],
                "Recording": job["recording"]
            }
            # Add IDs as separate columns
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

def export_all_data_to_excel():
    """Export all configuration data to a single Excel file with multiple sheets"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        # Export location hierarchy
        if 'hierarchy_data' in st.session_state:
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
        if 'trouble_locations' in st.session_state:
            trouble_df = pd.DataFrame(st.session_state.trouble_locations)
            trouble_df.to_excel(writer, sheet_name='Trouble Locations', index=False)
        
        # Export event types
        if 'event_types' in st.session_state:
            events_df = pd.DataFrame(st.session_state.event_types)
            events_df.to_excel(writer, sheet_name='Event Types', index=False)
        
        # Export responses (generic form data)
        if 'responses' in st.session_state and st.session_state.responses:
            responses_data = [{"Key": k, "Value": v} for k, v in st.session_state.responses.items()]
            responses_df = pd.DataFrame(responses_data)
            responses_df.to_excel(writer, sheet_name='Other Responses', index=False)
    
    output.seek(0)
    return output.getvalue()