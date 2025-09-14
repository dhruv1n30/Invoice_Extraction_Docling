from typing import List, Optional

from pydantic import Field, BaseModel


class VendorInfo(BaseModel):
    """Pydantic model for vendor information."""
    company_name: Optional[str] = Field(default=None, description="The name of the vendor's company.")
    address: Optional[str] = Field(default=None, description="The vendor's address.")
    phone: Optional[str] = Field(default=None, description="The vendor's phone number.")
    email: Optional[str] = Field(default=None, description="The vendor's email address.")
    tax_id: Optional[str] = Field(default=None, description="The vendor's tax identification number.")

class InvoiceDetails(BaseModel):
    """Pydantic model for core invoice details."""
    invoice_number: Optional[str] = Field(default=None, description="The unique invoice number.")
    date: Optional[str] = Field(default=None, description="The date the invoice was issued (YYYY-MM-DD).")
    due_date: Optional[str] = Field(default=None, description="The date the invoice is due (YYYY-MM-DD).")
    currency: Optional[str] = Field(default=None, description="The currency of the invoice amounts (e.g., USD, EUR).")

class CustomerInfo(BaseModel):
    """Pydantic model for customer information."""
    name: Optional[str] = Field(default=None, description="The name of the customer.")
    address: Optional[str] = Field(default=None, description="The customer's billing address.")
    customer_id: Optional[str] = Field(default=None, description="The customer's unique ID.")

class LineItem(BaseModel):
    """Pydantic model for a single line item in the invoice."""
    description: Optional[str] = Field(default=None, description="Description of the product or service.")
    quantity: Optional[float] = Field(default=None, description="The quantity of the item.")
    unit_price: Optional[float] = Field(default=None, description="The price per unit of the item.")
    total: Optional[float] = Field(default=None, description="The total price for the line item (quantity * unit_price).")

class Totals(BaseModel):
    """Pydantic model for the invoice totals."""
    subtotal: Optional[float] = Field(default=None, description="The total amount before taxes.")
    tax_amount: Optional[float] = Field(default=None, description="The total amount of tax.")
    total_amount: Optional[float] = Field(default=None, description="The final amount due (subtotal + tax).")

class StructuredInvoice(BaseModel):
    """Main Pydantic model that combines all parts of the invoice."""
    vendor_info: VendorInfo = Field(default_factory=VendorInfo)
    invoice_details: InvoiceDetails = Field(default_factory=InvoiceDetails)
    customer_info: CustomerInfo = Field(default_factory=CustomerInfo)
    line_items: List[LineItem] = Field(default_factory=list)
    totals: Totals = Field(default_factory=Totals)
