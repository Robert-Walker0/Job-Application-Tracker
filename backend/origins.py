import os

ALLOWED_ENVIRONMENTS = {"production", "development", "test"}


def get_frontend_remote_origin() -> str:

    env = os.getenv("ENVIRONMENT", "development").lower()
    url = os.getenv("FRONTEND_REMOTE_URL")

    if env not in ALLOWED_ENVIRONMENTS:
        raise RuntimeError(f"ENVIRONMENT '{env}' is not recognized.")

    if url is None:
        if env == "production":
            raise RuntimeError("FRONTEND_REMOTE_URL is not configured.")

        return "http://localhost:5173"

    return url
