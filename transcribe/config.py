from functools import lru_cache
from pydantic import BaseSettings


class Config(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str = None
    s3_bucket_name: str
    region: str = "us-east-1"  # Ensure this matches your bucket's region

    class Config:
        env_file = ".env"


@lru_cache()
def get_config():
    return Config()
