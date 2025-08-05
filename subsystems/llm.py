import openai
from openai.types.chat import ChatCompletion
import time
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

Settings.llm = None

class LLM:
    def __init__(self):
        self.llm = openai.OpenAI(
            api_key="eve",
            base_url="http://localhost:8080"
        )
       
        print("\033[92mLLM initialized successfully\033[0m")

    def generate(self, messages, streaming=False, tools=None):
        response: ChatCompletion = self.llm.chat.completions.create(
            model="gemini-2.5-flash-preview-04-17",
            messages=messages,
            stream=streaming,
            tools=tools,
            temperature=0.2,
            tool_choice="auto",
        )
        return response

    def manual_stream(self, text, chunk_size=5, delay=0.05):
            for i in range(0, len(text), chunk_size):
                yield text[i : i + chunk_size]
                time.sleep(delay)