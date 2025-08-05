import chromadb
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from tools import TOOLS
import os
import shutil

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5",
)
Settings.llm = None

class ToolMemory:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./tools_data")
        self.collection = self.client.get_or_create_collection("tools")

    def search(self, query: str):
        embeddings = Settings.embed_model.get_text_embedding(query)
        results = self.collection.query(embeddings, n_results=2)

        tool_data = []

        for i, tool_id in enumerate(results["ids"][0]):
            tool_info = {
                "name": tool_id,
                "args": results["metadatas"][0][i] # type: ignore
            }
            tool_data.append(tool_info)

        return {"tools": tool_data}

if __name__ == "__main__":
    if os.path.exists("./tools_data"):
        shutil.rmtree("./tools_data")
        
    memory = ToolMemory()
    
    for action in TOOLS:
        tool_id = action.name
        description = action.description
        metadatas = action.parameters if action.parameters != {} else None
        embeddings = Settings.embed_model.get_text_embedding(tool_id + description)

        print(f"adding {tool_id}")

        memory.collection.add(
            ids=[tool_id],
            embeddings=[embeddings],
            metadatas=[metadatas], # type: ignore
        )

    print(f"Memory initialized with {len(TOOLS)} tools.")
