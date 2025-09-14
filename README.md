# Invoice Extractor

An AI-powered invoice extraction tool that automates invoice processing from PDF and image files using FastAPI and Docling.

## Features

- Extracts structured invoice data (vendor, customer, line items, totals) from PDF and image files.
- REST API endpoints for health check and invoice extraction.
- Uses [Docling](https://pypi.org/project/docling/) for document parsing.
- Pydantic models for robust data validation.
- Supports PDF, JPG, JPEG, PNG, TIFF, and TIF formats.

---

## Setup Instructions


1. **Create and activate a virtual environment**
   ```sh
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Run the project using Uvicorn**
   ```sh
   uvicorn app.main:app --reload
   ```

   The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## Usage Examples

### Health Check

- **Endpoint:** `GET /api/v1/invoice/invoices/health`
- **Response:**
  ```json
  { "message": "API is healthy" }
  ```

### Extract Invoice Data

- **Endpoint:** `POST /api/v1/invoice/invoices/extract`
- **Request:** `multipart/form-data` with a file field named `file` (PDF or image)
- **Response:** JSON with structured invoice data.

**Example using `curl`:**
```sh
curl -X POST "http://127.0.0.1:8000/api/v1/invoice/invoices/extract" \
  -F "file=@data/sample-invoice.pdf"
```

---

## Architecture Overview

```
app/
├── main.py                  # FastAPI app setup and middleware
├── api/
│   └── v1/
│       └── endpoints/
│           └── invoice.py  # API endpoints for invoice extraction
├── models/
│   └── invoice_models.py    # Pydantic models for invoice structure
├── services/
│   └── invoice_parser.py    # Logic for extracting invoice data using Docling
```

- **[app/main.py](app/main.py):** Initializes FastAPI, sets up CORS, and includes routers.
- **[app/api/v1/endpoints/invoice.py](app/api/v1/endpoints/invoice.py):** Defines API endpoints for invoice extraction.
- **[app/models/invoice_models.py](app/models/invoice_models.py):** Contains Pydantic models for structured invoice data.
- **[app/services/invoice_parser.py](app/services/invoice_parser.py):** Handles the extraction logic using Docling.

---
