# Document Text Extractor with Ollama

This FastAPI application accepts document uploads and uses Ollama to extract text from them, returning the content in JSON format with each page's content separated.

## Prerequisites

1. Python 3.8 or higher
2. Ollama installed and running locally (or accessible via network)
3. A suitable LLM model loaded in Ollama that can handle documents and generate structured output (like llama3)

## Setup Instructions

1. Clone this repository:
```bash
git clone <repository-url>
cd ollama-doc-extractor
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

4. Make sure Ollama is running and has a suitable model:
```bash
ollama run llama3  # Or your preferred model
```

## Running the Application

Start the FastAPI server:
```bash
uvicorn app:app --reload
```

The API will be available at http://localhost:8000

## Using the API

1. Send a POST request to `/extract/` with your document as form data:

Using curl:
```bash
curl -X 'POST' \
  'http://localhost:8000/extract/' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@/path/to/your/document.pdf' \
  -F 'model=llama3'
```

2. The response will be JSON with each page's content:
```json
{
  "pages": [
    {"page_number": 1, "content": "text content of page 1"},
    {"page_number": 2, "content": "text content of page 2"}
  ]
}
```

## API Documentation

Once the server is running, you can access the automatic API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Edit the `app.py` file to change:
- `OLLAMA_API_URL`: The URL of your Ollama API (default: http://localhost:11434/api/generate)
- `DEFAULT_MODEL`: The default Ollama model to use (default: llama3)

## Notes

- The application temporarily saves uploaded files to process them
- Large documents may take significant time to process
- Different Ollama models may provide different quality of text extraction