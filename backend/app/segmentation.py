from app.schemas import Industry, MaturityLevel, Segment, JobRole
import random
from app.model import model
from app.utils import calculate_lead_score

def determine_industry(company_name: str) -> Industry:
    """
    Determine industry based on company name keywords.
    In a real system, this would use an external API or detailed firmographic data.
    """
    name = company_name.lower()
    
    if any(x in name for x in ['tech', 'soft', 'data', 'cloud', 'ai', 'cyber', 'sys']):
        return Industry.TECHNOLOGY
    elif any(x in name for x in ['health', 'med', 'pharma', 'care', 'bio']):
        return Industry.HEALTHCARE
    elif any(x in name for x in ['bank', 'fin', 'capital', 'invest', 'insur']):
        return Industry.FINANCE
    elif any(x in name for x in ['shop', 'retail', 'store', 'market']):
        return Industry.RETAIL
    elif any(x in name for x in ['mfg', 'ind', 'eng', 'construct', 'build']):
        return Industry.MANUFACTURING
    elif any(x in name for x in ['edu', 'school', 'univ', 'learn']):
        return Industry.EDUCATION
    else:
        # Randomly assign for demo purposes if no keyword match
        return random.choice([Industry.TECHNOLOGY, Industry.MANUFACTURING, Industry.FINANCE, Industry.OTHER])

def determine_maturity(quote_value: float, item_count: int, past_engagements: int = 0) -> MaturityLevel:
    """
    Determine customer maturity based on spending and engagement.
    """
    if quote_value > 50000 or item_count > 100:
        return MaturityLevel.ENTERPRISE
    elif quote_value > 10000 or item_count > 20:
        return MaturityLevel.MATURE
    elif quote_value > 5000:
        return MaturityLevel.GROWTH
    else:
        return MaturityLevel.EARLY_STAGE

def assign_segment(industry: Industry, maturity: MaturityLevel) -> Segment:
    """
    Assign a strategic segment based on Industry and Maturity.
    """
    if industry == Industry.TECHNOLOGY and maturity in [MaturityLevel.MATURE, MaturityLevel.ENTERPRISE]:
        return Segment.HIGH_VALUE_TECH
    elif industry == Industry.HEALTHCARE:
        return Segment.HEALTHCARE_INNOVATORS
    elif industry == Industry.FINANCE and maturity == MaturityLevel.ENTERPRISE:
        return Segment.FINANCIAL_ENTERPRISE
    elif industry == Industry.RETAIL and maturity == MaturityLevel.GROWTH:
        return Segment.RETAIL_GROWTH
    elif industry == Industry.MANUFACTURING:
        return Segment.MANUFACTURING_DIGITAL
    elif industry == Industry.EDUCATION:
        return Segment.EDUCATION_TECH
    else:
        return Segment.GENERAL


def determine_job_role(role_string: str = None) -> JobRole:
    """
    Determine job role from string input.
    Used for decision-maker identification per problem statement.
    """
    if not role_string:
        return JobRole.OTHER
    
    role_lower = role_string.lower()
    
    if 'cto' in role_lower or 'chief technology' in role_lower:
        return JobRole.CTO
    elif 'cio' in role_lower or 'chief information' in role_lower:
        return JobRole.CIO
    elif 'cfo' in role_lower or 'chief financial' in role_lower:
        return JobRole.CFO
    elif 'ceo' in role_lower or 'chief executive' in role_lower:
        return JobRole.CEO
    elif 'vp' in role_lower and 'eng' in role_lower:
        return JobRole.VP_ENGINEERING
    elif 'vp' in role_lower and 'sales' in role_lower:
        return JobRole.VP_SALES
    elif 'vp' in role_lower and 'operation' in role_lower:
        return JobRole.VP_OPERATIONS
    elif 'director' in role_lower and 'it' in role_lower:
        return JobRole.DIRECTOR_IT
    elif 'manager' in role_lower:
        return JobRole.MANAGER
    elif 'procurement' in role_lower or 'purchasing' in role_lower:
        return JobRole.PROCUREMENT
    else:
        return JobRole.OTHER


