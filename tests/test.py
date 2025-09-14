# # from IPython import display
# # from pydantic import BaseModel, Field
# # from rich import print
# # from typing import Optional

# # from docling.datamodel.base_models import InputFormat
# # from docling.document_extractor import DocumentExtractor


# # file_path = (
# #     "https://upload.wikimedia.org/wikipedia/commons/9/9f/Swiss_QR-Bill_example.jpg"
# # )
# # display.HTML(f"")



# # extractor = DocumentExtractor(allowed_formats=[InputFormat.IMAGE, InputFormat.PDF])



# # class Invoice(BaseModel):
# #     bill_no: str = Field(
# #         examples=["A123", "5414"]
# #     )
# #     total: float = Field(
# #         default=10, examples=[20]
# #     )
# #     tax_id: Optional[str] = Field(default=None, examples=["1234567890"])


# # result = extractor.extract(
# #     source=file_path,
# #     template=Invoice,
# # )
# # print(result.pages)



# # class Contact(BaseModel):
# #     name: Optional[str] = Field(default=None, examples=["Smith"])
# #     address: str = Field(default="123 Main St", examples=["456 Elm St"])
# #     postal_code: str = Field(default="12345", examples=["67890"])
# #     city: str = Field(default="Anytown", examples=["Othertown"])
# #     country: Optional[str] = Field(default=None, examples=["Canada"])


# # class ExtendedInvoice(BaseModel):
# #     bill_no: str = Field(
# #         examples=["A123", "5414"]
# #     )
# #     total: float = Field(
# #         default=10, examples=[20]
# #     ) 
# #     garden_work_hours: int = Field(default=1, examples=[2])
# #     sender: Contact = Field(default=Contact(), examples=[Contact()])
# #     receiver: Contact = Field(default=Contact(), examples=[Contact()])



# # result = extractor.extract(
# #     source=file_path,
# #     template=ExtendedInvoice,
# # )
# # print(result.pages)


# # invoice = ExtendedInvoice.model_validate(result.pages[0].extracted_data)
# # print(invoice)
# from typing import List, Optional, Dict, Any
# from datetime import date
# from pydantic import BaseModel, Field
# from docling.datamodel.base_models import InputFormat
# from docling.document_extractor import DocumentExtractor
# import json

# # Define Pydantic models for structured data extraction
# TRANSFORMERS_VERBOSITY="info"

# class VendorInfo(BaseModel):
#     """Vendor/Company information from the invoice"""
#     company_name: Optional[str] = Field(
#         default=None, 
#         examples=["ABC Corp", "XYZ Industries", "Smith & Associates"]
#     )
#     address: Optional[str] = Field(
#         default=None, 
#         examples=["123 Main St, City, State 12345", "456 Business Ave, Suite 100"]
#     )
#     phone: Optional[str] = Field(
#         default=None, 
#         examples=["+1-555-123-4567", "(555) 987-6543", "555.123.4567"]
#     )
#     email: Optional[str] = Field(
#         default=None, 
#         examples=["billing@company.com", "info@business.com"]
#     )
#     tax_id: Optional[str] = Field(
#         default=None, 
#         examples=["12-3456789", "EIN: 98-7654321", "TAX-ID-123456"]
#     )

# class InvoiceDetails(BaseModel):
#     """Invoice header details"""
#     invoice_number: Optional[str] = Field(
#         default=None, 
#         examples=["INV-001", "2024-0123", "A-4567"]
#     )
#     date: Optional[str] = Field(
#         default=None, 
#         examples=["2024-01-15", "01/15/2024", "January 15, 2024"],
#         description="Invoice date in YYYY-MM-DD format"
#     )
#     due_date: Optional[str] = Field(
#         default=None, 
#         examples=["2024-02-15", "02/15/2024", "February 15, 2024"],
#         description="Due date in YYYY-MM-DD format"
#     )
#     currency: Optional[str] = Field(
#         default="USD", 
#         examples=["USD", "EUR", "GBP", "$", "€"]
#     )

# class CustomerInfo(BaseModel):
#     """Customer/Bill-to information"""
#     name: Optional[str] = Field(
#         default=None, 
#         examples=["John Doe", "Acme Corporation", "Jane Smith LLC"]
#     )
#     address: Optional[str] = Field(
#         default=None, 
#         examples=["789 Customer St, City, State 54321", "Customer Address Line"]
#     )
#     customer_id: Optional[str] = Field(
#         default=None, 
#         examples=["CUST-001", "C123456", "ID-789"]
#     )

