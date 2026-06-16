from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CoverLetterGenerateRequest(BaseModel):
    job_title: str
    company_name: Optional[str] = None
    job_description: str
    recruiter_email: Optional[str] = None
    generated_by: Optional[str] = "visitor" # 'visitor' or 'owner'

class CoverLetterResponse(BaseModel):
    id: int
    job_title: str
    company_name: Optional[str] = None
    job_description: str
    generated_letter: str
    generated_by: str
    recruiter_email: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class SendEmailRequest(BaseModel):
    email: str
    pdf_base64: Optional[str] = None
