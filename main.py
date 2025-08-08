
import fastapi
from fastapi import Security, HTTPException, Depends
from fastapi.security import APIKeyHeader

from models.schemas import HackRxRequest, HackRxResponse
from services.query_processor import query_processor_service
from config import settings
from services.document_processor import document_processor_service
from services.vector_store import vector_store_service 

# Initialize FastAPI application
app = fastapi.FastAPI(
    title="HackRx 6.0 LLM Query System",
    description="API to process insurance/legal documents and answer natural language queries.",
    version="1.0.0"
)

# --- Authentication Setup ---
API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)

async def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    """
    Dependency function to validate the team token from the 'Authorization' header.
    It expects the header in the format 'Bearer <token>'.
    """
    if not api_key_header:
        raise HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header is missing",
        )

    parts = api_key_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization scheme. Expected 'Bearer <token>'",
        )

    token = parts[1]
    if token != settings.TEAM_TOKEN:
        raise HTTPException(
            status_code=fastapi.status.HTTP_403_FORBIDDEN,
            detail="Invalid or expired Team Token",
        )
    return token

# --- API Endpoints ---

@app.get("/", tags=["Health Check"])
async def health_check():
    """A simple endpoint to confirm the server is running."""
    return {"status": "ok", "message": "Welcome to the HackRx 6.0 API!"}


@app.post(
    "/api/v1/hackrx/run",
    response_model=HackRxResponse,
    tags=["Core Logic"],
    summary="Process a document and answer questions"
)
async def run_query(
    request: HackRxRequest,
    api_key: str = Depends(get_api_key)
):
    print(f"Received request for document URL: {request.documents}")
    
    try:
        extracted_text = document_processor_service.process_document_from_url(request.documents)
        
        text_chunks = document_processor_service.chunk_text(extracted_text)

        vector_store_service.create_store_from_chunks(text_chunks)

    except Exception as e:
        raise HTTPException(
            status_code=fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed during document processing pipeline: {e}"
        )

    generated_answers = query_processor_service.process_questions(request.questions)
    
    return HackRxResponse(answers=generated_answers)