# class LineItem(BaseModel):
#     """Individual line item on the invoice"""
#     description: Optional[str] = Field(
#         default=None, 
#         examples=["Professional Services", "Widget A", "Consulting Hours"]
#     )
#     quantity: Optional[float] = Field(
#         default=None, 
#         examples=[1.0, 10.5, 2.0]
#     )
#     unit_price: Optional[float] = Field(
#         default=None, 
#         examples=[100.00, 25.50, 1500.00]
#     )
#     total: Optional[float] = Field(
#         default=None, 
#         examples=[100.00, 267.25, 3000.00]
#     )

# class Totals(BaseModel):
#     """Invoice totals and calculations"""
#     subtotal: Optional[float] = Field(
#         default=None, 
#         examples=[1000.00, 2500.50, 500.00]
#     )
#     tax_amount: Optional[float] = Field(
#         default=None, 
#         examples=[80.00, 200.04, 40.00]
#     )
#     total_amount: Optional[float] = Field(
#         default=None, 
#         examples=[1080.00, 2700.54, 540.00]
#     )

# class FieldConfidence(BaseModel):
#     """Confidence scores for specific field groups"""
#     vendor_info: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.95, 0.87, 0.92]
#     )
#     invoice_details: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.98, 0.85, 0.90]
#     )
#     customer_info: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.88, 0.93, 0.86]
#     )
#     line_items: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.92, 0.89, 0.94]
#     )
#     totals: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.96, 0.91, 0.88]
#     )

# class ConfidenceScores(BaseModel):
#     """Overall confidence scoring for extraction quality"""
#     overall_confidence: Optional[float] = Field(
#         default=0.0, 
#         ge=0.0, 
#         le=1.0,
#         examples=[0.92, 0.87, 0.95],
#         description="Overall confidence score from 0.0 to 1.0"
#     )
#     field_confidence: Optional[FieldConfidence] = Field(
#         default_factory=FieldConfidence,
#         description="Confidence scores for individual field groups"
#     )

# class InvoiceData(BaseModel):
#     """Complete invoice data structure"""
#     vendor_info: Optional[VendorInfo] = Field(
#         default_factory=VendorInfo,
#         description="Information about the vendor/company issuing the invoice"
#     )
#     invoice_details: Optional[InvoiceDetails] = Field(
#         default_factory=InvoiceDetails,
#         description="Invoice header information and dates"
#     )
#     customer_info: Optional[CustomerInfo] = Field(
#         default_factory=CustomerInfo,
#         description="Information about the customer/bill-to party"
#     )
#     line_items: List[LineItem] = Field(
#         default_factory=list,
#         description="List of items/services on the invoice"
#     )
#     totals: Optional[Totals] = Field(
#         default_factory=Totals,
#         description="Invoice totals including subtotal, tax, and final amount"
#     )
#     confidence_scores: Optional[ConfidenceScores] = Field(
#         default_factory=ConfidenceScores,
#         description="Confidence scores for extraction quality assessment"
#     )

# class InvoiceExtractor:
#     """Invoice data extraction class using Docling"""
    
#     def __init__(self):
#         """Initialize the document extractor"""
#         self.extractor = DocumentExtractor(
#             allowed_formats=[InputFormat.IMAGE, InputFormat.PDF]
#         )
    
#     def extract_invoice_data(self, file_path: str) -> InvoiceData:
#         """
#         Extract structured invoice data from a file
        
#         Args:
#             file_path: Path to the invoice file (PDF or image)
            
#         Returns:
#             InvoiceData: Structured invoice data
#         """
#         try:
#             # Extract data using Docling with our Pydantic schema
#             result = self.extractor.extract(
#                 source=file_path,
#                 template=InvoiceData
#             )
            
#             if result.pages and len(result.pages) > 0:
#                 # Get the extracted data from the first page
#                 extracted_data = result.pages[0].extracted_data
                
#                 # Validate and create InvoiceData object
#                 invoice_data = InvoiceData.model_validate(extracted_data)
                
#                 return invoice_data
#             else:
#                 print("No data extracted from the document")
#                 return InvoiceData()
                
#         except Exception as e:
#             print(f"Error extracting data: {str(e)}")
#             return InvoiceData()
    
#     def extract_and_save(self, file_path: str, output_path: str = None) -> InvoiceData:
#         """
#         Extract invoice data and optionally save to JSON file
        
#         Args:
#             file_path: Path to the invoice file
#             output_path: Optional path to save JSON output
            
