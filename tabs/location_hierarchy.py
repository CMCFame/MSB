# ============================================================================
# LOCATION HIERARCHY TAB
# ============================================================================
import streamlit as st
from utils.ui_helpers import render_color_key, create_horizontal_rule, show_info_box

def render_location_hierarchy_form():
    """Render the Location Hierarchy form with integrated callout types and reasons"""
    st.markdown('<p class="tab-header">Location Hierarchy - Complete Configuration</p>', unsafe_allow_html=True)
    
    # Display descriptive text
    with st.expander("Instructions", expanded=False):
        st.markdown("""
        In ARCOS, your geographical service territory will be represented by a 4-level location hierarchy. You may refer to each Level by changing the Label to suit your requirements. The breakdown doesn't have to be geographical. Different business functions may also be split into different Level 2 or Level 3 locations.
        
        **Location names must contain a blank space per 25 contiguous characters.** Example: the hyphenated village of "Sutton-under-Whitestonecliffe" in England would be considered invalid (29 contiguous characters). Sutton under Whitestonecliffe would be valid. The max length for a location name is 50 characters.
        
        **Each Level 4 entry must have an accompanying Location Code.** This code can be from your HR system or something you create. It is important to make sure each code and each Location Name (on all levels) is unique. A code can be any combination of numbers and letters.
        
        **To create sub-branches:** 
        - Add a new location entry and fill only the levels you need.
        - Use the "Add sub-branch" buttons to quickly create entries that inherit values from their parent levels.
        
        **For each Level 4 (OpCenter):**
        - Add Location Codes (up to 5)
        - Configure Callout Types that apply to this location
        - Specify Callout Reasons specific to this location (comma-separated)
        """)
    
    # Add New Location button
    if st.button("➕ Add New Location Entry"):
        st.session_state.hierarchy_data["entries"].append(
            {
                "level1": "", 
                "level2": "", 
                "level3": "", 
                "level4": "", 
                "timezone": "", 
                "codes": ["", "", "", "", ""],
                "callout_types": {
                    "Normal": False,
                    "All Hands on Deck": False,
                    "Fill Shift": False,
                    "Travel": False,
                    "Notification": False,
                    "Notification (No Response)": False
                },
                "callout_reasons": ""
            }
        )
        st.rerun()
    
    # Default time zone info
    st.markdown('<p class="section-header">Default Time Zone</p>', unsafe_allow_html=True)
    st.write("Set a default time zone to be used when a specific zone is not specified for a location entry.")
    default_timezone = st.text_input("Default Time Zone", 
                                   value=st.session_state.hierarchy_data["timezone"])
    st.session_state.hierarchy_data["timezone"] = default_timezone
    
    # Preview of hierarchy structure in table format
    st.markdown('<p class="section-header">Hierarchy Entries</p>', unsafe_allow_html=True)
    
    # Display a table header without using columns
    labels = st.session_state.hierarchy_data["labels"]
    st.markdown(f"""
    <div style="display: flex; margin-bottom: 10px; font-weight: bold;">
        <div style="flex: 0.5; min-width: 50px;">Entry #</div>
        <div style="flex: 2;">{labels[0]}</div>
        <div style="flex: 2;">{labels[1]}</div>
        <div style="flex: 2;">{labels[2]}</div>
        <div style="flex: 2;">{labels[3]}</div>
        <div style="flex: 2;">Time Zone</div>
        <div style="flex: 0.5; min-width: 50px;">Actions</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Instead of nesting columns, we'll create a separate row for each entry
    for i, entry in enumerate(st.session_state.hierarchy_data["entries"]):
        # Creating separate containers for each row to avoid nesting columns
        entry_container = st.container()
        
        # Use a simple single-level column layout for each entry
        with entry_container:
            row_cols = st.columns([0.5, 2, 2, 2, 2, 2, 0.5])
            
            with row_cols[0]:
                st.write(f"#{i+1}")
            
            with row_cols[1]:
                entry["level1"] = st.text_input("Level 1", value=entry["level1"], key=f"lvl1_{i}", 
                                              placeholder=f"Enter {labels[0]}", label_visibility="collapsed")
            
            with row_cols[2]:
                entry["level2"] = st.text_input("Level 2", value=entry["level2"], key=f"lvl2_{i}", 
                                              placeholder=f"Enter {labels[1]}", label_visibility="collapsed")
            
            with row_cols[3]:
                entry["level3"] = st.text_input("Level 3", value=entry["level3"], key=f"lvl3_{i}", 
                                              placeholder=f"Enter {labels[2]}", label_visibility="collapsed")
            
            with row_cols[4]:
                entry["level4"] = st.text_input("Level 4", value=entry["level4"], key=f"lvl4_{i}", 
                                              placeholder=f"Enter {labels[3]}", label_visibility="collapsed")
            
            with row_cols[5]:
                entry["timezone"] = st.text_input("Time Zone", value=entry.get("timezone", ""), key=f"tz_{i}",
                                               placeholder=st.session_state.hierarchy_data["timezone"], 
                                               label_visibility="collapsed")
            
            with row_cols[6]:
                # Delete button
                if st.button("🗑️", key=f"del_{i}", help="Remove this entry"):
                    st.session_state.hierarchy_data["entries"].pop(i)
                    st.rerun()
        
        # Sub-branch buttons in a separate container
        if entry["level1"]:
            branch_container = st.container()
            with branch_container:
                sb_cols = st.columns([4, 2, 2, 2, 2])
                
                # Add Business Unit button (only if level1 is filled)
                with sb_cols[1]:
                    if st.button(f"+ Add Business Unit", key=f"add_bu_{i}", 
                               help=f"Add a new Business Unit under {entry['level1']}"):
                        new_entry = {
                            "level1": entry["level1"],
                            "level2": "",
                            "level3": "",
                            "level4": "",
                            "timezone": entry.get("timezone", ""),
                            "codes": ["", "", "", "", ""],
                            "callout_types": {
                                "Normal": False,
                                "All Hands on Deck": False,
                                "Fill Shift": False,
                                "Travel": False,
                                "Notification": False,
                                "Notification (No Response)": False
                            },
                            "callout_reasons": ""
                        }
                        st.session_state.hierarchy_data["entries"].append(new_entry)
                        st.rerun()
                
                # Add Division button (only if level1 and level2 are filled)
                with sb_cols[2]:
                    if entry["level2"]:
                        if st.button(f"+ Add Division", key=f"add_div_{i}", 
                                   help=f"Add a new Division under {entry['level2']}"):
                            new_entry = {
                                "level1": entry["level1"],
                                "level2": entry["level2"],
                                "level3": "",
                                "level4": "",
                                "timezone": entry.get("timezone", ""),
                                "codes": ["", "", "", "", ""],
                                "callout_types": {
                                    "Normal": False,
                                    "All Hands on Deck": False,
                                    "Fill Shift": False,
                                    "Travel": False,
                                    "Notification": False,
                                    "Notification (No Response)": False
                                },
                                "callout_reasons": ""
                            }
                            st.session_state.hierarchy_data["entries"].append(new_entry)
                            st.rerun()
                
                # Add OpCenter button (only if level1, level2, and level3 are filled)
                with sb_cols[3]:
                    if entry["level2"] and entry["level3"]:
                        if st.button(f"+ Add OpCenter", key=f"add_op_{i}", 
                                   help=f"Add a new OpCenter under {entry['level3']}"):
                            new_entry = {
                                "level1": entry["level1"],
                                "level2": entry["level2"],
                                "level3": entry["level3"],
                                "level4": "",
                                "timezone": entry.get("timezone", ""),
                                "codes": ["", "", "", "", ""],
                                "callout_types": {
                                    "Normal": False,
                                    "All Hands on Deck": False,
                                    "Fill Shift": False,
                                    "Travel": False,
                                    "Notification": False,
                                    "Notification (No Response)": False
                                },
                                "callout_reasons": ""
                            }
                            st.session_state.hierarchy_data["entries"].append(new_entry)
                            st.rerun()
        
        # LEVEL 4 CONFIGURATION in a separate container
        if entry["level4"]:
            with st.expander(f"Configure {entry['level4']} Details", expanded=False):
                # 1. LOCATION CODES SECTION
                st.markdown(f"<div style='margin: 10px 0;'><b>Location Codes for {entry['level4']}</b></div>", unsafe_allow_html=True)
                
                # Split code fields into separate containers to avoid nesting
                for j in range(0, 5, 5):  # Step by 5 to create separate rows
                    code_container = st.container()
                    with code_container:
                        code_cols = st.columns(5)
                        for k in range(5):
                            idx = j + k
                            if idx < 5:  # Ensure we don't go out of bounds
                                with code_cols[k]:
                                    if idx < len(entry["codes"]):
                                        entry["codes"][idx] = st.text_input(f"Code {idx+1}", 
                                                                        value=entry["codes"][idx], 
                                                                        key=f"code_{i}_{idx}")
                                    else:
                                        # Ensure we have 5 codes
                                        while len(entry["codes"]) <= idx:
                                            entry["codes"].append("")
                                        entry["codes"][idx] = st.text_input(f"Code {idx+1}", 
                                                                        value="", 
                                                                        key=f"code_{i}_{idx}")
                
                st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
                
                # 2. CALLOUT TYPES SECTION
                st.markdown(f"<div style='margin: 10px 0;'><b>Callout Types for {entry['level4']}</b></div>", unsafe_allow_html=True)
                st.write("Select the callout types available for this location:")
                
                # Split checkboxes into separate groups to avoid nesting
                ct_container1 = st.container()
                with ct_container1:
                    ct_cols1 = st.columns(3)
                    with ct_cols1[0]:
                        entry["callout_types"]["Normal"] = st.checkbox(
                            "Normal", 
                            value=entry["callout_types"].get("Normal", False),
                            key=f"ct_normal_{i}"
                        )
                    
                    with ct_cols1[1]:
                        entry["callout_types"]["All Hands on Deck"] = st.checkbox(
                            "All Hands on Deck", 
                            value=entry["callout_types"].get("All Hands on Deck", False),
                            key=f"ct_ahod_{i}"
                        )
                    
                    with ct_cols1[2]:
                        entry["callout_types"]["Fill Shift"] = st.checkbox(
                            "Fill Shift", 
                            value=entry["callout_types"].get("Fill Shift", False),
                            key=f"ct_fill_{i}"
                        )
                
                ct_container2 = st.container()
                with ct_container2:
                    ct_cols2 = st.columns(3)
                    with ct_cols2[0]:
                        entry["callout_types"]["Travel"] = st.checkbox(
                            "Travel", 
                            value=entry["callout_types"].get("Travel", False),
                            key=f"ct_travel_{i}"
                        )
                    
                    with ct_cols2[1]:
                        entry["callout_types"]["Notification"] = st.checkbox(
                            "Notification", 
                            value=entry["callout_types"].get("Notification", False),
                            key=f"ct_notif_{i}"
                        )
                    
                    with ct_cols2[2]:
                        entry["callout_types"]["Notification (No Response)"] = st.checkbox(
                            "Notification (No Response)", 
                            value=entry["callout_types"].get("Notification (No Response)", False),
                            key=f"ct_notif_nr_{i}"
                        )
                
                st.markdown("<hr style='margin: 15px 0;'>", unsafe_allow_html=True)
                
                # 3. CALLOUT REASONS SECTION
                st.markdown(f"<div style='margin: 10px 0;'><b>Callout Reasons for {entry['level4']}</b></div>", unsafe_allow_html=True)
                st.write("Enter applicable callout reasons for this location (comma-separated):")
                
                entry["callout_reasons"] = st.text_area(
                    "Callout Reasons",
                    value=entry.get("callout_reasons", ""),
                    height=100,
                    key=f"reasons_{i}",
                    placeholder="Gas Leak, Gas Fire, Gas Emergency, Car Hit Pole, Wires Down"
                )
            
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
        else:
            if entry["level1"] or entry["level2"] or entry["level3"]:
                st.info(f"Enter {labels[3]} to complete this entry and add location codes, callout types, and reasons.")
            st.markdown("<hr style='margin: 10px 0;'>", unsafe_allow_html=True)
    
    # Show preview in a separate container to avoid nesting
    preview_container = st.container()
    with preview_container:
        st.markdown('<p class="section-header">Hierarchy Preview</p>', unsafe_allow_html=True)
        
        # Generate a text representation of the hierarchy
        preview_text = generate_hierarchy_preview(st.session_state.hierarchy_data)
        st.code(preview_text)
        
        # Display sample hierarchy from example
        st.markdown('<p class="section-header">Sample Hierarchy</p>', unsafe_allow_html=True)
        st.info("""
        Example hierarchy:
        
        • CenterPoint Energy (Level 1)
          • Houston Electric (Level 2)
            • Distribution Operations (Level 3)
              • Baytown (Level 4, Codes: B1, B2, B3)
                [Callout Types: Normal, All Hands on Deck]
                [Callout Reasons: Gas Leak, Gas Fire, Gas Emergency]
              • Bellaire (Level 4, Codes: ENN1, ENN2)
                [Callout Types: Normal, Fill Shift]
                [Callout Reasons: Car Hit Pole, Wires Down]
        """)

def generate_hierarchy_preview(hierarchy_data):
    """Create a tree structure to organize the hierarchy and return a text representation"""
    # Create a tree structure to organize the hierarchy
    tree = {}
    
    # Populate the tree
    for entry in hierarchy_data["entries"]:
        if not entry["level1"]:
            continue
            
        l1 = entry["level1"]
        if l1 not in tree:
            tree[l1] = {}
        
        if entry["level2"]:
            l2 = entry["level2"]
            if l2 not in tree[l1]:
                tree[l1][l2] = {}
            
            if entry["level3"]:
                l3 = entry["level3"]
                if l3 not in tree[l1][l2]:
                    tree[l1][l2][l3] = []
                
                if entry["level4"]:
                    l4_info = {
                        "name": entry["level4"],
                        "codes": [c for c in entry["codes"] if c],
                        "timezone": entry["timezone"],
                        "callout_types": [ct for ct, enabled in entry["callout_types"].items() if enabled],
                        "callout_reasons": entry["callout_reasons"]
                    }
                    tree[l1][l2][l3].append(l4_info)
    
    # Generate the text representation
    lines = []
    
    for l1, l1_children in tree.items():
        lines.append(f"• {l1}")
        
        for l2, l2_children in l1_children.items():
            lines.append(f"  • {l2}")
            
            for l3, l3_children in l2_children.items():
                lines.append(f"    • {l3}")
                
                for l4_info in l3_children:
                    lines.append(f"      • {l4_info['name']}")
                    
                    if l4_info["codes"]:
                        lines.append(f"        (Codes: {', '.join(l4_info['codes'])})")
                    
                    if l4_info["timezone"]:
                        lines.append(f"        [Time Zone: {l4_info['timezone']}]")
                    
                    if l4_info["callout_types"]:
                        lines.append(f"        [Callout Types: {', '.join(l4_info['callout_types'])}]")
                    
                    if l4_info["callout_reasons"]:
                        lines.append(f"        [Callout Reasons: {l4_info['callout_reasons']}]")
    
    if not lines:
        return "No entries yet. Use the form on the left to add location hierarchy entries."
    
    return "\n".join(lines)