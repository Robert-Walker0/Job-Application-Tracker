import pytest
from origins import get_frontend_remote_origin


def test_get_frontend_origin_dev(monkeypatch):
    monkeypatch.setenv("FRONTEND_REMOTE_URL", "http://localhost:5173")
    monkeypatch.setenv("ENVIRONMENT", "development")

    result = get_frontend_remote_origin()

    assert result == "http://localhost:5173"


@pytest.mark.parametrize("bad_env", ["prod", "dev", "garbage", "123", "stage", ""])
def test_get_frontend_origin_bad_envs(monkeypatch, bad_env):
    monkeypatch.setenv("ENVIRONMENT", bad_env)

    with pytest.raises(
        RuntimeError, match=f"ENVIRONMENT '{bad_env}' is not recognized."
    ):
        get_frontend_remote_origin()


def test_get_frontend_remote_origin_prod_raises_error(monkeypatch):
    monkeypatch.delenv("FRONTEND_REMOTE_URL", raising=False)
    monkeypatch.setenv("ENVIRONMENT", "production")

    with pytest.raises(RuntimeError, match="FRONTEND_REMOTE_URL is not configured."):
        get_frontend_remote_origin()
