"""Load versioned policy text used by the ADK agents."""

from pathlib import Path


POLICY_DIR = Path(__file__).parents[1] / "policies"
SECURITY_POLICY = (POLICY_DIR / "security.md").read_text(encoding="utf-8")
