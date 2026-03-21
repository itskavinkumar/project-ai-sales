from typing import List, Optional
from app.schemas import UseCase, Industry, MaturityLevel, Segment

# Mock Database of Use Cases
USE_CASE_DB = [
    UseCase(
        id="UC001",
        title="AI-Driven Inventory Optimization",
        description="Reducing stockouts and overstock for manufacturing clients using predictive analytics.",
        industry=Industry.MANUFACTURING,
        pain_points=["High inventory costs", "Frequent stockouts", "Supply chain visibility"],
        solution_summary="Implemented our AI forecasting model to predict material needs 4 weeks in advance.",
        success_metrics="Reduced inventory holding costs by 22% in 6 months.",
        relevant_segments=[Segment.MANUFACTURING_DIGITAL, Segment.GENERAL]
    ),
    UseCase(
        id="UC002",
        title="Cloud Migration Accelerator",
        description="Seamless transition from legacy on-prem systems to cloud infrastructure for financial institutions.",
        industry=Industry.FINANCE,
        pain_points=["Legacy system downtime", "Security compliance risks", "Slow feature rollouts"],
        solution_summary="Deployed our secure migration framework with zero downtime guarantees.",
        success_metrics="Improved transaction speed by 40% while maintaining ISO 27001 compliance.",
        relevant_segments=[Segment.FINANCIAL_ENTERPRISE]
    ),
    UseCase(
        id="UC003",
        title="Patient Experience Data Platform",
        description="Unified data layer for healthcare providers to improve patient engagement.",
        industry=Industry.HEALTHCARE,
        pain_points=["Siloed patient data", "Low patient engagement", "Regulatory reporting burdens"],
        solution_summary="Integrated 5 different EHR systems into a single patient 360 view.",
        success_metrics="Increased patient portal adoption by 35%.",
        relevant_segments=[Segment.HEALTHCARE_INNOVATORS]
    ),
    UseCase(
        id="UC004",
        title="Omnichannel Retail Analytics",
        description="Connecting online and offline sales data for personalized customer journeys.",
        industry=Industry.RETAIL,
        pain_points=["Disconnected customer journey", "Inefficient marketing spend", "Low retention"],
        solution_summary="Implemented real-time attribution modeling across web, app, and in-store.",
        success_metrics="Boosted repeat purchase rate by 18% in Q4.",
        relevant_segments=[Segment.RETAIL_GROWTH]
    ),
    UseCase(
        id="UC005",
        title="Next-Gen EdTech Infrastructure",
        description="Scalable infrastructure for remote learning and digital campuses.",
        industry=Industry.EDUCATION,
        pain_points=["Video lag in classrooms", "Security vulnerabilities", "User management overhead"],
        solution_summary="Rolled out high-bandwidth, secure hybrid cloud environment.",
        success_metrics="Supported 50k concurrent users with 99.99% uptime.",
        relevant_segments=[Segment.EDUCATION_TECH]
    ),
    UseCase(
        id="UC006",
        title="Enterprise DevOps Transformation",
        description="Automating CI/CD pipelines for high-growth tech companies.",
        industry=Industry.TECHNOLOGY,
        pain_points=["Slow deployment cycles", "High bug rate", "Developer burnout"],
        solution_summary="Standardized deployment pipelines and automated testing.",
        success_metrics="Reduced deployment time from 2 days to 2 hours.",
        relevant_segments=[Segment.HIGH_VALUE_TECH]
    )
]

def get_all_use_cases() -> List[UseCase]:
    """Retrieve all use cases"""
    return USE_CASE_DB

def get_use_case_by_id(use_case_id: str) -> Optional[UseCase]:
    """Find a specific use case"""
    for uc in USE_CASE_DB:
        if uc.id == use_case_id:
            return uc
    return None

def match_use_case(industry: Industry, segment: Segment) -> UseCase:
    """
    Intelligent Use Case Matching Logic.
    Finds the most relevant use case for a given customer profile.
    """
    # First try exact segment match
    for uc in USE_CASE_DB:
        if segment in uc.relevant_segments:
            return uc
            
    # Then try industry match
    for uc in USE_CASE_DB:
        if uc.industry == industry:
            return uc
            
    # Fallback to general tech use case
    return USE_CASE_DB[5]  # Default to DevOps/Tech
