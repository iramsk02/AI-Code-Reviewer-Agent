import os
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from github_tools import GitHubTools
from static_tools import StaticAnalysisTools
from context_tools import KnowledgeGraphTools
from langchain.tools import Tool, StructuredTool
from pydantic import BaseModel, Field

class InlineComment(BaseModel):
    body: str = Field(description="Markdown body of the comment")
    commit_id: str = Field(description="SHA of the commit to comment on")
    path: str = Field(description="Relative path of the file being reviewed")
    line: int = Field(description="Line number where the comment is relevant")

class ReviewAgent:
    def __init__(self, github_token, repo_name, workspace_path, pr_number, kg_path="knowledge_graph.json"):
        self.github_tools = GitHubTools(github_token, repo_name)
        self.static_tools = StaticAnalysisTools(workspace_path)
        self.kg_tools = KnowledgeGraphTools(kg_path)
        self.pr_number = pr_number
        self.llm = ChatGroq(model="llama-3.3-70b-versatile", groq_api_key=os.getenv("GROQ_API_KEY"))
        self.agent_executor = self._create_agent()

    def _create_agent(self):
        # Define the tools the agent can use
        tools = [
            StructuredTool.from_function(
                name="run_static_scan",
                func=self.static_tools.run_semgrep_scan,
                description="Runs a security scan using Semgrep on the specified path or file. Useful for finding vulnerabilities."
            ),
            StructuredTool.from_function(
                name="get_file_context",
                func=self.github_tools.get_file_content,
                description="Fetches the full content of a specified file. Use this when the diff context is insufficient to understand the change."
            ),
            StructuredTool.from_function(
                name="query_knowledge_graph",
                func=self.kg_tools.query_kg,
                description="Queries the project's knowledge graph for architectural context or specific domain knowledge. Use this to understand code dependencies or core concepts."
            ),
            StructuredTool.from_function(
                name="post_pr_comment",
                func=lambda body: self.github_tools.post_pr_comment(self.pr_number, body),
                description="Posts a high-level summary review as a comment on the PR. Provide a summary of all findings here."
            ),
            StructuredTool.from_function(
                name="post_inline_comment",
                func=lambda **kwargs: self.github_tools.post_inline_comment(pr_number=self.pr_number, **kwargs),
                description="Posts a specific inline comment on a file at a specific line. Use this to report specific bugs or suggestions on a line.",
                args_schema=InlineComment
            )
        ]

        # Define the system prompt for our agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a highly intelligent Code Reviewer Agent, similar to CodeRabbit.
Your goal is to analyze pull requests, detect bugs, security issues, and suggest improvements.
You have access to tools that can run static analysis and fetch additional code context.

When reviewing a PR, follow these steps:
1. Understand the PR's intent and scope by looking at the diff.
2. If the changes are complex, use 'get_file_context' to see the full implementation.
3. Use 'run_static_scan' to catch security vulnerabilities and common bugs.
4. Reason about issues and provide constructive feedback.
5. Post your comments on the PR, either as a general summary or as inline comments for specific lines.

When reporting an issue, follow this format:
```md
⚠️ Issue: [Brief Name]
📁 File: [Filename] (line [Number])

Problem:
[Detailed description of the bug or security risk]

Fix:
[Specific code snippet or suggestion to fix it]
```

Be professional, concise, and helpful. Avoid over-commenting on minor style issues; focus on correctness, security, and maintainability."""),
            ("human", "{input}"),
            ("placeholder", "{agent_scratchpad}")
        ])

        # Create the agent
        agent = create_tool_calling_agent(self.llm, tools, prompt)
        return AgentExecutor(agent=agent, tools=tools, verbose=True)

    def run_review(self):
        # Fetch the diff to start the review
        diff = self.github_tools.get_pr_diff(self.pr_number)
        
        # We start the agent workflow by providing the diff and asking for a review
        agent_input = f"Analyze the following PR diff (PR #{self.pr_number}) and provide a comprehensive review. Use tools if necessary.\n\nDiff:\n{diff}"
        
        return self.agent_executor.invoke({"input": agent_input})
