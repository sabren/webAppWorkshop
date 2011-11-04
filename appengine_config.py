"""
Sets a new namespace based on the HTTP SERVER_NAME.
"""
import os

def namespace_manager_default_namespace_for_request():
    return os.environ["SERVER_NAME"]