#         Returns:
#             InvoiceData: Structured invoice data
#         """
#         invoice_data = self.extract_invoice_data(file_path)
        
#         if output_path:
#             try:
#                 # Convert to dictionary and save as JSON
#                 invoice_dict = invoice_data.model_dump()
#                 with open(output_path, 'w', encoding='utf-8') as f:
#                     json.dump(invoice_dict, f, indent=2, ensure_ascii=False)
#                 print(f"Invoice data saved to: {output_path}")
#             except Exception as e:
#                 print(f"Error saving to JSON: {str(e)}")
        
#         return invoice_data
    
#     def print_invoice_summary(self, invoice_data: InvoiceData):
#         """Print a formatted summary of the extracted invoice data"""
#         print("\n" + "="*50)
#         print("INVOICE EXTRACTION SUMMARY")
#         print("="*50)
        
#         # Vendor Information
#         if invoice_data.vendor_info and invoice_data.vendor_info.company_name:
#             print(f"\nVENDOR: {invoice_data.vendor_info.company_name}")
#             if invoice_data.vendor_info.address:
#                 print(f"Address: {invoice_data.vendor_info.address}")
#             if invoice_data.vendor_info.phone:
#                 print(f"Phone: {invoice_data.vendor_info.phone}")
#             if invoice_data.vendor_info.email:
#                 print(f"Email: {invoice_data.vendor_info.email}")
        
#         # Invoice Details
#         if invoice_data.invoice_details:
#             print(f"\nINVOICE: {invoice_data.invoice_details.invoice_number or 'N/A'}")
#             print(f"Date: {invoice_data.invoice_details.date or 'N/A'}")
#             print(f"Due Date: {invoice_data.invoice_details.due_date or 'N/A'}")
#             print(f"Currency: {invoice_data.invoice_details.currency or 'N/A'}")
        
#         # Customer Information
#         if invoice_data.customer_info and invoice_data.customer_info.name:
#             print(f"\nCUSTOMER: {invoice_data.customer_info.name}")
#             if invoice_data.customer_info.address:
#                 print(f"Address: {invoice_data.customer_info.address}")
        
#         # Line Items
#         if invoice_data.line_items:
#             print(f"\nLINE ITEMS ({len(invoice_data.line_items)}):")
#             for i, item in enumerate(invoice_data.line_items, 1):
#                 print(f"  {i}. {item.description or 'N/A'}")
#                 print(f"     Qty: {item.quantity or 0} | Unit Price: {item.unit_price or 0} | Total: {item.total or 0}")
        
#         # Totals
#         if invoice_data.totals:
#             print(f"\nTOTALS:")
#             print(f"  Subtotal: {invoice_data.totals.subtotal or 0}")
#             print(f"  Tax: {invoice_data.totals.tax_amount or 0}")
#             print(f"  Total Amount: {invoice_data.totals.total_amount or 0}")
        
#         # Confidence Scores
#         if invoice_data.confidence_scores and invoice_data.confidence_scores.overall_confidence:
#             print(f"\nCONFIDENCE: {invoice_data.confidence_scores.overall_confidence:.2%}")
        
#         print("="*50)

# def main():
#     """Example usage of the invoice extractor"""
    
#     # Initialize the extractor
#     extractor = InvoiceExtractor()
    
#     # Example file paths - replace with your actual invoice files
#     invoice_files = [
#         # "sample-invoice.pdf",
#         "1131w-aBb_N6_4CUg.jpg",
#     ]
    
#     for file_path in invoice_files:
#         print(f"\nProcessing: {file_path}")
        
#         try:
#             # Extract invoice data
#             invoice_data = extractor.extract_and_save(
#                 file_path=file_path,
#                 output_path=f"extracted_{file_path.split('/')[-1].split('.')[0]}.json"
#             )
            
#             # Print summary
#             extractor.print_invoice_summary(invoice_data)
            
#             # Access specific fields programmatically
#             if invoice_data.totals and invoice_data.totals.total_amount:
#                 print(f"Total Amount: ${invoice_data.totals.total_amount:.2f}")
            
#             if invoice_data.vendor_info and invoice_data.vendor_info.company_name:
#                 print(f"Vendor: {invoice_data.vendor_info.company_name}")
            
#         except Exception as e:
#             print(f"Failed to process {file_path}: {str(e)}")

# if __name__ == "__main__":
#     import time
#     start_time = time.time()
#     main()
#     end_time = time.time()
#     print(f"Time taken : {end_time - start_time: .2f} seconds")
