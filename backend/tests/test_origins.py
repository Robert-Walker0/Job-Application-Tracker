import pytest
from origins import get_frontend_remote_origin

def test_get_frontend_remote_origin(monkeypatch):
    monkeypatch.setenv(
        "FRONTEND_REMOTE_URL",
        "https://example.com"
    )

    assert get_frontend_remote_origin() == "https://example.com"

def test_get_frontend_remote_origin_missing(monkeypatch):
    monkeypatch.delenv("FRONTEND_REMOTE_URL", raising=False)
    with pytest.raises(RuntimeError):
        get_frontend_remote_origin()
