import subprocess
import os

class StaticAnalysisTools:
    def __init__(self, workspace_path: str):
        self.workspace_path = workspace_path

    def run_semgrep_scan(self, path: str = ".") -> str:
        """Runs a Semgrep scan on the specified path."""
        try:
            # We assume Semgrep is installed in the environment
            # Using --config p/security to catch common vulnerabilities
            result = subprocess.run(
                ["semgrep", "--config=p/security", "--json", path],
                capture_output=True, text=True, cwd=self.workspace_path
            )
            return result.stdout
        except Exception as e:
            return f"Error running Semgrep: {str(e)}"

    def dependency_scan(self) -> str:
        """Runs a dependency vulnerability scan (e.g., using safety or pip-audit)."""
        try:
            # Simple check using safety if available
            result = subprocess.run(
                ["pip-audit", "--format", "json"],
                capture_output=True, text=True, cwd=self.workspace_path
            )
            return result.stdout
        except Exception as e:
            return f"Error running dependency scan: {str(e)}"

    def lint_code(self, file_path: str) -> str:
        """Runs a linter like flake8 on the given file."""
        try:
            result = subprocess.run(
                ["flake8", file_path],
                capture_output=True, text=True, cwd=self.workspace_path
            )
            return result.stdout or "No issues found."
        except Exception as e:
            return f"Error running linter: {str(e)}"
