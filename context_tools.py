import json
import os

class KnowledgeGraphTools:
    def __init__(self, kg_path="knowledge_graph.json"):
        self.kg_path = kg_path
        self.kg = self._load_kg()

    def _load_kg(self) -> dict:
        """Loads the knowledge graph from a JSON file."""
        if os.path.exists(self.kg_path):
            with open(self.kg_path, "r") as f:
                return json.load(f)
        return {"classes": [], "methods": [], "dependencies": []}

    def query_kg(self, query: str) -> str:
        """Query the knowledge graph for architectural context."""
        # Simple string-based query logic for now
        # In a real implementation, this would use semantic search or advanced retrieval
        results = [str(item) for item in list(self.kg.values()) if query.lower() in str(item).lower()]
        return "\n".join(results) if results else "No knowledge found for the query."

    def add_knowledge(self, category: str, data: dict):
        """Add new knowledge context to the graph."""
        if category not in self.kg:
            self.kg[category] = []
        self.kg[category].append(data)
        with open(self.kg_path, "w") as f:
            json.dump(self.kg, f, indent=4)
        return "Knowledge added successfully."
