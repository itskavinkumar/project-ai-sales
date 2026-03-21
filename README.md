# AI-Powered Outbound Sales Platform 🚀

> An intelligent lead management and email campaign system that automatically scores, segments, and engages B2B prospects using AI

## 📋 Table of Contents
- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Installation Guide](#installation-guide)
- [Data Generation](#data-generation)
- [System Architecture](#system-architecture)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Multi-System Deployment](#multi-system-deployment)
- [Troubleshooting](#troubleshooting)
- [Configuration](#configuration)

---

## Overview

This platform automates the entire outbound sales workflow from lead scoring to personalized email campaigns. It combines machine learning with business rules to identify high-value prospects and generates customized outreach emails using AI.

**Key Capabilities:**
- 🎯 Intelligent lead scoring (0-100% scale)
- 📊 Multi-dimensional segmentation (Enterprise, Mid-Market, SMB, Startup)
- 📧 AI-powered personalized email generation (LLaMA 3.1)
- 📈 Real-time analytics and conversion tracking
- 🔄 Automated campaign scheduling
- 💼 CRM integration ready

---

## Problem Statement

**Original Challenge:**
- **228 leads in database but only 100 displaying** in frontend (pagination issue)
- **All lead scores showing 0%** preventing email campaign functionality
- **No high-value leads available** for targeted outreach (requires score >60%)
- **Manual lead qualification** consuming excessive sales team time

**Solution Delivered:**
- ✅ Fixed pagination: Now displays all leads (up to 1,000)
- ✅ Implemented hybrid scoring algorithm: 161 high-value leads (>70%), 65 medium (40-70%), 2 low (<40%)
- ✅ Automated lead enrichment with AI segmentation
- ✅ Email campaign system with 161 qualified prospects ready for outreach

---

## Features

### 🎯 Lead Management
- **Smart Lead Scoring:** Hybrid algorithm combining ML predictions with business rules
  - Deal size analysis (15-50 base points)
  - Decision-maker identification (+25 points)
  - Segment classification (+10 points)
  - Engagement history (+5-10 points)
  - Item count analysis (+5 points)
  - ML contribution (+5-15 points)
- **Real-time Filtering:** Filter by score, segment, industry, region
- **Bulk Import:** CSV upload with automatic data validation
- **Lead Enrichment:** AI-powered segmentation and categorization

### 📧 Email Campaigns
- **AI Email Generation:** Personalized emails using LLaMA 3.1 via Groq
- **Template Variables:** Dynamic content insertion (name, company, pain points)
- **High-Value Targeting:** Automatic filtering of leads with score >60%
- **Bulk Sending:** Send to multiple prospects simultaneously
- **Campaign Tracking:** Monitor open rates, clicks, and responses

### 📊 Analytics Dashboard
- **Score Distribution:** Visual breakdown (High/Medium/Low categories)
- **Segment Analysis:** Performance by Enterprise/Mid-Market/SMB/Startup
- **Conversion Funnel:** Track leads through qualification stages
- **Revenue Forecasting:** Deal value projections based on lead scores

### 🔄 Automation
- **Scheduled Campaigns:** Run email campaigns at optimal times
- **Lead Scoring Updates:** Automatic recalculation based on new data
- **Follow-up Sequences:** Timed multi-touch campaigns

---

## Tech Stack

### Backend
- **Framework:** FastAPI (Python 3.11+)
- **Database:** MongoDB (Motor async driver)
- **ML Model:** Scikit-learn LogisticRegression
- **AI:** LLaMA 3.1 via Groq API
- **Email:** SMTP with TLS encryption
- **Scheduler:** APScheduler for automation
- **Environment:** Python-dotenv

### Frontend
- **Framework:** React 18 with TypeScript
- **Build Tool:** Vite
- **Styling:** Tailwind CSS
- **State Management:** React Hooks
- **HTTP Client:** Axios
- **Icons:** Lucide React

### DevOps
- **API Server:** Uvicorn ASGI server
- **CORS:** Enabled for localhost development
- **Hot Reload:** Both backend and frontend support live updates

---

## Prerequisites

Before installation, ensure you have:

1. **Python 3.11+** - [Download](https://www.python.org/downloads/)
2. **Node.js 18+** and npm - [Download](https://nodejs.org/)
3. **MongoDB Community Edition** - [Download](https://www.mongodb.com/try/download/community)
   - Must be running on `localhost:27017`
   - No authentication required for local development
4. **Groq API Key** - [Get Free Key](https://console.groq.com/)
   - Free tier: 30 requests/minute, 14,400 requests/day
5. **Git** (optional) - For cloning the repository

**System Requirements:**
- OS: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- RAM: 4GB minimum (8GB recommended)
- Storage: 500MB free space
- Internet: Required for AI email generation

---

## Quick Start

Get up and running in 5 minutes:

```bash
# 1. Start MongoDB (ensure it's running on localhost:27017)
# Windows: MongoDB should auto-start as a service
# macOS: brew services start mongodb-community
# Linux: sudo systemctl start mongod

# 2. Backend Setup
cd backend
pip install -r requirements.txt
python auto_generate_leads.py  # Generates 200 sample leads
uvicorn app.main:app --reload  # Starts on http://localhost:8000

# 3. Frontend Setup (in new terminal)
cd Frontend
npm install
npm run dev  # Starts on http://localhost:5173

# 4. Access Application
# Open browser: http://localhost:5173
```

**Default Login:** No authentication required for development mode

---

## Installation Guide

### Step 1: Install MongoDB

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Run installer with default settings (installs as Windows Service)
3. MongoDB will auto-start on `localhost:27017`
4. Verify: Open Command Prompt and run `mongosh` (should connect successfully)

#### macOS
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
mongosh  # Test connection
```

#### Linux (Ubuntu/Debian)
```bash
wget -qO - https://www.mongodb.org/static/pgp/server-7.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/7.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-7.0.list
sudo apt update
sudo apt install -y mongodb-org
sudo systemctl start mongod
mongosh  # Test connection
```

### Step 2: Clone/Download Project

```bash
# If using Git
git clone <repository-url>
cd Outbound

# Or download ZIP and extract
```

### Step 3: Backend Installation

```bash
cd backend

# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -c "import fastapi, motor, sklearn, groq; print('✓ All packages installed')"
```

### Step 4: Frontend Installation

```bash
cd ../Frontend

# Install Node dependencies
npm install

# Verify installation
npm list react typescript vite
```

### Step 5: Configuration

Create `.env` file in `backend/` directory:

```env
# MongoDB Configuration
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_sales_db

# Groq API (for AI email generation)
GROQ_API_KEY=your_groq_api_key_here

# Email Configuration (optional - for sending emails)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password

# Application Settings
CORS_ORIGINS=http://localhost:5173
```

**Get Groq API Key:**
1. Visit [console.groq.com](https://console.groq.com/)
2. Sign up (free tier available)
3. Navigate to API Keys section
4. Create new key and copy to `.env` file

---

## Data Generation

### Option 1: Auto-Generate Sample Data (Recommended)

```bash
cd backend
python auto_generate_leads.py
```

**What it does:**
- Creates **200 realistic B2B leads** with diverse characteristics
- Generates company names, contacts, deal values ($10K-$500K)
- Assigns job roles (CEO, CTO, CFO, CMO, VP Sales, etc.)
- Includes regional distribution (North America, Europe, Asia-Pacific)
- Adds engagement history and item counts
- Automatically calculates lead scores and conversion probabilities

**Output:**
```
✓ Generated 200 leads
✓ Stored in MongoDB (ai_sales_db.leads)
✓ Score distribution:
  - High (>70%): ~140 leads
  - Medium (40-70%): ~55 leads
  - Low (<40%): ~5 leads
```

### Option 2: Import CSV Data

1. Prepare CSV file with columns:
   ```csv
   company_name,contact_name,email,job_role,quote_value,region,items_count,past_engagements
   ```

2. Upload via frontend:
   - Navigate to "Lead Management" page
   - Click "Import CSV" button
   - Select your file
   - Leads will be automatically scored and enriched

### Option 3: API Upload

```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corp",
    "contact_name": "John Doe",
    "email": "john@acme.com",
    "job_role": "CTO",
    "quote_value": 250000,
    "region": "North America",
    "items_count": 15,
    "past_engagements": 3
  }'
```

---

## System Architecture

```
┌─────────────────┐         ┌──────────────────┐         ┌─────────────────┐
│                 │         │                  │         │                 │
│  React Frontend │◄───────►│  FastAPI Backend │◄───────►│    MongoDB      │
│  (Port 5173)    │  REST   │  (Port 8000)     │  Motor  │  (Port 27017)   │
│                 │   API   │                  │  Async  │                 │
└─────────────────┘         └──────────────────┘         └─────────────────┘
                                     │
                                     │
                        ┌────────────┼─────────────┐
                        │            │             │
                        ▼            ▼             ▼
                 ┌────────────┐ ┌─────────┐ ┌──────────┐
                 │   Groq AI  │ │   ML    │ │  SMTP    │
                 │  (LLaMA)   │ │ Scoring │ │  Email   │
                 └────────────┘ └─────────┘ └──────────┘
```

### Data Flow

1. **Lead Enrichment:**
   ```
   Raw Lead → Business Rules → ML Model → Hybrid Score → MongoDB
   ```

2. **Email Campaign:**
   ```
   High-Value Leads (>60%) → AI Prompt → LLaMA 3.1 → Personalized Email → SMTP → Send
   ```

3. **Scoring Algorithm:**
   ```python
   Base Score (15-50)      # Deal size tiers
   + Decision Maker (+25)  # CXO/VP roles
   + Segment (+10)         # Enterprise/Mid-Market
   + Engagements (+5-10)   # Past interactions
   + Items (+5)            # Quote complexity
   + ML Contribution (+5-15) # Model prediction
   ─────────────────────
   = Hybrid Score (0-100)
   ÷ 100 = Final Score (0-1 scale)
   ```

### Database Schema

**leads Collection:**
```json
{
  "_id": "ObjectId",
  "company_name": "string",
  "contact_name": "string",
  "email": "string",
  "job_role": "string",
  "quote_value": "number",
  "region": "string",
  "items_count": "number",
  "past_engagements": "number",
  "lead_score": "decimal (0-1)",  // Used by frontend
  "conversion_probability": "decimal (0-1)",
  "segment": "string",  // Enterprise/Mid-Market/SMB/Startup
  "created_at": "datetime"
}
```

---

## API Documentation

### Base URL
```
http://localhost:8000
```

### Endpoints

#### 1. Get All Leads
```http
GET /leads
```

**Response:**
```json
[
  {
    "_id": "65f1a2b3c4d5e6f7g8h9i0j1",
    "company_name": "FinTech Capital Partners",
    "contact_name": "Sarah Johnson",
    "email": "sarah.johnson@fintechcap.com",
    "job_role": "CFO",
    "quote_value": 350000,
    "region": "North America",
    "items_count": 25,
    "past_engagements": 5,
    "lead_score": 0.95,
    "conversion_probability": 0.78,
    "segment": "Enterprise"
  }
]
```

#### 2. Create New Lead
```http
POST /leads
Content-Type: application/json
```

**Request Body:**
```json
{
  "company_name": "Tech Innovations Inc",
  "contact_name": "Mike Chen",
  "email": "mike@techinnovations.com",
  "job_role": "CTO",
  "quote_value": 180000,
  "region": "Asia-Pacific",
  "items_count": 12,
  "past_engagements": 2
}
```

**Response:**
```json
{
  "message": "Lead created successfully",
  "lead_id": "65f1a2b3c4d5e6f7g8h9i0j2",
  "lead_score": 0.82
}
```

#### 3. Get Single Lead
```http
GET /leads/{lead_id}
```

#### 4. Update Lead
```http
PUT /leads/{lead_id}
Content-Type: application/json
```

#### 5. Delete Lead
```http
DELETE /leads/{lead_id}
```

#### 6. Generate AI Email
```http
POST /generate-email
Content-Type: application/json
```

**Request Body:**
```json
{
  "lead_id": "65f1a2b3c4d5e6f7g8h9i0j1",
  "template": "product_launch",
  "tone": "professional"
}
```

**Response:**
```json
{
  "subject": "Exclusive Early Access: Transform Your Sales Process",
  "body": "Hi Sarah,\n\nI noticed FinTech Capital Partners...",
  "estimated_read_time": "2 minutes"
}
```

#### 7. Send Email Campaign
```http
POST /send-campaign
Content-Type: application/json
```

**Request Body:**
```json
{
  "lead_ids": ["id1", "id2", "id3"],
  "subject": "Custom subject line",
  "body": "Email content with {{company_name}} variables"
}
```

#### 8. Recalculate Lead Scores
```http
POST /recalculate-scores
```

**Response:**
```json
{
  "message": "Recalculated 228 leads",
  "distribution": {
    "high": 161,
    "medium": 65,
    "low": 2
  }
}
```

---

## Usage Guide

### 1. Dashboard Overview

Navigate to `http://localhost:5173` after starting both servers.

**Dashboard Features:**
- **Total Leads:** Current database count
- **High-Value Leads:** Count of leads with score >70%
- **Conversion Rate:** Average lead score across all prospects
- **Total Revenue Potential:** Sum of quote_value for high-value leads

**Score Distribution Chart:**
- Green: High (>70%) - Priority targets
- Yellow: Medium (40-70%) - Nurture campaigns
- Red: Low (<40%) - Re-qualification needed

### 2. Lead Management

**Viewing Leads:**
- All leads display with color-coded scores
- Green badge: High-value (>70%)
- Yellow badge: Medium (40-70%)
- Red badge: Low (<40%)

**Filtering:**
- Click "Filter" dropdown to narrow by:
  - Score range (High/Medium/Low)
  - Segment (Enterprise/Mid-Market/SMB/Startup)
  - Region (North America/Europe/Asia-Pacific)
  - Deal size ($0-$50K, $50K-$150K, $150K+)

**Lead Details:**
- Click any lead card to view full profile
- Edit fields directly (auto-saves)
- Rescore button to recalculate with new data

### 3. Email Campaigns

**Starting a Campaign:**

1. Navigate to "Email Campaign" page
2. System automatically loads leads with score >60%
3. Select recipients:
   - "Select All" for bulk campaigns
   - Manual selection for targeted outreach
4. Click "Generate AI Email"
5. Review personalized content
6. Edit subject line or body as needed
7. Click "Send Campaign"

**AI Email Generation:**
- Powered by LLaMA 3.1 (via Groq)
- Personalization variables:
  - `{{contact_name}}` - Recipient's name
  - `{{company_name}}` - Company name
  - `{{job_role}}` - Their position
  - `{{pain_point}}` - Industry-specific challenge
  - `{{quote_value}}` - Deal size context

**Example Generated Email:**
```
Subject: Sarah, streamline FinTech Capital Partners' sales process

Hi Sarah,

As CFO of FinTech Capital Partners, you understand the importance 
of maximizing ROI on every sales initiative. I noticed your team 
is evaluating solutions in the $350K range.

Our AI-powered platform has helped similar enterprise clients:
- Reduce sales cycle by 40%
- Increase conversion rates by 28%
- Automate 60% of lead qualification

Would you be open to a 15-minute call next week to explore how 
we can deliver similar results for FinTech Capital Partners?

Best regards,
[Your Name]
```

### 4. Analytics

**Segment Performance:**
- Enterprise: 45 leads, 85% avg score
- Mid-Market: 98 leads, 68% avg score
- SMB: 72 leads, 54% avg score
- Startup: 13 leads, 42% avg score

**Regional Analysis:**
- North America: Highest engagement (72% avg score)
- Europe: Moderate engagement (61% avg score)
- Asia-Pacific: Growing market (58% avg score)

**Export Reports:**
- Click "Export CSV" to download filtered data
- Includes all fields plus calculated scores
- Use for external CRM imports or analysis

---

## Multi-System Deployment

### Deploying on Multiple Computers

Each system runs **independently** with its own local MongoDB database. Data does NOT automatically sync between computers.

**Setup Process for Each Computer:**

#### Computer A (Your System)
```bash
# Already set up with 228 leads
# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# MongoDB: localhost:27017/ai_sales_db
```

#### Computer B (Friend's System)

1. **Install Prerequisites:**
   - Python 3.11+
   - Node.js 18+
   - MongoDB Community Edition
   - Get Groq API key

2. **Copy Project Files:**
   ```bash
   # Option 1: Git clone
   git clone <repository-url>
   
   # Option 2: Copy entire Outbound folder via USB/cloud
   ```

3. **Start MongoDB:**
   ```bash
   # Windows: Should auto-start
   # macOS: brew services start mongodb-community
   # Linux: sudo systemctl start mongod
   ```

4. **Backend Setup:**
   ```bash
   cd backend
   pip install -r requirements.txt
   
   # Generate fresh data (200 leads)
   python auto_generate_leads.py
   
   # Start server
   uvicorn app.main:app --reload
   ```

5. **Frontend Setup:**
   ```bash
   cd Frontend
   npm install
   npm run dev
   ```

6. **Access Application:**
   - Open browser: `http://localhost:5173`
   - Computer B now has its own 200 leads
   - Completely independent from Computer A

**Data Isolation:**
- ✅ Each computer has separate MongoDB database
- ✅ Leads generated/imported are local only
- ✅ Email campaigns sent from each system are independent
- ❌ No automatic data synchronization
- ❌ Changes on Computer A don't affect Computer B

**Sharing Data Between Systems:**

If you need to sync data:

1. **Export from Computer A:**
   ```bash
   cd backend
   mongoexport --db=ai_sales_db --collection=leads --out=leads_export.json
   ```

2. **Transfer File:**
   - Copy `leads_export.json` via USB, email, or cloud storage

3. **Import to Computer B:**
   ```bash
   cd backend
   mongoimport --db=ai_sales_db --collection=leads --file=leads_export.json
   ```

---

## Troubleshooting

### Common Issues and Solutions

#### 1. Frontend Shows "No high-value leads available"

**Symptom:** Email Campaign page displays no leads even though database has data.

**Causes:**
- All lead scores are below 60% threshold
- Backend not running or API connection failed
- Frontend cache showing old data

**Solutions:**
```bash
# Check lead scores in database
cd backend
python -c "
from pymongo import MongoClient
client = MongoClient('mongodb://localhost:27017/')
db = client['ai_sales_db']
high = db.leads.count_documents({'lead_score': {'$gt': 0.6}})
print(f'High-value leads: {high}')
"

# If count is 0, recalculate scores
python recalculate_scores.py

# Refresh frontend (hard refresh)
# Press Ctrl+Shift+R in browser
```

#### 2. Lead Scores Showing as 5000% or Other Invalid Values

**Symptom:** Lead scores display as percentages over 100%.

**Root Cause:** Backend returning score in 0-100 scale, but frontend expects 0-1 scale.

**Solution:**
Verify [segmentation.py](backend/app/segmentation.py) returns scores divided by 100:
```python
# Correct implementation
return hybrid_score / 100  # Returns 0-1 scale
```

Then recalculate:
```bash
cd backend
python recalculate_scores.py
```

#### 3. MongoDB Connection Failed

**Symptom:** 
```
pymongo.errors.ServerSelectionTimeoutError: localhost:27017
```

**Solutions:**

**Windows:**
```bash
# Check if MongoDB service is running
services.msc  # Look for "MongoDB Server"

# If not running, start it
net start MongoDB
```

**macOS:**
```bash
brew services start mongodb-community
# Or manually:
mongod --config /usr/local/etc/mongod.conf
```

**Linux:**
```bash
sudo systemctl status mongod
sudo systemctl start mongod
```

#### 4. Frontend Shows Only 100 Leads (Pagination Issue)

**Symptom:** Database has 228 leads but frontend displays 100.

**Root Cause:** Backend query limit set too low.

**Solution:**
Check [database.py](backend/app/database.py):
```python
async def get_all_leads(limit: int = 1000):  # Should be 1000, not 100
```

#### 5. AI Email Generation Fails

**Symptom:**
```
Error generating email: 401 Unauthorized
```

**Causes:**
- Invalid or missing Groq API key
- API rate limit exceeded
- Network connection issue

**Solutions:**

1. **Verify API Key:**
```bash
# Check .env file
cat backend/.env | grep GROQ_API_KEY

# Test API key
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.groq.com/v1/models
```

2. **Check Rate Limits:**
   - Free tier: 30 requests/minute, 14,400/day
   - Wait 60 seconds and retry
   - Upgrade to paid tier if needed

3. **Alternative:** Use template-based emails without AI:
   - Email Campaign page has "Use Template" option
   - Manually edit `{{variables}}` in email body

#### 6. Email Sending Fails (SMTP Error)

**Symptom:**
```
SMTPAuthenticationError: Username and Password not accepted
```

**Solutions:**

**Gmail Users:**
1. Enable 2-factor authentication on Google account
2. Generate App-Specific Password:
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy 16-character password to `.env`:
   ```env
   EMAIL_PASSWORD=abcd efgh ijkl mnop
   ```

**Other Providers:**
- Outlook: `smtp.office365.com:587`
- Yahoo: `smtp.mail.yahoo.com:587`
- Custom SMTP: Check provider documentation

#### 7. Module Not Found Errors

**Symptom:**
```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution:**
```bash
cd backend

# Verify virtual environment is activated
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Verify installation
pip list | grep fastapi
```

#### 8. Port Already in Use

**Symptom:**
```
Error: Port 8000 is already in use
```

**Solutions:**

**Windows:**
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID 12345 /F
```

**macOS/Linux:**
```bash
# Find and kill process
lsof -ti:8000 | xargs kill -9
```

**Alternative:** Use different port:
```bash
uvicorn app.main:app --reload --port 8001
```

Update frontend API URL in `src/services/api.ts`:
```typescript
const API_BASE_URL = 'http://localhost:8001';
```

#### 9. Frontend Build Errors

**Symptom:**
```
Error: Cannot find module '@vitejs/plugin-react'
```

**Solution:**
```bash
cd Frontend

# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install

# Clear Vite cache
rm -rf node_modules/.vite

# Retry
npm run dev
```

#### 10. Scores Not Updating After Data Changes

**Symptom:** Changed lead data (e.g., quote_value) but score remains the same.

**Solution:**
Scores are calculated once and stored. After data changes, run:
```bash
cd backend
python recalculate_scores.py
```

**Automatic Recalculation:**
To enable automatic score updates when data changes, add to [main.py](backend/app/main.py):
```python
@app.put("/leads/{lead_id}")
async def update_lead(lead_id: str, lead: LeadUpdate):
    # Update lead data
    await update_lead_in_db(lead_id, lead)
    
    # Recalculate score
    enriched = await enrich_lead_data(lead)
    await update_score_in_db(lead_id, enriched['lead_score'])
```

---

## Configuration

### Environment Variables

Create `backend/.env` file with these settings:

```env
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# DATABASE CONFIGURATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MONGODB_URL=mongodb://localhost:27017
DATABASE_NAME=ai_sales_db

# For MongoDB Atlas (cloud):
# MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/
# DATABASE_NAME=production_sales_db

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# AI CONFIGURATION
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GROQ_API_KEY=your_groq_api_key_here

# Model selection (optional, defaults to llama-3.1-70b-versatile)
GROQ_MODEL=llama-3.1-70b-versatile

# Alternative models:
# GROQ_MODEL=llama-3.1-8b-instant  # Faster, lower quality
# GROQ_MODEL=mixtral-8x7b-32768    # Longer context

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# EMAIL CONFIGURATION (Optional)
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USER=your_email@gmail.com
EMAIL_PASSWORD=your_app_specific_password
EMAIL_FROM_NAME=Sales Team

# For testing without sending real emails:
# EMAIL_ENABLED=false

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# APPLICATION SETTINGS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CORS_ORIGINS=http://localhost:5173,http://localhost:5174
DEBUG=true

# Production settings:
# CORS_ORIGINS=https://yourdomain.com
# DEBUG=false

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCORING THRESHOLDS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HIGH_SCORE_THRESHOLD=0.7    # 70%+
MEDIUM_SCORE_THRESHOLD=0.4  # 40-70%
EMAIL_CAMPAIGN_THRESHOLD=0.6  # 60%+ for campaigns

#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SCHEDULER SETTINGS
#━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ENABLE_SCHEDULER=true
SCORE_UPDATE_INTERVAL=3600  # Seconds (3600 = 1 hour)
CAMPAIGN_CHECK_INTERVAL=86400  # Seconds (86400 = 24 hours)
```

### Frontend Configuration

Update `Frontend/src/services/api.ts` if backend URL changes:

```typescript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// For production:
// const API_BASE_URL = 'https://api.yourdomain.com';
```

### Scoring Algorithm Tuning

Adjust scoring weights in `backend/app/segmentation.py`:

```python
# Current Configuration (lines 145-195)
SCORING_CONFIG = {
    'deal_size_tiers': {
        'tier_1': {'threshold': 300000, 'points': 50},
        'tier_2': {'threshold': 150000, 'points': 40},
        'tier_3': {'threshold': 75000, 'points': 35},
        'tier_4': {'threshold': 30000, 'points': 25},
        'tier_5': {'threshold': 0, 'points': 15}
    },
    'decision_maker_boost': 25,  # CXO/VP roles
    'segment_boost': 10,          # Enterprise/Mid-Market
    'engagement_max_boost': 10,   # Past interactions
    'item_count_boost': 5,        # Quote complexity
    'ml_max_contribution': 15     # ML model prediction
}
```

**To emphasize deal size over other factors:**
```python
'deal_size_tiers': {
    'tier_1': {'threshold': 300000, 'points': 60},  # Increased
    # ... adjust other tiers
}
'decision_maker_boost': 15,  # Decreased from 25
```

**To weight ML predictions higher:**
```python
'ml_max_contribution': 25  # Increased from 15
```

---

## Performance Optimization

### Database Indexing

Add indexes for faster queries:

```javascript
// Connect to MongoDB shell
mongosh

use ai_sales_db;

// Create indexes
db.leads.createIndex({ "lead_score": -1 });
db.leads.createIndex({ "segment": 1, "lead_score": -1 });
db.leads.createIndex({ "email": 1 }, { unique: true });
db.leads.createIndex({ "company_name": 1 });

// Verify indexes
db.leads.getIndexes();
```

### API Response Caching

Add caching for frequently accessed data:

```python
# In backend/app/main.py
from functools import lru_cache

@lru_cache(maxsize=128)
async def get_cached_analytics():
    # Expensive computation
    return analytics_data
```

### Frontend Optimization

```typescript
// In Frontend/src/components/LeadManagement.tsx
// Implement pagination for large datasets
const LEADS_PER_PAGE = 50;
```

---

## Security Considerations

### Production Deployment

1. **Enable Authentication:**
   - Implement JWT tokens for API access
   - Add user login system

2. **Environment Variables:**
   - Never commit `.env` files to Git
   - Use secrets management for production (AWS Secrets Manager, Azure Key Vault)

3. **CORS Configuration:**
   ```python
   # Restrict to specific domain
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://yourdomain.com"],
       # ... other settings
   )
   ```

4. **MongoDB Security:**
   - Enable authentication: `mongod --auth`
   - Create database users with limited permissions
   - Use MongoDB Atlas for cloud hosting with built-in security

5. **API Rate Limiting:**
   ```python
   from slowapi import Limiter
   
   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   
   @app.get("/leads")
   @limiter.limit("100/minute")
   async def get_leads():
       # ...
   ```

---

## Support and Contributions

### Getting Help

- **GitHub Issues:** Report bugs or request features
- **Documentation:** This README covers 95% of use cases
- **Community:** Join discussions in project forums

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open Pull Request

---

## License

This project is licensed under the MIT License - see LICENSE file for details.

---

## Changelog

### Version 1.0.0 (Current)

**Features:**
- ✅ Hybrid lead scoring algorithm (ML + business rules)
- ✅ AI-powered email generation (LLaMA 3.1)
- ✅ Multi-segment classification (Enterprise/Mid-Market/SMB/Startup)
- ✅ Real-time analytics dashboard
- ✅ Bulk email campaigns
- ✅ Auto lead generation script (200 sample leads)
- ✅ CSV import/export

**Bug Fixes:**
- Fixed pagination issue (100 → 1,000 lead limit)
- Fixed all lead scores showing 0%
- Fixed score display bug (5000% → correct percentage)
- Fixed ML model scale mismatch (0-100 vs 0-1)

**Known Issues:**
- Scikit-learn version mismatch warning (1.7.2 vs 1.6.1) - non-critical
- Email sending requires app-specific password for Gmail
- Frontend requires hard refresh (Ctrl+Shift+R) after score recalculation

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════╗
║  AI-POWERED OUTBOUND SALES PLATFORM - QUICK COMMANDS     ║
╠══════════════════════════════════════════════════════════╣
║  START MONGODB                                           ║
║    Windows: Auto-starts as service                       ║
║    macOS:   brew services start mongodb-community        ║
║    Linux:   sudo systemctl start mongod                  ║
╠══════════════════════════════════════════════════════════╣
║  START BACKEND (from backend/ directory)                 ║
║    uvicorn app.main:app --reload                         ║
║    Access: http://localhost:8000                         ║
║    Docs:   http://localhost:8000/docs                    ║
╠══════════════════════════════════════════════════════════╣
║  START FRONTEND (from Frontend/ directory)               ║
║    npm run dev                                           ║
║    Access: http://localhost:5173                         ║
╠══════════════════════════════════════════════════════════╣
║  GENERATE SAMPLE DATA                                    ║
║    python auto_generate_leads.py                         ║
║    (Creates 200 realistic B2B leads)                     ║
╠══════════════════════════════════════════════════════════╣
║  RECALCULATE SCORES                                      ║
║    python recalculate_scores.py                          ║
║    (Updates all lead scores in MongoDB)                  ║
╠══════════════════════════════════════════════════════════╣
║  VIEW DATABASE STATS                                     ║
║    mongosh                                               ║
║    use ai_sales_db                                       ║
║    db.leads.countDocuments()                             ║
╠══════════════════════════════════════════════════════════╣
║  HARD REFRESH FRONTEND                                   ║
║    Windows/Linux: Ctrl + Shift + R                       ║
║    macOS: Cmd + Shift + R                                ║
╠══════════════════════════════════════════════════════════╣
║  SCORE CATEGORIES                                        ║
║    High:   >70%  (Green) - Email campaign targets        ║
║    Medium: 40-70% (Yellow) - Nurture campaigns           ║
║    Low:    <40%  (Red) - Re-qualification needed         ║
╠══════════════════════════════════════════════════════════╣
║  KEY FILES                                               ║
║    Backend:  backend/app/main.py                         ║
║    Scoring:  backend/app/segmentation.py                 ║
║    Frontend: Frontend/src/App.tsx                        ║
║    Config:   backend/.env                                ║
╚══════════════════════════════════════════════════════════╝
```

---

**Built with ❤️ for sales teams who want to work smarter, not harder.**

Last Updated: February 7, 2026
