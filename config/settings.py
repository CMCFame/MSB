# ============================================================================
# ARCOS SIG FORM - CONFIGURATION SETTINGS
# ============================================================================

# ============================================================================
# APPLICATION SETTINGS
# ============================================================================
# This file contains settings that might need to be changed based on deployment 
# environment or user preferences.

# Application title that appears in the browser tab
APP_TITLE = "ARCOS SIG Form"

# Default tab to show when the application first loads
DEFAULT_TAB = "Location Hierarchy"

# Enable or disable the AI assistant feature
ENABLE_AI_ASSISTANT = True

# ============================================================================
# FILE PATHS
# ============================================================================
# Paths to data files used by the application

# Path to callout reasons JSON file
CALLOUT_REASONS_PATH = "data/callout_reasons.json"

# Path to SIG descriptions JSON file
SIG_DESCRIPTIONS_PATH = "data/sig_descriptions.json"

# Path to ARCOS logo
LOGO_PATH = "https://www.arcos-inc.com/wp-content/uploads/2020/10/logo-arcos-news.png"

# ============================================================================
# AI ASSISTANT SETTINGS
# ============================================================================
# Configuration for the AI assistant feature

# System prompt for the AI assistant
ASSISTANT_SYSTEM_PROMPT = """
You are a helpful expert on ARCOS system implementation. Your role is to assist users 
in completing their ARCOS System Implementation Guide form.

Provide clear explanations of ARCOS concepts, best practices for configuration, and 
helpful examples from the utility industry where appropriate.

Consider the user's current task (indicated by the tab they're working on) when providing guidance.
"""

# Maximum number of chat history messages to display
MAX_CHAT_HISTORY = 10

# ============================================================================
# EXPORT SETTINGS
# ============================================================================
# Configuration for data export functionality

# Default filename for exported data (without extension)
DEFAULT_EXPORT_FILENAME = "arcos_sig"

# Include timestamp in export filenames
INCLUDE_TIMESTAMP_IN_FILENAME = True

# Timestamp format for export filenames
TIMESTAMP_FORMAT = "%Y%m%d_%H%M%S"