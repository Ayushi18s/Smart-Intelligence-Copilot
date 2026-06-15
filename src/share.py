import uuid

shared_links = {}

def generate_share_link():
    token = str(uuid.uuid4())[:8]
    shared_links[token] = "dashboard_data"
    return f"http://localhost:8501/shared/{token}"