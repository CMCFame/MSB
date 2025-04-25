# ============================================================================
# CONSTANTS AND CONFIGURATION VALUES
# ============================================================================

# Streamlit page configuration
PAGE_TITLE = "ARCOS SIG Form"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "expanded"

# Define color scheme to match ARCOS branding
ARCOS_RED = "#e3051b"
ARCOS_LIGHT_RED = "#ffcccc"
ARCOS_GREEN = "#99cc99"
ARCOS_BLUE = "#6699ff"

# Custom CSS to improve the look and feel
CUSTOM_CSS = """
<style>
    .main-header {color: #e3051b; font-size: 2.5rem; font-weight: bold;}
    .tab-header {color: #e3051b; font-size: 1.5rem; font-weight: bold; margin-top: 1rem;}
    .section-header {font-size: 1.2rem; font-weight: bold; margin-top: 1rem; margin-bottom: 0.5rem;}
    .info-box {background-color: #f0f0f0; padding: 10px; border-radius: 5px; margin-bottom: 10px;}
    .red-bg {background-color: #ffcccc;}
    .green-bg {background-color: #99cc99;}
    .blue-bg {background-color: #6699ff;}
    .stButton>button {background-color: #e3051b; color: white;}
    .stButton>button:hover {background-color: #b30000;}
    .help-btn {font-size: 0.8rem; padding: 2px 8px;}
    .st-emotion-cache-16idsys p {font-size: 14px;}
    .hierarchy-table th {background-color: #e3051b; color: white; text-align: center; font-weight: bold;}
    .hierarchy-table td {text-align: center; padding: 8px;}
    .color-key-box {padding: 5px; margin: 2px; display: inline-block; width: 80px; text-align: center;}
    .arcos-logo {max-width: 200px; margin-bottom: 10px;}
    .download-button {background-color: #28a745; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none; display: inline-block; margin-top: 10px;}
    .download-button:hover {background-color: #218838; color: white; text-decoration: none;}
    
 /* Style for tab buttons to look like the screenshot */
    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: #f2f2f2 !important;
        color: black !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        font-weight: normal !important;
        width: 100% !important;
        height: 40px !important;
        margin-bottom: 5px !important;
        transition: background-color 0.3s ease !important;
    }
    
    /* Style for active tab button */
    div[data-testid="stButton"] button[kind="primary"] {
        background-color: #e3051b !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        width: 100% !important;
        height: 40px !important;
        margin-bottom: 5px !important;
    }
    
    /* Enhanced active tab styling */
    div[data-testid="stButton"] button.active {
        background-color: #b30000 !important; /* Darker shade of red for active state */
        color: white !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
    }
    
    /* Small export buttons */
    .small-export-btn {
        display: inline-block;
        width: 150px !important;
        font-size: 0.9em !important;
        margin: 0 10px !important;
    }
    
    /* Container for export buttons */
    .export-container {
        text-align: center;
        margin-top: 20px;
        margin-bottom: 20px;
    }
    
    /* Footer area */
    .footer-container {
        position: fixed;
        bottom: 20px;
        left: 0;
        right: 0;
        text-align: center;
        margin-left: auto;
        margin-right: auto;
        width: 100%;
        background-color: white;
        padding: 10px 0;
        border-top: 1px solid #f0f0f0;
    }
</style>
"""

# ARCOS Logo URL
ARCOS_LOGO_URL = "https://www.arcos-inc.com/wp-content/uploads/2020/10/logo-arcos-news.png"

# OpenAI model configuration
OPENAI_MODEL = "gpt-4o-2024-08-06"
OPENAI_MAX_TOKENS = 800
OPENAI_TEMPERATURE = 0.7

# Default data structures
DEFAULT_HIERARCHY_DATA = {
    "levels": ["Level 1", "Level 2", "Level 3", "Level 4"],
    "labels": ["Parent Company", "Business Unit", "Division", "OpCenter"],
    "entries": [
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
    ],
    "timezone": "ET / CT / MT / AZ / PT"
}

DEFAULT_CALLOUT_TYPES = [
    "Normal", "All Hands on Deck", "Fill Shift", "Travel", 
    "Notification", "Notification (No Response)"
]

DEFAULT_CALLOUT_REASONS = [
    "Gas Leak", "Gas Fire", "Gas Emergency", "Car Hit Pole", "Wires Down"
]

DEFAULT_JOB_CLASSIFICATION = {
    "type": "", 
    "title": "", 
    "ids": ["", "", "", "", ""], 
    "recording": ""
}

DEFAULT_TROUBLE_LOCATION = {
    "recording_needed": True, 
    "id": "", 
    "location": "", 
    "verbiage": ""
}