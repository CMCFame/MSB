# ============================================================================
# GENERIC TAB RENDERER
# ============================================================================
import streamlit as st
import json
from utils.ai_assistant import get_openai_response, save_chat_history

def render_generic_tab(tab_name):
    """Render a generic form for tabs that are not yet implemented with custom UI"""
    st.markdown(f'<p class="tab-header">{tab_name}</p>', unsafe_allow_html=True)
    
    # Load descriptions
    try:
        with open('data/sig_descriptions.json', 'r') as file:
            descriptions = json.load(file)
        
        if tab_name in descriptions:
            tab_desc = descriptions[tab_name]
            st.write(tab_desc["description"])
            
            # Create form fields for this tab
            for field_name, field_info in tab_desc["fields"].items():
                field_key = f"{tab_name}_{field_name}".replace(" ", "_").lower()
                
                # Create expandable section for each field
                with st.expander(f"{field_name}", expanded=False):
                    st.markdown(f"**Description:** {field_info['description']}")
                    
                    if "example" in field_info:
                        st.markdown(f"**Example:** {field_info['example']}")
                    
                    if "best_practices" in field_info:
                        st.markdown(f"**Best Practices:** {field_info['best_practices']}")
                    
                    # Get existing value from session state
                    existing_value = st.session_state.responses.get(field_key, "")
                    
                    # Display input field
                    response = st.text_area(
                        label=f"Enter your {field_name} details below",
                        value=existing_value,
                        height=150,
                        key=field_key
                    )
                    
                    # Store response in session state
                    st.session_state.responses[field_key] = response
                    
                    # Add a help button for this field
                    if st.button(f"Get more help with {field_name}", key=f"help_{field_key}"):
                        help_query = f"Explain in detail what information is needed for the '{field_name}' section in the '{tab_name}' tab of the ARCOS System Implementation Guide. Include examples, best practices, and common configurations."
                        with st.spinner("Loading help..."):
                            help_response = get_openai_response(help_query)
                            save_chat_history(f"Help with {field_name}", help_response)
                        
                        st.info(help_response)
        else:
            st.write(f"This tab allows you to configure {tab_name} settings in ARCOS.")
            
            # Generic text field for this tab
            tab_key = tab_name.replace(" ", "_").lower()
            existing_value = st.session_state.responses.get(tab_key, "")
            
            response = st.text_area(
                label=f"Enter {tab_name} details",
                value=existing_value,
                height=300,
                key=tab_key
            )
            
            st.session_state.responses[tab_key] = response
            
    except Exception as e:
        st.error(f"Error loading tab data: {str(e)}")
        
        # Generic text field as fallback
        tab_key = tab_name.replace(" ", "_").lower()
        existing_value = st.session_state.responses.get(tab_key, "")
        
        response = st.text_area(
            label=f"Enter {tab_name} details",
            value=existing_value,
            height=300,
            key=tab_key
        )
        
        st.session_state.responses[tab_key] = response