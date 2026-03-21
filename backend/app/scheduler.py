"""
Automated Scheduler for Monthly Segmentation and Campaign Execution
Problem Statement Requirement: "AI segments customers monthly"
"""
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime
from app.database import db
from app.segmentation import enrich_lead_data
from app.email_sender import send_sales_email
from app.use_cases import match_use_case
from app.utils import generate_email_llama2, calculate_lead_score
from app.model import model
import time


class AutomationScheduler:
    """
    Handles automated tasks:
    1. Monthly customer segmentation
    2. Email campaign execution with throttling
    3. CRM data sync
    """
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    async def monthly_segmentation_job(self):
        """
        Run monthly re-segmentation of all customers.
        Identifies upsell/cross-sell opportunities.
        """
        print(f"\n🔄 Starting Monthly Segmentation Job at {datetime.now()}")
        
        try:
            all_leads = await db.get_all_leads()
            
            if not all_leads:
                print("⚠️ No leads found for segmentation")
                return
            
            updated_count = 0
            segment_changes = {}
            
            for lead in all_leads:
                try:
                    old_segment = lead.get("segment", "UNKNOWN")
                    
                    # Re-enrich and re-segment
                    enriched = enrich_lead_data(lead)
                    enriched['last_segmented_at'] = datetime.now().isoformat()
                    
                    new_segment = enriched.get("segment")
                    
                    # Track segment changes (upsell/cross-sell opportunities)
                    if old_segment != new_segment:
                        change_key = f"{old_segment} → {new_segment}"
                        segment_changes[change_key] = segment_changes.get(change_key, 0) + 1
                    
                    # Save updated lead
                    await db.save_lead(enriched)
                    updated_count += 1
                    
                except Exception as e:
                    print(f"Error segmenting {lead.get('company_name')}: {e}")
            
            print(f"✅ Monthly Segmentation Complete:")
            print(f"   - Total Leads Updated: {updated_count}")
            print(f"   - Segment Changes: {segment_changes}")
            
        except Exception as e:
            print(f"❌ Monthly Segmentation Failed: {e}")
    
    async def execute_scheduled_campaigns(self):
        """
        Execute scheduled email campaigns with throttling.
        Sends emails at configured rate to avoid spam.
        """
        print(f"\n📧 Checking for Scheduled Campaigns at {datetime.now()}")
        
        try:
            # Get all scheduled campaigns
            campaigns = await db.get_all_campaigns()
            scheduled = [c for c in campaigns if c.get("status") == "scheduled"]
            
            if not scheduled:
                print("No campaigns scheduled for execution")
                return
            
            for campaign in scheduled:
                try:
                    # Check if campaign should run now
                    send_time = campaign.get("send_time")
                    if send_time and datetime.fromisoformat(send_time) > datetime.now():
                        continue  # Not yet time
                    
                    print(f"🚀 Executing Campaign: {campaign['name']}")
                    
                    # Update status to active
                    await db.update_campaign_status(
                        str(campaign["_id"]), 
                        status="active"
                    )
                    
                    # Get target leads
                    target_emails = campaign.get("target_leads", [])
                    throttle_rate = campaign.get("throttle_rate", 10)  # emails per minute
                    delay = 60 / throttle_rate  # seconds between emails
                    
                    use_case_id = campaign.get("use_case_id")
                    emails_sent = 0
                    
                    # Send emails with throttling
                    for email in target_emails[:50]:  # Limit to 50 per execution
                        try:
                            # Fetch lead data
                            all_leads = await db.get_all_leads()
                            lead = next((l for l in all_leads if l.get("email") == email), None)
                            
                            if not lead:
                                continue
                            
                            # Generate and send email
                            result = send_sales_email(
                                customer_name=lead.get("company_name"),
                                customer_email=email,
                                lead_score=lead.get("lead_score", 0),
                                quote_value=lead.get("quote_value", 0),
                                item_count=lead.get("item_count", 0),
                                subject=f"Exclusive {campaign['campaign_type']} Opportunity"
                            )
                            
                            if result.get("success"):
                                emails_sent += 1
                            
                            # Throttle - wait before next email
                            time.sleep(delay)
                            
                        except Exception as e:
                            print(f"Error sending to {email}: {e}")
                    
                    # Update campaign progress
                    await db.update_campaign_status(
                        str(campaign["_id"]),
                        status="completed",
                        emails_sent=emails_sent
                    )
                    
                    print(f"✅ Campaign Complete: {emails_sent} emails sent")
                    
                except Exception as e:
                    print(f"Campaign execution error: {e}")
        
        except Exception as e:
            print(f"❌ Campaign Execution Failed: {e}")
    
    async def sync_crm_data(self):
        """
        Automated CRM data sync.
        Problem statement: "Ingest customer data from CRM"
        """
        print(f"\n🔄 CRM Sync Job at {datetime.now()}")
        
        # This would call the actual CRM sync endpoint
        # For now, just log the scheduled execution
        print("CRM sync would run here (requires CRM credentials)")
    
    def start(self):
        """
        Start the scheduler with all jobs.
        """
        if self.is_running:
            print("⚠️ Scheduler already running")
            return
        
        # Monthly segmentation - Run on 1st day of month at 2 AM
        self.scheduler.add_job(
            self.monthly_segmentation_job,
            CronTrigger(day=1, hour=2, minute=0),
            id="monthly_segmentation",
            name="Monthly Customer Segmentation"
        )
        
        # Campaign execution - Check every 15 minutes
        self.scheduler.add_job(
            self.execute_scheduled_campaigns,
            CronTrigger(minute="*/15"),
            id="campaign_execution",
            name="Email Campaign Execution"
        )
        
        # CRM Sync - Daily at 1 AM
        self.scheduler.add_job(
            self.sync_crm_data,
            CronTrigger(hour=1, minute=0),
            id="crm_sync",
            name="Daily CRM Data Sync"
        )
        
        self.scheduler.start()
        self.is_running = True
        print("✅ Automation Scheduler Started")
        print("   - Monthly Segmentation: 1st of month at 2:00 AM")
        print("   - Campaign Execution: Every 15 minutes")
        print("   - CRM Sync: Daily at 1:00 AM")
    
    def stop(self):
        """Stop the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            self.is_running = False
            print("✅ Scheduler stopped")


# Global scheduler instance
automation_scheduler = AutomationScheduler()
