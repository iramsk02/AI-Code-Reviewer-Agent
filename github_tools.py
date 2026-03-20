import os
from github import Github
from dotenv import load_dotenv

load_dotenv()

class GitHubTools:
    def __init__(self, token=None, repo_name=None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.repo_name = repo_name or os.getenv("GITHUB_REPOSITORY")
        self.github = Github(self.token)
        if self.repo_name:
            self.repo = self.github.get_repo(self.repo_name)
    
    def get_pr_diff(self, pr_number: int) -> str:
        """Fetches the diff of a Pull Request."""
        pr = self.repo.get_pull(pr_number)
        # GitHub API returns the diff as a string via the 'diff' header or similar
        # For simplicity, we can get the PR comparison
        comparison = self.repo.compare(pr.base.sha, pr.head.sha)
        return comparison.patch if hasattr(comparison, 'patch') else ""

    def post_pr_comment(self, pr_number: int, body: str):
        """Posts a general comment on the PR."""
        pr = self.repo.get_pull(pr_number)
        pr.create_issue_comment(body)

    def post_inline_comment(self, pr_number: int, body: str, commit_id: str, path: str, line: int):
        """Posts an inline comment on a specific file and line."""
        pr = self.repo.get_pull(pr_number)
        pr.create_review_comment(body, commit_id, path, line)

    def get_file_content(self, path: str, ref: str = None) -> str:
        """Fetches the content of a file at a specific reference."""
        content = self.repo.get_contents(path, ref=ref)
        return content.decoded_content.decode("utf-8")
