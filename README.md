# PDF Text Extractor API with RTL Support

This FastAPI application accepts PDF uploads and extracts text from them, returning the content in JSON format with each page's content separated. It has special support for detecting and handling right-to-left (RTL) text like Arabic.

## Features

- Extract text from PDF documents
- Automatically detect Arabic text and provide RTL metadata
- Return both page-by-page text and complete document text
- Simple REST API interface

## Prerequisites

1. Python 3.8 or higher
2. Dependencies listed in requirements.txt (FastAPI, PyMuPDF, etc.)

## Setup Instructions

1. Clone this repository:
```bash
git clone <repository-url>
cd pdf-text-extractor
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app:app --reload
```

Or run the application directly:
```bash
python app.py
```

The API will be available at http://localhost:8000

## Using the API

1. Send a POST request to `/extract-text/` with your PDF as form data:

Using curl:
```bash
curl -X 'POST' \
  'http://localhost:8000/extract-text' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/document.pdf'
```

2. The response will be JSON with the following structure:
```json
{
  "status": "success",
  "filename": "example.pdf",
  "page_count": 2,
  "text_by_page": {
    "0": "content of page 1",
    "1": "content of page 2"
  },
  "complete_text": "content of page 1\n\ncontent of page 2\n\n",
  "text_direction": "ltr",
  "language": null
}
```

If Arabic text is detected, the response will include:
- `text_direction`: "rtl"
- `language`: "ar"

## API Documentation

Once the server is running, you can access the automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Notes

- The application temporarily saves uploaded files to process them
- PDF files are processed using PyMuPDF (fitz)
- The application automatically detects Arabic text and includes RTL metadata