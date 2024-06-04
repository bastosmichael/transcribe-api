from transcribe.config import Config, get_config


def test_get_config():
    config = get_config()
    assert isinstance(config, Config)
    assert hasattr(config, "aws_access_key_id")
    assert hasattr(config, "aws_secret_access_key")
    assert hasattr(config, "aws_session_token")
    assert hasattr(config, "s3_bucket_name")
    assert hasattr(config, "region")
