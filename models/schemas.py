
from pydantic import BaseModel, Field
from typing import List, Any



class HackRxRequest(BaseModel):

    documents: str = Field(
        ..., 
        description="Publicly accessible URL of the document to be processed.",
        example="https://some-public-url.com/policy.pdf"
    )
    questions: List[str] = Field(
        ..., 
        description="A list of natural language questions to be answered based on the document.",
        example=["What is the grace period for premium payment?"]
    )

# --- Response Model ---

class HackRxResponse(BaseModel):
    
    answers: List[Any] = Field(
        ..., 
        description="A list of detailed answers for each question."
    )