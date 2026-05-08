from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from config import OPENAI_API_KEY
from langchain_community.retrievers import BM25Retriever
from langchain_classic.retrievers import EnsembleRetriever


class RetrieverBuilder:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(api_key=OPENAI_API_KEY)
        
    def build_hybrid_retriever(self, docs):
        """Build a hybrid retriever using BM25 and vector-based retrieval."""
        try:
            # Create Chroma vector store
            vector_store = Chroma.from_documents(
                documents=docs,
                embedding=self.embeddings
            )
            # Create BM25 retriever
            bm25 = BM25Retriever.from_documents(docs)
            
            # Create vector-based retriever
            vector_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
            
            # Combine retrievers into a hybrid retriever
            hybrid_retriever = EnsembleRetriever(
                retrievers=[bm25, vector_retriever]
            )
            return hybrid_retriever
        except Exception as e:
            print(f"Failed to build hybrid retriever: {e}")
            raise
