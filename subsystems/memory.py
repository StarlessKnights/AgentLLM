from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import uuid

Settings.embed_model = HuggingFaceEmbedding(
    model_name="BAAI/bge-small-en-v1.5"
)

class Memory:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Memory, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized') or not self._initialized:
            try:
                self.documents = SimpleDirectoryReader('memory').load_data()
                self.index = VectorStoreIndex.from_documents(self.documents)
                self.retriever = self.index.as_retriever()
            except Exception as e:
                print(f"Error initializing memory: {e}")
                self.documents = []
                self.index = None
                self.retriever = None
            self._initialized = True
            
            print("\033[92mMemory initialized successfully\033[0m")
        
    def query(self, query):
        if self.index is None or self.retriever is None:
            return "Memory empty."
        nodes = self.retriever.retrieve(query)
        context_str = "\n\n".join([n.get_text() for n in nodes])
        return context_str
    
    def add(self, text):
        with open(f'memory/{uuid.uuid4()}.txt', 'w') as f:
            f.write(text)
            f.flush()
            f.close()
            
        self.documents = SimpleDirectoryReader('memory').load_data()
        self.index = VectorStoreIndex.from_documents(self.documents)
        self.retriever = self.index.as_retriever()