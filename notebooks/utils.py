import os

# S3 endpoint of our object store
ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL")

# S3 bucket used in the workshop
BUCKET = "cng-forum-workshop" 
BUCKET_URI = f"s3://{BUCKET}"

# Set prefix where the current user can write to
USER_NAME = os.getenv("JUPYTERHUB_USER") or os.getenv("USER")
USER_PREFIX_URI = f"{BUCKET}/users/{USER_NAME}"   


def https_url(urlpath: str) -> str:
    """Convert s3://bucket/key to the public (path-style) HTTPS URL."""
    return f"{ENDPOINT_URL}/{urlpath.removeprefix('s3://')}"