from transcribe.config import Settings, get_settings


def test_get_settings():
    settings = get_settings()
    assert isinstance(settings, Settings)
    assert hasattr(settings, "aws_access_key_id")
    assert hasattr(settings, "aws_secret_access_key")
    assert hasattr(settings, "aws_session_token")
    assert hasattr(settings, "s3_bucket_name")
    assert hasattr(settings, "region")
