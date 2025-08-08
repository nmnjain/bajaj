

from typing import List, Dict, Any
from .llm_service import llm_service
from .vector_store import vector_store_service

class QueryProcessorService:
    def process_questions(self, questions: List[str]) -> List[str]:
        all_answers = []
        for question in questions:
            print(f"--- Starting processing for question: '{question}' ---")
            search_query = llm_service._transform_query(question)
            relevant_clauses = vector_store_service.search_relevant_clauses(search_query)
            answer = llm_service.generate_response(question, relevant_clauses)
            all_answers.append(answer)
        
        return all_answers

query_processor_service = QueryProcessorService()