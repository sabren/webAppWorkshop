import os

NS_MASTER = "[webappworkshop]"

def namespace_manager_default_namespace_for_request():
    return os.environ.get("SERVER_NAME", NS_MASTER)
