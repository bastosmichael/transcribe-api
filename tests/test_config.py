from transcribe.config import Config, config


def test_config():
    cfg = config()
    assert isinstance(cfg, Config)
    assert hasattr(cfg, "aws_access_key_id")
    assert hasattr(cfg, "aws_secret_access_key")
    assert hasattr(cfg, "aws_session_token")
    assert hasattr(cfg, "s3_bucket_name")
    assert hasattr(cfg, "region")
