from typing import List
from langchain_google_genai import ChatGoogleGenerativeAI
from config import settings

class LLMService:
    def __init__(self):
        try:
            self.chat_model = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash",
                google_api_key=settings.GOOGLE_API_KEY,
                convert_system_message_to_human=True 
            )
            print("LLMService Initialized with Google Gemini Pro chat model.")
        except Exception as e:
            print(f"Failed to initialize Google chat model: {e}")
            self.chat_model = None

    def _transform_query(self, query: str) -> str:
        if not self.chat_model:
            return query
            
        prompt = f"""
        You are an expert at rewriting user questions into optimal queries for a semantic vector database search.

        Analyze the following user question. Follow these rules:
        1.  If the question is already specific, contains key terms, and is well-suited for a vector search (like asking for a specific definition, number, or clause), return the original question without any changes.
        2.  If the question is conversational, vague, or a yes/no question, rewrite it as a concise, keyword-focused statement that describes the core information needed.
        3.  Do not answer the question. Only return the original or the rewritten search query.

        User question: "{query}"

        Optimal search query:
        """
        try:
            response = self.chat_model.invoke(prompt)
            transformed_query = response.content.strip().strip('"') 
            print(f"Original Query: '{query}' | Transformed Query: '{transformed_query}'")
            return transformed_query
        except Exception as e:
            print(f"Could not transform query due to error: {e}. Using original query.")
            return query

    def generate_response(self, query: str, context_clauses: List[str]) -> str:
        if not self.chat_model:
            return "Error: Google chat model is not initialized."
        
        context_str = "\n\n".join(context_clauses)
        
        prompt = f"""
        You are a highly intelligent insurance policy analysis assistant. Your task is to answer the user's question based ONLY on the provided context clauses from the policy document.

        Follow these rules strictly:
        1.  Synthesize the information from all provided context clauses into a single, coherent answer.
        2.  Do not repeat information. If multiple clauses mention the same point, present it only once.
        3.  Do not use any external knowledge.
        4.  Your answer must be concise and directly address the user's question.
        5.  If the answer is not present in any of the provided context clauses, you MUST state: 'Based on the provided context, the answer to this question is not available.'

        CONTEXT CLAUSES:
        ---
        {context_str}
        ---
        
        QUESTION:
        {query}
        
        ANSWER:
        """

        print("--- Sending prompt to Google Gemini API ---")
        try:
            response = self.chat_model.invoke(prompt)
            answer = response.content
            print("--- Received response from Google Gemini ---")
            return answer.strip()

        except Exception as e:
            print(f"An error occurred while calling the Google Gemini API: {e}")
            return "Error: Could not generate a response from the Gemini model."

llm_service = LLMService()