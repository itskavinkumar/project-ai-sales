from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime


# Enums for structured data
class Industry(str, Enum):
    TECHNOLOGY = "Technology"
    HEALTHCARE = "Healthcare"
    FINANCE = "Finance"
    RETAIL = "Retail"
    MANUFACTURING = "Manufacturing"
    EDUCATION = "Education"
    OTHER = "Other"


class MaturityLevel(str, Enum):
    EARLY_STAGE = "Early Stage"
    GROWTH = "Growth"
    MATURE = "Mature"
    ENTERPRISE = "Enterprise"


class Segment(str, Enum):
    HIGH_VALUE_TECH = "High-Value Technology"
    HEALTHCARE_INNOVATORS = "Healthcare Innovators"
    FINANCIAL_ENTERPRISE = "Financial Enterprise"
    RETAIL_GROWTH = "Retail Growth"
    MANUFACTURING_DIGITAL = "Manufacturing Digital Transformation"
    EDUCATION_TECH = "Education Technology"
    GENERAL = "General"


class JobRole(str, Enum):
    CTO = "Chief Technology Officer"
    CIO = "Chief Information Officer"
    CFO = "Chief Financial Officer"
    CEO = "Chief Executive Officer"
    VP_ENGINEERING = "VP Engineering"
    VP_SALES = "VP Sales"
    VP_OPERATIONS = "VP Operations"
    DIRECTOR_IT = "Director IT"
    MANAGER = "Manager"
    PROCUREMENT = "Procurement"
    OTHER = "Other"


# Original schemas
class LeadInput(BaseModel):
    id: Optional[str] = None  # Salesforce/CRM ID
    quote_value: float
    item_count: int
    conversion_days: int
    company_name: Optional[str] = "Unknown Tech Co"
    email: Optional[str] = None
    job_role: Optional[JobRole] = JobRole.OTHER
    past_engagements: Optional[int] = 0


class LeadScoreResponse(BaseModel):
    lead_score: float
    conversion_probability: float


# Enhanced Lead Schema with Segmentation
class EnhancedLead(BaseModel):
    company_name: str
    email: Optional[str] = None
    job_role: Optional[JobRole] = JobRole.OTHER
    industry: Optional[Industry] = Industry.OTHER
    maturity_level: Optional[MaturityLevel] = MaturityLevel.EARLY_STAGE
    segment: Optional[Segment] = Segment.GENERAL
    quote_value: float
    item_count: int
    conversion_days: Optional[int] = -1
    lead_score: Optional[float] = 0.0
    conversion_probability: Optional[float] = 0.0
    past_engagements: Optional[int] = 0
    revenue_potential: Optional[float] = 0.0
    last_segmented_at: Optional[str] = None


# Use Case Schemas
class UseCase(BaseModel):
    id: str
    title: str
    description: str
    industry: Industry
    pain_points: List[str]
    solution_summary: str
    success_metrics: Optional[str] = None
    customer_type: Optional[MaturityLevel] = None
    relevant_segments: List[Segment]


class UseCaseCreate(BaseModel):
    title: str
    description: str
    industry: Industry
    pain_points: List[str]
    solution_summary: str
    success_metrics: Optional[str] = None
    customer_type: Optional[MaturityLevel] = None
    relevant_segments: List[Segment]


# Campaign Schemas
class CampaignType(str, Enum):
    ONBOARDING = "Onboarding"
    NURTURE = "Nurture"
    CROSS_SELL = "Cross-Sell"
    UPSELL = "Upsell"
    RE_ENGAGEMENT = "Re-engagement"


class Campaign(BaseModel):
    id: str
    name: str
    campaign_type: CampaignType
    target_segment: Segment
    use_case_id: Optional[str] = None
    emails_sent: int = 0
    emails_scheduled: int = 0
    status: str = "draft"  # draft, scheduled, active, completed
    created_at: Optional[str] = None


class CampaignCreate(BaseModel):
    name: str
    campaign_type: CampaignType
    target_segment: Segment
    use_case_id: Optional[str] = None
    send_time: Optional[str] = None
    throttle_rate: Optional[int] = 10  # emails per minute


# Enhanced Email Schemas
class EmailInput(BaseModel):
    customer_name: str
    lead_score: float
    quote_value: float
    item_count: int
    industry: Optional[Industry] = Industry.OTHER
    segment: Optional[Segment] = Segment.GENERAL
    use_case_id: Optional[str] = None


class EmailResponse(BaseModel):
    subject: str
    email_body: str
    use_case_applied: Optional[str] = None


class SendEmailInput(BaseModel):
    customer_name: str
    customer_email: str
    lead_score: float
    quote_value: float
    item_count: int
    industry: Optional[Industry] = Industry.OTHER
    segment: Optional[Segment] = Segment.GENERAL
    use_case_id: Optional[str] = None
    subject: str = "Exclusive IT Solutions for Your Business"


class SendEmailResponse(BaseModel):
    success: bool
    message: str
    email_body: str


# CRM Integration Schemas
class CRMSync(BaseModel):
    source: str  # "salesforce", "hubspot", "dynamics"
    sync_type: str  # "full", "incremental"
    records_synced: int = 0
    status: str = "pending"


# Segmentation Request/Response
class SegmentationRequest(BaseModel):
    lead_ids: Optional[List[str]] = None  # If None, segment all leads
    force_resegment: bool = False


class SegmentationResponse(BaseModel):
    segments_updated: int
    segment_distribution: dict


# Cross-sell/Upsell Schemas
class OpportunityType(str, Enum):
    CROSS_SELL = "Cross-Sell"
    UPSELL = "Upsell"
    RENEWAL = "Renewal"


class SalesOpportunity(BaseModel):
    company_name: str
    opportunity_type: OpportunityType
    recommended_product: str
    confidence_score: float
    estimated_value: float
    rationale: str
