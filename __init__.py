# QA Agent Ecosystem - AQEE
# Import `root_agent` from the main agent module for ADK discovery.
# Use tolerant imports so test runners that import this package as a plain
# module don't fail on relative imports.
try:
	from .agent import root_agent  # package-style import (normal ADK runtime)
except Exception:
	try:
		# fallback to absolute import when running tests or scripts
		from agent import root_agent
	except Exception:
		root_agent = None

__all__ = ["root_agent"]
