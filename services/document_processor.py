import requests
import fitz  
from docx import Document
import io
from typing import Tuple, List 
import os
from langchain.text_splitter import RecursiveCharacterTextSplitter 

class DocumentProcessor:

    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True, 
        separators=["\n\n", "\n", " ", ""] 
)

    def chunk_text(self, text: str) -> List[str]:
        
        print("Chunking document text...")
        chunks = self.text_splitter.split_text(text)
        print(f"Successfully created {len(chunks)} chunks.")
        return chunks

    def process_document_from_path(self, path: str) -> str:
        
        try:
            if not os.path.exists(path):
                raise FileNotFoundError(f"No file found at the specified path: {path}")

            print(f"Processing local file: {path}")
            _, file_extension = os.path.splitext(path)
            file_type = file_extension.lower().strip('.')

            with open(path, 'rb') as f:
                content = f.read()

            if file_type == 'pdf':
                text = self._extract_text_from_pdf(content)
            elif file_type == 'docx':
                text = self._extract_text_from_docx(content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            print("Text extraction from local file successful.")
            return text

        except FileNotFoundError as e:
            print(f"Error: {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during local document processing: {e}")
            raise

    def process_document_from_url(self, url: str) -> str:
        
        try:
            print(f"Starting download from URL: {url}")
            content, file_type = self._download_document(url)
            print(f"Download complete. Detected file type: {file_type}")

            if file_type == 'pdf':
                text = self._extract_text_from_pdf(content)
            elif file_type == 'docx':
                text = self._extract_text_from_docx(content)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")
            
            print("Text extraction successful.")
            return text

        except requests.exceptions.RequestException as e:
            print(f"Error: Failed to download document. {e}")
            raise
        except Exception as e:
            print(f"An unexpected error occurred during document processing: {e}")
            raise

    def _download_document(self, url: str) -> Tuple[bytes, str]:
        headers = {'User-Agent': 'Mozilla/5.0'} 
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()  

        content_type = response.headers.get('content-type', '').lower()
        
        file_type = None
        if 'pdf' in content_type or url.lower().endswith('.pdf'):
            file_type = 'pdf'
        elif 'openxmlformats-officedocument.wordprocessingml.document' in content_type or url.lower().endswith('.docx'):
            file_type = 'docx'
            
        if not file_type:
            raise ValueError("Could not determine document type from URL or content-type header.")

        return response.content, file_type

    def _extract_text_from_pdf(self, content: bytes) -> str:
        
        text = ""
        with fitz.open(stream=content, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text

    def _extract_text_from_docx(self, content: bytes) -> str:
        
        text = ""
        doc_stream = io.BytesIO(content)
        doc = Document(doc_stream)
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text

document_processor_service = DocumentProcessor()