def is_decision_maker(job_role: JobRole) -> bool:
    """
    Identify if contact is a decision-maker (C-level or VP).
    Critical for prioritization per problem statement.
    """
    return job_role in [
        JobRole.CEO, JobRole.CTO, JobRole.CIO, JobRole.CFO,
        JobRole.VP_ENGINEERING, JobRole.VP_SALES, JobRole.VP_OPERATIONS
    ]


def enrich_lead_data(lead_record: dict) -> dict:
    """
    Enrich a raw lead record with segmentation data.
    Implements problem statement requirements:
    - Industry segmentation
    - Maturity level assessment  
    - Role-based decision-maker identification
    - Past engagement tracking
    """
    company_name = lead_record.get('company_name', lead_record.get('customer_name', 'Unknown'))
    quote_value = float(lead_record.get('quote_value', 0) or 0)
    item_count = int(lead_record.get('item_count', 0) or 0)
    
    # Get or determine job role
    job_role_str = lead_record.get('job_role') or lead_record.get('role')
    if isinstance(job_role_str, str):
        job_role = determine_job_role(job_role_str)
    else:
        job_role = JobRole.OTHER
    
    # Get past engagements (real from CRM or simulated)
    past_engagements = int(lead_record.get('past_engagements', 0) or 0)
    if past_engagements == 0:
        # Simulate if not provided (for demo purposes)
        past_engagements = random.randint(0, 5)
    
    # Run segmentation logic
    industry = determine_industry(company_name)
    maturity = determine_maturity(quote_value, item_count, past_engagements)
    segment = assign_segment(industry, maturity)
    
    # Calculate additional metrics
    revenue_potential = quote_value * 1.5 if maturity == MaturityLevel.ENTERPRISE else quote_value * 1.2
    
    # Boost revenue potential for decision-makers
    if is_decision_maker(job_role):
        revenue_potential *= 1.3
    
    # Calculate lead score using ML model
    conversion_days = int(lead_record.get('conversion_days', 45) or 45)  # Default 45 days
    try:
        X = [[quote_value, item_count, conversion_days]]
        ml_score, probability = calculate_lead_score(model, X)
        
        # Hybrid scoring: Start with Business Rules (more weight)
        # Base score from deal size
        if quote_value > 300000:
            base_score = 50
        elif quote_value > 150000:
            base_score = 40
        elif quote_value > 75000:
            base_score = 35
        elif quote_value > 30000:
            base_score = 25
        else:
            base_score = 15
        
        # Boost for decision-makers (+20 points)
        if is_decision_maker(job_role):
            base_score += 25
        
        # Boost for high-value segments (+10 points)
        if segment in [Segment.HIGH_VALUE_TECH, Segment.FINANCIAL_ENTERPRISE]:
            base_score += 10
        
        # Boost for multiple past engagements
        if past_engagements > 10:
            base_score += 10
        elif past_engagements > 5:
            base_score += 5
        
        # Boost based on item count (higher engagement)
        if item_count > 400:
            base_score += 5
        
        # Add ML model contribution (5-15 points based on its prediction)
        ml_contribution = min(ml_score, 15)
        hybrid_score = base_score + ml_contribution
        
        # Cap at 100
        hybrid_score = min(hybrid_score, 100)
        
        # Convert to 0-1 scale for consistency (frontend expects decimal)
        lead_score = hybrid_score / 100
        probability = hybrid_score / 100
        
    except Exception as e:
        # Fallback if model prediction fails
        lead_score = 0.5
        probability = 0.5
    
    # Update record
    lead_record['industry'] = industry
    lead_record['maturity_level'] = maturity
    lead_record['segment'] = segment
    lead_record['job_role'] = job_role
    lead_record['is_decision_maker'] = is_decision_maker(job_role)
    lead_record['revenue_potential'] = round(revenue_potential, 2)
    lead_record['past_engagements'] = past_engagements
    lead_record['lead_score'] = lead_score
    lead_record['conversion_probability'] = round(probability, 4)
    
    return lead_record


def resegment_all_leads(leads: list) -> list:
    """
    Re-segment all leads for monthly automation.
    Problem statement requirement: "AI segments customers monthly"
    """
    return [enrich_lead_data(lead) for lead in leads]
