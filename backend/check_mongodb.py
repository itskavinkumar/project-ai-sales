"""
Check MongoDB connection and view stored leads
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ai_sales_db")


async def check_mongodb():
    print("="*60)
    print("  MONGODB DATA VERIFICATION")
    print("="*60)
    
    try:
        # Connect to MongoDB
        client = AsyncIOMotorClient(MONGO_URL)
        db = client[DB_NAME]
        
        print(f"\n✅ Connected to MongoDB: {DB_NAME}")
        
        # Count leads
        leads_count = await db["leads"].count_documents({})
        print(f"\n📊 Total Leads in MongoDB: {leads_count}")
        
        # Get sample leads
        print("\n📋 Sample Leads (First 5):")
        print("-" * 60)
        
        cursor = db["leads"].find().limit(5)
        leads = await cursor.to_list(length=5)
        
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. Company: {lead.get('company_name')}")
            print(f"   Email: {lead.get('email')}")
            print(f"   Role: {lead.get('job_role')}")
            print(f"   Industry: {lead.get('industry')}")
            print(f"   Segment: {lead.get('segment')}")
            print(f"   Quote Value: ${lead.get('quote_value', 0):,}")
            print(f"   Revenue Potential: ${lead.get('revenue_potential', 0):,}")
            print(f"   Past Engagements: {lead.get('past_engagements', 0)}")
            print(f"   Decision Maker: {lead.get('is_decision_maker', False)}")
        
        # Segment distribution
        print("\n" + "="*60)
        print("  SEGMENT DISTRIBUTION IN MONGODB")
        print("="*60)
        
        pipeline = [
            {
                "$group": {
                    "_id": "$segment",
                    "count": {"$sum": 1},
                    "avg_quote": {"$avg": "$quote_value"},
                    "total_revenue": {"$sum": "$revenue_potential"}
                }
            },
            {"$sort": {"count": -1}}
        ]
        
        segments = await db["leads"].aggregate(pipeline).to_list(length=100)
        
        for seg in segments:
            print(f"\n{seg['_id']}:")
            print(f"   Leads: {seg['count']}")
            print(f"   Avg Quote: ${seg['avg_quote']:,.0f}")
            print(f"   Total Pipeline: ${seg['total_revenue']:,.0f}")
        
        # Check campaigns
        campaigns_count = await db["campaigns"].count_documents({})
        print(f"\n📧 Total Campaigns: {campaigns_count}")
        
        client.close()
        print("\n✅ MongoDB verification complete!")
        
    except Exception as e:
        print(f"\n❌ MongoDB Error: {e}")
        print("\nMake sure:")
        print("1. MongoDB is running")
        print("2. Connection URL is correct")


if __name__ == "__main__":
    asyncio.run(check_mongodb())
    print("\n" + "="*60)
