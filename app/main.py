from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import invoice

app = FastAPI(title="Invoice Extractor",
            description="An AI-powered invoice extraction tool that automates invoice processing from Invoice PDF and Images.",
            version="0.0.0")


#Allow all origin for CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(invoice.router, prefix="/api/v1/invoice", tags=["Invoice Extractor"])
