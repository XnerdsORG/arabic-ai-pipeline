from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import tempfile
import os
import fitz  # PyMuPDF
import uvicorn
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging
import re

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

print("Starting application initialization...")
# Initialize FastAPI app
app = FastAPI(
    title="PDF Text Extractor API",
    description="API to extract text from PDF documents with RTL support",
    version="1.1.0"
)
print("FastAPI app initialized successfully")

class TextExtractionResponse(BaseModel):
    status: str
    filename: str
    page_count: int
    text_by_page: Dict[int, str]
    complete_text: str
    text_direction: str = "ltr"  # Default to left-to-right
    language: Optional[str] = None

def detect_arabic_text(text: str) -> bool:
    """
    Detect if text contains Arabic characters.
    Returns True if Arabic characters are found.
    """
    print(f"Checking for Arabic text in string of length {len(text)}")
    # Arabic Unicode block range
    arabic_pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]')
    result = bool(arabic_pattern.search(text))
    print(f"Arabic text detected: {result}")
    return result

@app.get("/")
async def root():
    print("Root endpoint accessed")
    logger.info("Root endpoint accessed")
    return {"message": "PDF Text Extractor API with RTL Support. Use /extract-text endpoint to upload and process PDFs."}

@app.post("/extract-text", response_model=TextExtractionResponse)
async def extract_text(file: UploadFile = File(...)):
    """
    Extract text from a PDF file uploaded via form data.
    
    - **file**: The PDF file to process
    
    Returns the extracted text organized by page number with RTL metadata
    """
    print(f"==== EXTRACT TEXT ENDPOINT CALLED ====")
    print(f"Received file upload: {file.filename}")
    logger.info(f"Received file upload: {file.filename}")
    
    # Check if the uploaded file is a PDF
    if not file.filename.lower().endswith('.pdf'):
        print(f"ERROR: Invalid file format: {file.filename}")
        logger.error(f"Invalid file format: {file.filename}")
        raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")
    
    print(f"File format validated as PDF: {file.filename}")
    logger.info("File format validated as PDF")
    
    # Create a temporary file to save the uploaded PDF
    print("Creating temporary file for PDF storage")
    logger.info("Creating temporary file")
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        # Write the uploaded file content to the temporary file
        print("Reading content from uploaded file")
        content = await file.read()
        print(f"Read {len(content)} bytes from uploaded file")
        logger.info(f"Read {len(content)} bytes from uploaded file")
        
        print("Writing content to temporary file")
        temp_file.write(content)
        temp_file_path = temp_file.name
        print(f"Saved to temporary file: {temp_file_path}")
        logger.info(f"Saved to temporary file: {temp_file_path}")
    
    try:
        # Open the PDF with PyMuPDF
        print("Opening PDF with PyMuPDF")
        logger.info("Opening PDF with PyMuPDF")
        doc = fitz.open(temp_file_path)
        print(f"PDF opened successfully. Total pages: {len(doc)}")
        logger.info(f"PDF opened successfully. Pages: {len(doc)}")
        
        # Extract text from each page
        text_by_page = {}
        complete_text = ""
        contains_arabic = False
        
        print("Starting text extraction from pages")
        logger.info("Starting text extraction from pages")
        for page_num, page in enumerate(doc):
            print(f"Processing page {page_num+1}/{len(doc)}")
            logger.info(f"Processing page {page_num+1}/{len(doc)}")
            text = page.get_text()
            print(f"Extracted text from page {page_num+1} (length: {len(text)} characters)")
            
            # Check if the text contains Arabic
            if detect_arabic_text(text):
                contains_arabic = True
                print(f"Arabic text detected on page {page_num+1}")
                logger.info(f"Arabic text detected on page {page_num+1}")
            
            text_by_page[page_num] = text
            complete_text += text + "\n\n"
            print(f"Added page {page_num+1} text to results dictionary")
            logger.info(f"Extracted {len(text)} characters from page {page_num+1}")
        
        # Clean up
        print("Text extraction complete, closing PDF document")
        logger.info("Closing PDF document")
        doc.close()
        
        # Determine text direction and language
        text_direction = "rtl" if contains_arabic else "ltr"
        language = "ar" if contains_arabic else None
        
        print(f"Text direction determined: {text_direction}")
        print(f"Language identified: {language}")
        logger.info(f"Text extraction completed successfully. Text direction: {text_direction}")
        
        # Return the response with RTL metadata
        print("Preparing API response")
        response = TextExtractionResponse(
            status="success",
            filename=file.filename,
            page_count=len(text_by_page),
            text_by_page=text_by_page,
            complete_text=complete_text,
            text_direction=text_direction,
            language=language
        )
        print("API response ready, returning data")
        return response
        
    except Exception as e:
        print(f"ERROR processing PDF: {str(e)}")
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")
    
    finally:
        # Clean up the temporary file
        print(f"Cleaning up temporary file: {temp_file_path}")
        logger.info(f"Cleaning up temporary file: {temp_file_path}")
        try:
            os.unlink(temp_file_path)
            print("Temporary file deleted successfully")
            logger.info("Temporary file deleted")
        except Exception as e:
            print(f"ERROR: Failed to delete temporary file: {str(e)}")
            logger.error(f"Failed to delete temporary file: {str(e)}")

# Optional: For running the app directly with Python
if __name__ == "__main__":
    print("===== STARTING PDF TEXT EXTRACTOR API SERVER =====")
    logger.info("Starting PDF Text Extractor API server with RTL support")
    print("Server will be available at http://0.0.0.0:8000")
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)