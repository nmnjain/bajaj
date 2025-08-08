from typing import List
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from config import settings

class VectorStoreService:
    def __init__(self):
        try:
            self.embeddings_model = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001", 
                google_api_key=settings.GOOGLE_API_KEY
            )
            print("VectorStoreService Initialized with GoogleGenerativeAIEmbeddings")
        except Exception as e:
            print(f"Failed to initialize Google embeddings model: {e}")
            self.embeddings_model = None

        self.vector_store = None

    def create_store_from_chunks(self, chunks: List[str]):
        if not self.embeddings_model:
            print("Error: Embeddings model is not available.")
            return

        if not chunks:
            print("No chunks provided to create vector store.")
            return
            
        print(f"Creating vector store from {len(chunks)} text chunks using Google's model...")
        try:
            self.vector_store = FAISS.from_texts(texts=chunks, embedding=self.embeddings_model)
            print("Vector store created successfully.")
        except Exception as e:
            print(f"An error occurred during vector store creation: {e}")
            self.vector_store = None
            raise

    def search_relevant_clauses(self, query: str) -> List[str]:
        if not self.vector_store:
            print("Error: Vector store is not available. Cannot perform search.")
            return ["Error: Vector store was not created. Please process a document first."]

        print(f"Performing vector search for query: '{query}'")
        retrieved_docs = self.vector_store.similarity_search(query, k=5)
        retrieved_chunks = [doc.page_content for doc in retrieved_docs]
        
        print(f"Found {len(retrieved_chunks)} relevant chunks.")
        return retrieved_chunks

vector_store_service = VectorStoreService()