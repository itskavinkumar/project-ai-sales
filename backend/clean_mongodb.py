"""
Clean MongoDB and keep only realistic leads
Removes old anonymized CSV data, keeps the good generated leads
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ai_sales_db")


async def clean_mongodb():
    print("="*60)
    print("  MONGODB CLEANUP & VERIFICATION")
    print("="*60)
    
    client = AsyncIOMotorClient(MONGO_URL)
    db = client[DB_NAME]
    
    # Count current leads
    total_before = await db["leads"].count_documents({})
    print(f"\n📊 Total Leads Before Cleanup: {total_before}")
    
    # Find leads without proper segmentation (old CSV data)
    bad_leads = await db["leads"].count_documents({
        "$or": [
            {"segment": None},
            {"segment": {"$exists": False}},
            {"industry": None},
            {"industry": {"$exists": False}},
            {"job_role": None},
            {"job_role": {"$exists": False}}
        ]
    })
    
    print(f"❌ Bad/Incomplete Leads (no segment/industry/role): {bad_leads}")
    
    # Find good leads (with full data)
    good_leads = await db["leads"].count_documents({
        "segment": {"$exists": True, "$ne": None},
        "industry": {"$exists": True, "$ne": None},
        "job_role": {"$exists": True, "$ne": None}
    })
    
    print(f"✅ Good Leads (complete data): {good_leads}")
    
    # Ask for confirmation
    print("\n" + "="*60)
    print("  OPTIONS")
    print("="*60)
    print("\n1. Delete bad leads (keep only complete data)")
    print("2. View sample good leads")
    print("3. View sample bad leads")
    print("4. Delete ALL leads and start fresh")
    print("5. Exit without changes")
    
    choice = input("\nSelect option (1-5): ").strip()
    
    if choice == "1":
        # Delete incomplete leads
        result = await db["leads"].delete_many({
            "$or": [
                {"segment": None},
                {"segment": {"$exists": False}},
                {"industry": None},
                {"industry": {"$exists": False}},
                {"job_role": None},
                {"job_role": {"$exists": False}}
            ]
        })
        
        print(f"\n✅ Deleted {result.deleted_count} incomplete leads")
        
        remaining = await db["leads"].count_documents({})
        print(f"📊 Remaining Leads: {remaining}")
        
        # Show sample of remaining leads
        print("\n📋 Sample Remaining Leads:")
        cursor = db["leads"].find().limit(3)
        leads = await cursor.to_list(length=3)
        
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. {lead.get('company_name')}")
            print(f"   Industry: {lead.get('industry')}")
            print(f"   Segment: {lead.get('segment')}")
            print(f"   Role: {lead.get('job_role')}")
            print(f"   Quote: ${lead.get('quote_value', 0):,}")
    
    elif choice == "2":
        print("\n✅ Sample Good Leads:")
        cursor = db["leads"].find({
            "segment": {"$exists": True, "$ne": None},
            "job_role": {"$exists": True, "$ne": None}
        }).limit(10)
        leads = await cursor.to_list(length=10)
        
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. {lead.get('company_name')}")
            print(f"   Email: {lead.get('email')}")
            print(f"   Role: {lead.get('job_role')}")
            print(f"   Industry: {lead.get('industry')}")
            print(f"   Segment: {lead.get('segment')}")
            print(f"   Quote: ${lead.get('quote_value', 0):,}")
            print(f"   Decision Maker: {lead.get('is_decision_maker', False)}")
    
    elif choice == "3":
        print("\n❌ Sample Bad Leads:")
        cursor = db["leads"].find({
            "$or": [
                {"segment": None},
                {"segment": {"$exists": False}}
            ]
        }).limit(5)
        leads = await cursor.to_list(length=5)
        
        for i, lead in enumerate(leads, 1):
            print(f"\n{i}. {lead.get('company_name')}")
            print(f"   Email: {lead.get('email')}")
            print(f"   Segment: {lead.get('segment')}")
            print(f"   Industry: {lead.get('industry')}")
            print(f"   Role: {lead.get('job_role')}")
    
    elif choice == "4":
        confirm = input("\n⚠️ DELETE ALL LEADS? Type 'yes' to confirm: ").strip().lower()
        if confirm == "yes":
            result = await db["leads"].delete_many({})
            print(f"\n✅ Deleted {result.deleted_count} leads")
            print("💡 Run 'python auto_generate_leads.py' to create new data")
        else:
            print("❌ Cancelled")
    
    else:
        print("\n👋 No changes made")
    
    client.close()
    print("\n" + "="*60)


if __name__ == "__main__":
    asyncio.run(clean_mongodb())
