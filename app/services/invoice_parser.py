from loguru import logger
from fastapi import HTTPException
from docling.document_extractor import DocumentExtractor
from docling.datamodel.base_models import InputFormat

from app.models.invoice_models import StructuredInvoice


def extract_invoice_data(file_path: str) -> StructuredInvoice:
    """
    Extracts structured data from an invoice document (PDF or image).
    
    Args:
        file_path (str): Path to the invoice file.
    
    Returns:
        StructuredInvoice: The extracted invoice data as a Pydantic model.
    
    Raises:
        HTTPException: If extraction fails or no data is found.
    """
    try:
        # Initialize the extractor
        extractor = DocumentExtractor(allowed_formats=[InputFormat.IMAGE, InputFormat.PDF])

        # Extract data from the document
        result = extractor.extract(
            source=file_path,
            template=StructuredInvoice,
        )

        logger.info(f"Extraction result: {result}")

        # Check if there are any pages and extracted data
        if not result.pages or not result.pages[0].extracted_data:
            logger.error("No data extracted from the invoice.")
            raise HTTPException(status_code=404, detail="Could not extract data from the invoice.")

        # Validate and return the extracted data as a StructuredInvoice object
        invoice = StructuredInvoice.model_validate(result.pages[0].extracted_data)
        logger.success(f"Successfully extracted invoice data: {invoice}")
        return invoice

    except Exception as e:
        logger.error(f"Error during invoice extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Extraction failed: {str(e)}")
