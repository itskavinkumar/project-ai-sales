import os
import pandas as pd
from typing import List, Dict, Optional
from dotenv import load_dotenv

# Try importing simple_salesforce, handle if not installed
try:
    from simple_salesforce import Salesforce
except ImportError:
    Salesforce = None

load_dotenv()

class CRMConnector:
    """
    Base class for CRM integrations (Salesforce, HubSpot, etc.)
    """
    def connect(self):
        raise NotImplementedError
    
    def fetch_leads(self) -> List[Dict]:
        raise NotImplementedError

    def update_lead(self, lead_id: str, updates: Dict):
        raise NotImplementedError

class SalesforceClient(CRMConnector):
    def __init__(self):
        self.username = os.getenv("SF_USERNAME")
        self.password = os.getenv("SF_PASSWORD")
        self.security_token = os.getenv("SF_TOKEN")
        self.sf = None

    def connect(self):
        """Authenticates with Salesforce API"""
        if not Salesforce:
            print("❌ simple-salesforce library not installed. Run: pip install simple-salesforce")
            return False
            
        try:
            self.sf = Salesforce(
                username=self.username,
                password=self.password,
                security_token=self.security_token
            )
            print("✅ Connected to Salesforce CRM")
            return True
        except Exception as e:
            print(f"❌ Salesforce Connection Error: {e}")
            return False

    def fetch_leads(self, limit=100) -> List[Dict]:
        """
        Fetches 'Open - Not Contacted' leads and maps them to our AI schema.
        Enhanced to include role and past engagements.
        """
        if not self.sf:
            print("⚠️ Not connected to Salesforce. Using mock data.")
            return []

        # SOQL Query to fetch relevant fields including role and past activities
        query = f"""
            SELECT Id, Name, Company, Industry, AnnualRevenue, NumberOfEmployees, 
                   Title, Email, Description, 
                   (SELECT Id FROM Tasks) Tasks,
                   (SELECT Id FROM Events) Events
            FROM Lead 
            WHERE Status = 'Open - Not Contacted' 
            LIMIT {limit}
        """
        
        try:
            results = self.sf.query(query)
            records = results['records']
            
            mapped_leads = []
            for r in records:
                # Calculate past engagements from tasks and events
                task_count = len(r.get('Tasks', {}).get('records', []))
                event_count = len(r.get('Events', {}).get('records', []))
                past_engagements = task_count + event_count
                
                # Map Salesforce fields to our Internal AI Model
                mapped_leads.append({
                    "id": r['Id'],
                    "company_name": r['Company'] or r['Name'],
                    "job_role": r['Title'],  # Job title/role
                    "email": r['Email'],
                    # normalize revenue to our 'quote_value' proxy
                    "quote_value": float(r['AnnualRevenue'] or 0) / 100, 
                    # normalize employees to our 'item_count' proxy
                    "item_count": int(r['NumberOfEmployees'] or 1),
                    "industry": r['Industry'] or "Unknown",
                    "conversion_days": 30, # Default for new leads
                    "past_engagements": past_engagements,  # Real engagement history
                    "source": "Salesforce"
                })
            
            return mapped_leads
            
        except Exception as e:
            print(f"❌ Error fetching Salesforce leads: {e}")
            return []

    def update_lead_ai_data(self, lead_id: str, lead_score: float, use_case: str):
        """
        Writes the AI Score and Recommended Use Case back to Salesforce
        """
        if not self.sf:
            return
            
        try:
            # Assumes you have created custom fields: AI_Score__c and AI_Use_Case__c
            self.sf.Lead.update(lead_id, {
                'AI_Score__c': lead_score,
                'AI_Recommended_Use_Case__c': use_case,
                'Description': f"AI Strategy Recommendation: {use_case}"
            })
            print(f"✅ Updated Salesforce Lead {lead_id}")
        except Exception as e:
            print(f"❌ Failed to update lead {lead_id}: {e}")

# ---------------------------------------------------------
# Mock Connector (Use this for testing without credentials)
# ---------------------------------------------------------
class MockCRMClient(CRMConnector):
    def connect(self):
        print("✅ [MOCK] Connected to CRM Simulator")
        return True

    def fetch_leads(self, limit=100) -> List[Dict]:
        """Returns dummy data structured exactly like the Salesforce output"""
        return [
            {
                "id": "LEAD-001",
                "company_name": "Acme Manufacturing Corp",
                "industry": "Manufacturing",
                "job_role": "Chief Technology Officer",
                "quote_value": 120000,
                "item_count": 500,
                "conversion_days": 45,
                "past_engagements": 3,
                "email": "cto@acme-manufacturing.com"
            },
            {
                "id": "LEAD-002",
                "company_name": "TechStart Cloud Solutions",
                "industry": "Technology",
                "job_role": "VP Engineering",
                "quote_value": 45000,
                "item_count": 25,
                "conversion_days": 15,
                "past_engagements": 7,
                "email": "vp@techstart.io"
            },
            {
                "id": "LEAD-003",
                "company_name": "HealthCare Innovators Inc",
                "industry": "Healthcare",
                "job_role": "Chief Information Officer",
                "quote_value": 85000,
                "item_count": 150,
                "conversion_days": 30,
                "past_engagements": 2,
                "email": "cio@healthcare-innovators.com"
            },
            {
                "id": "LEAD-004",
                "company_name": "Retail Express",
                "industry": "Retail",
                "job_role": "Manager",
                "quote_value": 15000,
                "item_count": 30,
                "conversion_days": 20,
                "past_engagements": 1,
                "email": "manager@retailexpress.com"
            }
        ]
    
    def update_lead(self, lead_id: str, updates: Dict):
        print(f"✅ [MOCK] Updated lead {lead_id} with: {updates}")
        return True

# Factory to get the right client
def get_crm_client(use_mock=False):
    if use_mock:
        return MockCRMClient()
    return SalesforceClient()
