import pytest
from origins import get_frontend_remote_origin


def test_get_frontend_remote_origin_missing(monkeypatch):
    """Tests whether the remotre origin of the application is missing"""
    monkeypatch.delenv("FRONTEND_REMOTE_URL", raising=False)
    with pytest.raises(RuntimeError):
        get_frontend_remote_origin()
