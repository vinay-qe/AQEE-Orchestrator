import importlib

from qa_orchestrator.azure_devops import get_ado_client
from qa_orchestrator import secrets


def test_ado_client_not_configured(monkeypatch):
    monkeypatch.delenv("AZURE_DEVOPS_TOKEN", raising=False)
    monkeypatch.delenv("AZURE_DEVOPS_ORG_URL", raising=False)

    importlib.reload(secrets)
    secrets.load_credentials()

    client = get_ado_client()
    assert client.is_configured() is False
    assert client.get_project_info("nonexistent") is None


def test_ado_client_setup_session(monkeypatch):
    monkeypatch.setenv("AZURE_DEVOPS_TOKEN", "pat-test-xyz")
    monkeypatch.setenv("AZURE_DEVOPS_ORG_URL", "https://dev.azure.com/fakeorg")

    importlib.reload(secrets)
    secrets.load_credentials()

    # Reload azure_devops to recreate the global client with fresh credentials
    import qa_orchestrator.azure_devops as ado_mod
    importlib.reload(ado_mod)
    client = ado_mod.get_ado_client()
    assert client.is_configured() is True
    session = client._setup_session()
    assert session is not None
    assert "Authorization" in session.headers
    assert session.headers.get("Content-Type") == "application/json"
