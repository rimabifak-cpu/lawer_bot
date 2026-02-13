from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    telegram_id: int
    username: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int
    
    class Config:
        from_attributes = True

# PartnerProfile schemas
class PartnerProfileBase(BaseModel):
    user_id: int
    full_name: str
    company_name: str
    phone: str
    email: str
    specialization: str
    experience: int
    consent_to_share_data: bool = False

class PartnerProfileCreate(PartnerProfileBase):
    pass

class PartnerProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    specialization: Optional[str] = None
    experience: Optional[int] = None
    consent_to_share_data: Optional[bool] = None

class PartnerProfile(PartnerProfileBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ServiceRequest schemas
class ServiceRequestBase(BaseModel):
    user_id: int
    description: str
    status: str = "новый"

class ServiceRequestCreate(ServiceRequestBase):
    pass

class ServiceRequestUpdate(BaseModel):
    description: Optional[str] = None
    status: Optional[str] = None

class ServiceRequest(ServiceRequestBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# RequestDocument schemas
class RequestDocumentBase(BaseModel):
    request_id: int
    file_path: str
    file_type: str

class RequestDocumentCreate(RequestDocumentBase):
    pass

class RequestDocument(RequestDocumentBase):
    id: int
    uploaded_at: datetime
    
    class Config:
        from_attributes = True

# DocumentCategory schemas
class DocumentCategoryBase(BaseModel):
    name: str

class DocumentCategoryCreate(DocumentCategoryBase):
    pass

class DocumentCategory(DocumentCategoryBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document schemas
class DocumentBase(BaseModel):
    category_id: int
    title: str
    file_path: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# FAQ schemas
class FAQBase(BaseModel):
    question: str
    answer: str
    category: str

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None

class FAQ(FAQBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# PartnerRevenue schemas
class PartnerRevenueBase(BaseModel):
    partner_id: int
    amount: int
    description: Optional[str] = None
    client_reference: Optional[str] = None


class PartnerRevenueCreate(BaseModel):
    partner_id: int
    amount: int
    description: Optional[str] = None
    client_reference: Optional[str] = None


class PartnerRevenue(PartnerRevenueBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# ReferralPayout schemas
class ReferralPayoutBase(BaseModel):
    referrer_id: int
    amount: int
    month: int
    year: int
    status: str = "pending"


class ReferralPayoutCreate(BaseModel):
    referrer_id: int
    amount: int
    month: int
    year: int


class ReferralPayout(ReferralPayoutBase):
    id: int
    paid_at: Optional[datetime] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


# CaseMessage schemas
class CaseMessageBase(BaseModel):
    questionnaire_id: int
    sender_id: int
    sender_type: str  # 'admin' или 'user'
    message_content: str


class CaseMessageCreate(BaseModel):
    questionnaire_id: int
    sender_id: int
    sender_type: str
    message_content: str


class CaseMessage(CaseMessageBase):
    id: int
    is_read: bool
    created_at: datetime
    
    class Config:
        from_attributes = True