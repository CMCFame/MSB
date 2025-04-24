# ============================================================================
# MATRIX OF LOCATIONS AND CALLOUT TYPES TAB
# ============================================================================
import streamlit as st
import pandas as pd
from utils.ai_assistant import get_openai_response, save_chat_history

def render_matrix_locations_callout_types():
    """Render the Matrix of Locations and Callout Types with interactive elements"""
    st.markdown('<p class="tab-header">Matrix of Locations and CO Types</p>', unsafe_allow_html=True)
    
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        This tab allows you to define the specific Callout Types available within a given location in ARCOS.
        
        The matrix allows you to place an "X" in the appropriate cells to indicate which Callout Types are available for each location. If your company desires to have all Callout Types available to all locations, this tab can be skipped.
        """)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Manage callout types
        st.markdown('<p class="section-header">Manage Callout Types</p>', unsafe_allow_html=True)
        
        # Current callout types
        st.write("Current Callout Types:")
        
        # Display current callout types in rows of 3
        callout_types = st.session_state.callout_types
        
        # Calculate how many rows we need
        num_items = len(callout_types)
        items_per_row = 3
        num_rows = (num_items + items_per_row - 1) // items_per_row  # Ceiling division
        
        # Create each row separately
        for row in range(num_rows):
            # Create columns for this row
            row_cols = st.columns(items_per_row)
            
            # Fill columns with items
            for col in range(items_per_row):
                idx = row * items_per_row + col
                
                # Check if we have an item for this position
                if idx < num_items:
                    with row_cols[col]:
                        callout_type = callout_types[idx]
                        st.write(f"🔹 {callout_type}")
                        if st.button("Remove", key=f"rm_co_{idx}", help=f"Remove {callout_type}"):
                            st.session_state.callout_types.pop(idx)
                            st.rerun()
        
        # Add new callout type - in a separate row
        st.markdown('<p class="section-header">Add New Callout Type</p>', unsafe_allow_html=True)
        add_cols = st.columns([3, 1])
        with add_cols[0]:
            new_callout = st.text_input("New Callout Type Name", key="new_callout")
        with add_cols[1]:
            if st.button("Add"):
                if new_callout and new_callout not in st.session_state.callout_types:
                    st.session_state.callout_types.append(new_callout)
                    st.rerun()
        
        # Matrix configuration
        st.markdown('<p class="section-header">Callout Types by Location Matrix</p>', unsafe_allow_html=True)
        
        # Create a DataFrame to represent the matrix with full hierarchy path
        matrix_data = create_matrix_data()
        
        if matrix_data:
            # Display each location in its own section
            for i, row in enumerate(matrix_data):
                location = row["Location"]
                st.write(f"**{row['Display']}**")
                
                # Calculate number of columns and rows needed for checkboxes
                num_callout_types = len(st.session_state.callout_types)
                max_cols_per_row = 4  # Maximum 4 checkboxes per row
                num_checkbox_rows = (num_callout_types + max_cols_per_row - 1) // max_cols_per_row
                
                # Create rows of checkboxes
                for row_idx in range(num_checkbox_rows):
                    # Create columns for this row
                    check_cols = st.columns(max_cols_per_row)
                    
                    # Fill columns with checkboxes
                    for col_idx in range(max_cols_per_row):
                        ct_idx = row_idx * max_cols_per_row + col_idx
                        
                        # Check if we still have callout types
                        if ct_idx < num_callout_types:
                            with check_cols[col_idx]:
                                ct = st.session_state.callout_types[ct_idx]
                                # Create a unique key for each checkbox that includes the location index and callout type index
                                checkbox_key = f"matrix_{i}_{location}_{ct_idx}_{ct}".replace(" ", "_")
                                
                                # Store the actual response key (which we'll still use for data storage)
                                response_key = f"matrix_{location}_{ct}".replace(" ", "_")
                                
                                # Use the checkbox with unique key, but store in the original response key
                                st.session_state.responses[response_key] = st.checkbox(
                                    ct, 
                                    value=row.get(ct, False), 
                                    key=checkbox_key  # Using the unique key here
                                )
                
                st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        else:
            st.warning("Add Level 4 locations in the Location Hierarchy tab first to configure this matrix.")
    
    with col2:
        # Preview matrix as a table
        st.markdown('<p class="section-header">Matrix Preview</p>', unsafe_allow_html=True)
        
        preview_data = create_preview_data(matrix_data)
        
        if preview_data:
            # Create dataframe and display it
            preview_df = pd.DataFrame(preview_data)
            # Limit the column width of the location column to prevent very wide tables
            st.dataframe(preview_df, use_container_width=True)
        else:
            st.info("Add locations to see the matrix preview.")
        
        # Help section
        st.markdown('<p class="section-header">Need Help?</p>', unsafe_allow_html=True)
        help_topic = st.selectbox(
            "Select topic for help",
            ["Callout Types", "Matrix Configuration", "Best Practices for Callout Types"]
        )
        
        if st.button("Get Help"):
            help_query = f"Explain in detail what I need to know about {help_topic} when configuring the Matrix of Locations and Callout Types in ARCOS. Include examples and best practices."
            with st.spinner("Loading help..."):
                help_response = get_openai_response(help_query)
                save_chat_history(f"Help with {help_topic}", help_response)
            
            st.info(help_response)
                
def create_matrix_data():
    """Create a DataFrame to represent the matrix with full hierarchy path"""
    matrix_data = []
    
    # Add entries from location hierarchy
    for entry in st.session_state.hierarchy_data["entries"]:
        if entry["level4"]:  # Only Level 4 locations need callout type assignments
            # Create full hierarchical path for display
            hierarchy_path = []
            if entry["level1"]:
                hierarchy_path.append(entry["level1"])
            if entry["level2"]:
                hierarchy_path.append(entry["level2"])
            if entry["level3"]:
                hierarchy_path.append(entry["level3"])
            
            # Format the path for display
            path_str = " > ".join(hierarchy_path)
            location_display = f"{entry['level4']} ({path_str})"
            
            # Use the level4 name as the key for data storage
            location_name = entry["level4"]
            
            row_data = {"Location": location_name, "Display": location_display, "Path": path_str}
            
            # Add a column for each callout type
            for ct in st.session_state.callout_types:
                key = f"matrix_{location_name}_{ct}".replace(" ", "_")
                if key not in st.session_state.responses:
                    st.session_state.responses[key] = False
                row_data[ct] = st.session_state.responses[key]
            
            matrix_data.append(row_data)
    
    # Sort the matrix by hierarchy path to group related locations together
    if matrix_data:
        matrix_data = sorted(matrix_data, key=lambda x: x["Path"])
    
    return matrix_data

def create_preview_data(matrix_data):
    """Create a display version of the matrix for the preview"""
    if not matrix_data:
        return []
        
    # Create a display version of the matrix for the preview
    preview_data = []
    for row in matrix_data:
        # Use the hierarchical display name for the preview
        display_row = {"Location": row["Display"]}
        for ct in st.session_state.callout_types:
            key = f"matrix_{row['Location']}_{ct}".replace(" ", "_")
            display_row[ct] = "X" if key in st.session_state.responses and st.session_state.responses[key] else ""
        preview_data.append(display_row)
    
    return preview_data