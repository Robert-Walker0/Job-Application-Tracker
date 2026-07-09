import os

def get_frontend_remote_origin() -> str:
    url = os.getenv("FRONTEND_REMOTE_URL")
    if url is None:
        raise RuntimeError("FRONTEND_REMOTE_URL is not configured.")
    return url