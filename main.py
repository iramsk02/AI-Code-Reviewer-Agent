import sys
import os
from dotenv import load_dotenv
from agent import ReviewAgent

# Load environment variables (useful for local development)
load_dotenv()

def main():
    # Setup parameters for the agent
    github_token = os.getenv("GITHUB_TOKEN")
    repo_name = os.getenv("GITHUB_REPOSITORY")
    workspace_path = os.getenv("GITHUB_WORKSPACE", ".")
    pr_number = os.getenv("PR_NUMBER")

    # Error handling for missing required environment variables
    if not github_token:
        print("Error: GITHUB_TOKEN is not set.")
        sys.exit(1)
    if not repo_name:
        print("Error: GITHUB_REPOSITORY is not set.")
        sys.exit(1)
    if not pr_number:
        print("Error: PR_NUMBER is not set.")
        sys.exit(1)

    # Initialize and run the reviewer agent
    try:
        pr_num = int(pr_number)
        reviewer = ReviewAgent(github_token, repo_name, workspace_path, pr_num)
        print(f"Starting review for PR #{pr_num} in repo {repo_name}...")
        
        result = reviewer.run_review()
        
        print(f"Review completed successfully: {result['output']}")
    except Exception as e:
        print(f"Error during PR review: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
