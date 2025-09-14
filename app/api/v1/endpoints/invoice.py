from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.invoice_parser import extract_invoice_data
from app.models.invoice_models import StructuredInvoice
import shutil
import os
import tempfile
from loguru import logger

router = APIRouter(prefix="/invoices", tags=["invoices"])

@router.get("/health")
async def health_check():
    """Check the health of the invoice API."""
    return {"message": "API is healthy"}

@router.post("/extract", response_model=StructuredInvoice)
async def extract_from_invoice(file: UploadFile = File(...)):
    """
    Accepts an invoice file (JPEG, PDF, etc.) and returns the extracted structured data.
    
    Args:
        file (UploadFile): The uploaded invoice file.
    
    Returns:
        StructuredInvoice: The extracted invoice data.
    
    Raises:
        HTTPException: If the file is invalid or extraction fails.
    """
    # Validate file extension
    valid_extensions = {'.pdf', '.jpg', '.jpeg', '.png', '.tiff', '.tif'}
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in valid_extensions:
        logger.error(f"Invalid file extension: {file_ext}")
        raise HTTPException(status_code=400, detail="Unsupported file format. Use PDF, JPG, JPEG, PNG, TIFF, or TIF.")

    # Use a temporary file to store the uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as temp_file:
        temp_file_path = temp_file.name
        try:
            # Save the uploaded file to the temporary location
            shutil.copyfileobj(file.file, temp_file)

            # Extract data from the invoice
            extracted_data = extract_invoice_data(temp_file_path)
            return extracted_data

        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Failed to process invoice: {str(e)}")
        
        finally:
            # Clean up the temporary file
            try:
                os.unlink(temp_file_path)
            except Exception as e:
                logger.warning(f"Failed to delete temporary file {temp_file_path}: {str(e)}")