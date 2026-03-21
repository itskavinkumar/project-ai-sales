"""
Script to recalculate lead scores for all leads in MongoDB.
This will add lead_score to all 228 existing leads.
"""
import asyncio
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from motor.motor_asyncio import AsyncIOMotorClient
from app.segmentation import enrich_lead_data
from dotenv import load_dotenv

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ai_sales_db")


async def recalculate_all_scores():
    """Recalculate lead scores for all leads in database"""
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    print("🔄 Fetching all leads from MongoDB...")
    leads = await db["leads"].find({}).to_list(length=None)
    total = len(leads)
    
    print(f"✅ Found {total} leads")
    print(f"🧮 Recalculating scores...\n")
    
    updated_count = 0
    errors = []
    
    for idx, lead in enumerate(leads, 1):
        try:
            # Convert ObjectId to string for processing
            lead_id = lead.pop('_id')
            
            # Enrich lead data (this will calculate lead_score)
            enriched = enrich_lead_data(lead)
            
            # Update in database
            result = await db["leads"].update_one(
                {"_id": lead_id},
                {"$set": {
                    "lead_score": enriched.get("lead_score", 0),
                    "conversion_probability": enriched.get("conversion_probability", 0)
                }}
            )
            
            if result.modified_count > 0:
                updated_count += 1
            
            # Print progress
            if idx % 50 == 0 or idx == total:
                print(f"⏳ Progress: {idx}/{total} leads processed ({updated_count} updated)")
                if enriched.get("lead_score"):
                    print(f"   Last: {enriched.get('company_name', 'N/A')} - Score: {enriched['lead_score']:.1f}%")
        
        except Exception as e:
            error_msg = f"Error processing lead {idx}: {str(e)}"
            errors.append(error_msg)
            print(f"❌ {error_msg}")
    
    print(f"\n✨ Score Recalculation Complete!")
    print(f"   Total Leads: {total}")
    print(f"   Updated: {updated_count}")
    print(f"   Errors: {len(errors)}")
    
    if errors:
        print("\n⚠️ Errors encountered:")
        for error in errors[:10]:  # Show first 10 errors
            print(f"   - {error}")
    
    # Show sample of high-value leads
    print("\n🎯 Sample of High-Value Leads (Score > 70%):")
    high_value_leads = await db["leads"].find(
        {"lead_score": {"$gt": 70}}
    ).limit(5).to_list(length=5)
    
    for lead in high_value_leads:
        print(f"   • {lead.get('company_name', 'N/A'):30} | Score: {lead.get('lead_score', 0):5.1f}% | "
              f"Segment: {lead.get('segment', 'N/A')}")
    
    # Show statistics by score category
    print("\n📊 Score Distribution:")
    high_count = await db["leads"].count_documents({"lead_score": {"$gte": 70}})
    medium_count = await db["leads"].count_documents({"lead_score": {"$gte": 40, "$lt": 70}})
    low_count = await db["leads"].count_documents({"lead_score": {"$lt": 40}})
    
    print(f"   High (≥70%):   {high_count:3} leads")
    print(f"   Medium (40-70%): {medium_count:3} leads")
    print(f"   Low (<40%):    {low_count:3} leads")
    
    client.close()


if __name__ == "__main__":
    print("=" * 60)
    print("  LEAD SCORE RECALCULATION TOOL")
    print("=" * 60)
    print()
    
    asyncio.run(recalculate_all_scores())
    
    print("\n✅ All done! Refresh your frontend to see updated scores.")
