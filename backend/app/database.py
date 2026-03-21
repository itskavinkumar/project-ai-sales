import os
import motor.motor_asyncio
from dotenv import load_dotenv

load_dotenv()

# MongoDB Configuration
MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "ai_sales_db")

class Database:
    client: motor.motor_asyncio.AsyncIOMotorClient = None
    db = None

    def connect(self):
        """Connect to MongoDB."""
        try:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
            self.db = self.client[DB_NAME]
            print(f"✅ Connected to MongoDB: {DB_NAME}")
        except Exception as e:
            print(f"❌ MongoDB Connection Error: {e}")

    def close(self):
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            print("❌ Closed MongoDB connection")

    # --- CRUD Operations ---

    async def get_all_leads(self, limit=1000):
        if self.db is None: return []
        cursor = self.db["leads"].find().limit(limit)
        return await cursor.to_list(length=limit)

    async def save_lead(self, lead_data: dict):
        if self.db is None: return
        # Update if exists, insert if new (Upsert)
        await self.db["leads"].update_one(
            {"email": lead_data["email"]},
            {"$set": lead_data},
            upsert=True
        )

    async def get_use_cases(self):
        if self.db is None: return []
        cursor = self.db["use_cases"].find()
        return await cursor.to_list(length=100)

    async def seed_use_cases(self, use_cases_list):
        """Populate DB with initial use cases if empty"""
        if self.db is None: return
        count = await self.db["use_cases"].count_documents({})
        if count == 0:
            await self.db["use_cases"].insert_many(use_cases_list)
            print("✅ Seeded initial Use Cases to MongoDB")

    async def save_campaign(self, campaign_data: dict):
        """Save email campaign"""
        if self.db is None: return
        result = await self.db["campaigns"].insert_one(campaign_data)
        campaign_data["_id"] = str(result.inserted_id)
        return campaign_data

    async def get_all_campaigns(self):
        """Fetch all campaigns"""
        if self.db is None: return []
        cursor = self.db["campaigns"].find()
        return await cursor.to_list(length=100)

    async def update_campaign_status(self, campaign_id: str, status: str, emails_sent: int = 0):
        """Update campaign progress"""
        if self.db is None: return
        from bson import ObjectId
        await self.db["campaigns"].update_one(
            {"_id": ObjectId(campaign_id)},
            {"$set": {"status": status, "emails_sent": emails_sent}}
        )

db = Database()
