# AI Agent Code Reviewer (CodeRabbit Clone) 🤖🚀

This is an **agentic code reviewer** built with Python, LangChain, and Groq. It acts as an autonomous AI system that reads PRs, understands code changes, reasons about bugs, and interacts with developers.

## 🏗️ Architecture

- **Orchestrator**: LangChain Agent that plans and executes the review.
- **Diff Analyzer**: Extracts changes from GitHub PRs.
- **LLM Brain**: Groq (Llama 3.1) for high-performance reasoning.
- **Tool System**: Used by the agent to run static analysis (Semgrep), fetch context, and query a Knowledge Graph.

## ⚙️ Core Components

1.  **Agent Brain**: Uses `ChatGroq` for decision-making.
2.  **GitHub Interaction**: Uses `PyGithub` to fetch diffs and post comments.
3.  **Static Analysis**: Integrates `Semgrep` for security scans.
4.  **Context Knowledge**: A JSON-based Knowledge Graph for project-specific context.

## 🚀 How to Run locally

1.  **Clone the Repo**
2.  **Install dependencies**:
    ```bash
    pip install langchain langchain-groq PyGithub python-dotenv pydantic
    ```
3.  **Setup environment variables** in a `.env` file:
    ```env
    GITHUB_TOKEN=your_token
    GROQ_API_KEY=your_groq_key
    GITHUB_REPOSITORY=owner/repo
    PR_NUMBER=1
    ```
4.  **Run the orchestrator**:
    ```bash
    python main.py
    ```

## 🛠️ GitHub Actions Integration

Use this agent as a GitHub Action by adding the following to your workflow:

```yaml
- uses: iramsk02/agentic-code-reviewer@main
  with:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
    GROQ_API_KEY: ${{ secrets.GROQ_API_KEY }}
```

## 🧠 Reasoning & Iteration

Unlike a simple script, this agent:
1.  **Plans** its review strategy.
2.  **Executes tools** to gather more info.
3.  **Reasons** about the combined data.
4.  **Iterates** if further context is needed.
