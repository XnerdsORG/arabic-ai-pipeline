# PDF Text Extractor API

A FastAPI application that extracts text from PDF files uploaded via API form data.

## Features

- Extract text from PDF documents
- Returns text organized by page number
- Returns complete text as a single string
- Interactive API documentation with Swagger UI

## Installation

1. Clone the repository or download the source code and start the virtual env

```bash
python -m venv venv

source venv/bin/activate
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Starting the server

Run the following command to start the server:

```bash
uvicorn app:app --reload
```

The server will start at `http://127.0.0.1:8000`

### API Endpoints

#### 1. GET `/`

A simple welcome endpoint to verify the API is running.

#### 2. POST `/extract-text`

Upload a PDF file to extract text.

**Request:**
- Form data with a file field named `file`

**Response:**
```json
{
  "status": "success",
  "filename": "example.pdf",
  "page_count": 3,
  "text_by_page": {
    "0": "Text from page 1...",
    "1": "Text from page 2...",
    "2": "Text from page 3..."
  },
  "complete_text": "Full text of the document..."
}
```

### Swagger Documentation

The API includes built-in documentation available at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Example API Usage

### Using curl:

```bash
curl -X POST -F "file=@your_document.pdf" http://127.0.0.1:8000/extract-text
```

### Using Python requests:

```python
import requests

url = "http://127.0.0.1:8000/extract-text"
files = {"file": open("your_document.pdf", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

## Error Handling

The API includes error handling for:
- Non-PDF file uploads
- PDF processing errors
- Server issues

## Dependencies

- FastAPI: Web framework
- PyMuPDF: PDF processing library
- Uvicorn: ASGI server
- Python-multipart: For form data processing
- Pydantic: Data validation