import os
import importlib

import pytest

from qa_orchestrator import secrets


def test_load_and_get_credentials(monkeypatch):
    monkeypatch.setenv("GOOGLE_API_KEY", "gkey-123")
    monkeypatch.setenv("AZURE_DEVOPS_TOKEN", "pat-abc")
    monkeypatch.setenv("AZURE_DEVOPS_ORG_URL", "https://dev.azure.com/fakeorg")

    # reload module to ensure fresh state
    importlib.reload(secrets)
    secrets.load_credentials()

    assert secrets.get_credential("google_api_key") == "gkey-123"
    assert secrets.has_credential("azure_devops_token") is True
    # repr should not leak actual token
    rep = repr(secrets._credential_manager)
    assert "pat-abc" not in rep


def test_missing_credentials_logs_warning(monkeypatch, caplog):
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("AZURE_DEVOPS_TOKEN", raising=False)
    monkeypatch.delenv("AZURE_DEVOPS_ORG_URL", raising=False)

    importlib.reload(secrets)
    with caplog.at_level("WARNING"):
        secrets.load_credentials()
        assert "Missing credentials" in caplog.text
