# ============================================================================
# JOB CLASSIFICATIONS TAB
# ============================================================================
import streamlit as st
import pandas as pd
from config.constants import DEFAULT_JOB_CLASSIFICATION

def render_job_classifications():
    """Render the Job Classifications form with interactive elements"""
    st.markdown('<p class="tab-header">Job Classifications</p>', unsafe_allow_html=True)
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab is used to list the Job Classifications (job titles) of the employees that will be in the ARCOS database.
        
        List the Job Classifications (job titles) of the employees and assign each a unique ID (typically taken from your HR system).
        If you have more than one ID for a Job Class, you can separate up to 5 in different columns.
        
        If applicable, indicate Journeyman and Apprentice classes. If your company requires the option to have a duty position or classification spoken to employees
        when being called out, please indicate the verbiage.
        """)
    
    # Initialize the job classifications if not already in session state
    if 'job_classifications' not in st.session_state:
        st.session_state.job_classifications = [DEFAULT_JOB_CLASSIFICATION]
    
    # Add new job classification button
    if st.button("➕ Add Job Classification"):
        st.session_state.job_classifications.append(DEFAULT_JOB_CLASSIFICATION.copy())
        st.rerun()
    
    # Display and edit job classifications - avoiding nested columns
    for i, job in enumerate(st.session_state.job_classifications):
        st.markdown(f"<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<p><b>Job Classification #{i+1}</b></p>", unsafe_allow_html=True)
        
        # Type and title in separate container
        type_title_container = st.container()
        with type_title_container:
            type_title_cols = st.columns([2, 3])
            with type_title_cols[0]:
                job["type"] = st.selectbox(
                    "Type", 
                    ["", "Journeyman", "Apprentice"], 
                    index=["", "Journeyman", "Apprentice"].index(job["type"]) if job["type"] in ["", "Journeyman", "Apprentice"] else 0,
                    key=f"job_type_{i}"
                )
            with type_title_cols[1]:
                job["title"] = st.text_input("Job Classification Title", value=job["title"], key=f"job_title_{i}")
        
        # IDs in separate container
        st.markdown("<p><b>Job Classification IDs</b> (up to 5)</p>", unsafe_allow_html=True)
        ids_container = st.container()
        with ids_container:
            id_cols = st.columns(5)
            for j in range(5):
                with id_cols[j]:
                    # Ensure we have enough id slots
                    while len(job["ids"]) <= j:
                        job["ids"].append("")
                    job["ids"][j] = st.text_input(f"ID {j+1}", value=job["ids"][j], key=f"job_id_{i}_{j}")
        
        # Recording in separate container
        recording_container = st.container()
        with recording_container:
            job["recording"] = st.text_input(
                "Recording Verbiage (what should be spoken during callout)", 
                value=job["recording"], 
                key=f"job_rec_{i}",
                help="Leave blank if same as Job Title"
            )
        
        # Delete button in separate container
        delete_container = st.container()
        with delete_container:
            if st.button("🗑️ Remove", key=f"del_job_{i}"):
                st.session_state.job_classifications.pop(i)
                st.rerun()
    
    # Preview in separate container
    preview_container = st.container()
    with preview_container:
        st.markdown('<p class="section-header">Classifications Preview</p>', unsafe_allow_html=True)
        
        if st.session_state.job_classifications:
            # Create display data
            job_data = []
            for job in st.session_state.job_classifications:
                if job["title"]:  # Only include jobs with titles
                    job_data.append({
                        "Type": job["type"],
                        "Title": job["title"],
                        "IDs": ", ".join([id for id in job["ids"] if id]),
                        "Recording": job["recording"] if job["recording"] else "(Same as title)"
                    })
            
            if job_data:
                job_df = pd.DataFrame(job_data)
                st.dataframe(job_df, use_container_width=True)
            else:
                st.info("Add job classifications to see the preview.")
        else:
            st.info("No job classifications added yet.")