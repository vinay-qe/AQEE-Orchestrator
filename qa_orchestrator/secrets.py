"""
Secure credential management for AQEE agents.

This module handles API keys and sensitive credentials safely:
- Loads from environment variables (preferred)
- Validates presence before use
- Prevents credential leakage in logs/outputs
- Supports credential rotation
"""

import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class CredentialManager:
    """Securely manage API credentials without exposing them."""

    def __init__(self):
        """Initialize credential manager."""
        self._credentials = {}
        self._loaded = False

    def load_from_env(self) -> None:
        """Load credentials from environment variables."""
        self._credentials = {
            "google_api_key": os.getenv("GOOGLE_API_KEY"),
            "azure_devops_token": os.getenv("AZURE_DEVOPS_TOKEN"),
            "azure_devops_org_url": os.getenv("AZURE_DEVOPS_ORG_URL"),
        }
        self._loaded = True
        self._validate_credentials()

    def _validate_credentials(self) -> None:
        """Validate that required credentials are present."""
        required = ["google_api_key", "azure_devops_token", "azure_devops_org_url"]
        missing = [k for k in required if not self._credentials.get(k)]
        if missing:
            logger.warning(f"Missing credentials: {', '.join(missing)}")

    def get_credential(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Safely retrieve a credential without exposing it in logs."""
        if not self._loaded:
            self.load_from_env()
        value = self._credentials.get(key, default)
        # Never log the actual value
        if value:
            logger.debug(f"Credential '{key}' loaded successfully")
        return value

    def has_credential(self, key: str) -> bool:
        """Check if a credential is available without exposing it."""
        if not self._loaded:
            self.load_from_env()
        return bool(self._credentials.get(key))

    def __repr__(self) -> str:
        """Prevent credential leakage in string representation."""
        return f"<CredentialManager with {len([k for k, v in self._credentials.items() if v])} credentials loaded>"


# Global credential manager instance
_credential_manager = CredentialManager()


def get_credential(key: str, default: Optional[str] = None) -> Optional[str]:
    """Convenience function to get a credential."""
    return _credential_manager.get_credential(key, default)


def has_credential(key: str) -> bool:
    """Convenience function to check if credential exists."""
    return _credential_manager.has_credential(key)


def load_credentials() -> None:
    """Explicitly load credentials from environment."""
    _credential_manager.load_from_env()
