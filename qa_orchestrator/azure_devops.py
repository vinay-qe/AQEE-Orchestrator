"""
Azure DevOps integration for AQEE agents.

Provides secure integration with Azure DevOps for:
- Creating and managing User Stories
- Managing Test Plans and Test Cases
- Creating work items and tracking issues
- Retrieving project information
"""

from typing import Optional, Dict, List, Any
import logging
import requests
from base64 import b64encode
from qa_orchestrator.secrets import get_credential

logger = logging.getLogger(__name__)


class AzureDevOpsClient:
    """Secure client for Azure DevOps API interactions."""

    def __init__(self):
        """Initialize Azure DevOps client with credentials from environment."""
        self.org_url = get_credential("azure_devops_org_url")
        self.token = get_credential("azure_devops_token")
        self.api_version = "7.1"
        self.session = None

    def _setup_session(self) -> requests.Session:
        """Create authenticated session."""
        if self.session:
            return self.session

        if not self.org_url or not self.token:
            logger.error("Azure DevOps credentials not configured")
            return None

        session = requests.Session()
        # Azure DevOps uses Basic auth with PAT
        auth_string = b64encode(f":{self.token}".encode()).decode()
        session.headers.update({
            "Authorization": f"Basic {auth_string}",
            "Content-Type": "application/json",
        })
        self.session = session
        return session

    def is_configured(self) -> bool:
        """Check if Azure DevOps integration is properly configured."""
        return bool(self.org_url and self.token)

    def create_user_story(
        self,
        project: str,
        title: str,
        description: str,
        acceptance_criteria: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Create a User Story in Azure DevOps.

        Args:
            project: Azure DevOps project name
            title: User Story title
            description: User Story description
            acceptance_criteria: List of acceptance criteria

        Returns:
            Work item details or None if failed
        """
        if not self.is_configured():
            logger.warning("Azure DevOps not configured; cannot create User Story")
            return None

        session = self._setup_session()
        if not session:
            return None

        criteria_text = "\n".join(f"- {c}" for c in acceptance_criteria)
        body = f"{description}\n\nAcceptance Criteria:\n{criteria_text}"

        url = f"{self.org_url}/{project}/_apis/wit/workitems/$User%20Story?api-version={self.api_version}"

        payload = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/System.Description", "value": body},
        ]

        try:
            response = session.patch(url, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Created User Story: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to create User Story: {e}")
            return None

    def create_test_plan(
        self, project: str, name: str, description: str
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Test Plan in Azure DevOps.

        Args:
            project: Azure DevOps project name
            name: Test Plan name
            description: Test Plan description

        Returns:
            Test Plan details or None if failed
        """
        if not self.is_configured():
            logger.warning("Azure DevOps not configured; cannot create Test Plan")
            return None

        session = self._setup_session()
        if not session:
            return None

        url = f"{self.org_url}/{project}/_apis/test/plans?api-version={self.api_version}"

        payload = {
            "name": name,
            "description": description,
            "state": "Active",
        }

        try:
            response = session.post(url, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Created Test Plan: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to create Test Plan: {e}")
            return None

    def create_test_case(
        self,
        project: str,
        title: str,
        steps: List[str],
        expected_results: List[str],
    ) -> Optional[Dict[str, Any]]:
        """
        Create a Test Case in Azure DevOps.

        Args:
            project: Azure DevOps project name
            title: Test Case title
            steps: Test execution steps
            expected_results: Expected results for each step

        Returns:
            Test Case details or None if failed
        """
        if not self.is_configured():
            logger.warning("Azure DevOps not configured; cannot create Test Case")
            return None

        session = self._setup_session()
        if not session:
            return None

        steps_text = "\n".join(f"{i+1}. {s}" for i, s in enumerate(steps))
        results_text = "\n".join(f"{i+1}. {r}" for i, r in enumerate(expected_results))

        url = f"{self.org_url}/{project}/_apis/wit/workitems/$Test%20Case?api-version={self.api_version}"

        payload = [
            {"op": "add", "path": "/fields/System.Title", "value": title},
            {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.Steps", "value": steps_text},
            {"op": "add", "path": "/fields/Microsoft.VSTS.TCM.ExpectedResult", "value": results_text},
        ]

        try:
            response = session.patch(url, json=payload)
            response.raise_for_status()
            result = response.json()
            logger.info(f"Created Test Case: {result.get('id')}")
            return result
        except Exception as e:
            logger.error(f"Failed to create Test Case: {e}")
            return None

    def get_project_info(self, project: str) -> Optional[Dict[str, Any]]:
        """Get project information from Azure DevOps."""
        if not self.is_configured():
            logger.warning("Azure DevOps not configured")
            return None

        session = self._setup_session()
        if not session:
            return None

        url = f"{self.org_url}/_apis/projects/{project}?api-version={self.api_version}"

        try:
            response = session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Failed to get project info: {e}")
            return None


# Global Azure DevOps client instance
_ado_client = AzureDevOpsClient()


def get_ado_client() -> AzureDevOpsClient:
    """Get the global Azure DevOps client instance."""
    return _ado_client
