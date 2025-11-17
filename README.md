# Marketing Data to Supabase - Zero Data Loss

Process your **Google Ads** and **TikTok Ads** CSV exports and store them in Supabase with **100% data preservation**.

## 📊 Supported Platforms

- ✅ **Google Ads** - Performance & conversion data
- ✅ **TikTok Ads** - Campaign performance & video metrics
- ✅ **Meta Ads** - Campaign performance & video metrics
- ✅ **Power BI** - Store sales data (LFL Sales)

## 🎯 Two Versions Available

### ⚡ **Simple Version** (RECOMMENDED TO START)
- ✅ **Fast & Easy** - No embeddings, no Google API needed
- ✅ **Zero Data Loss** - 100% preservation
- ✅ **Only 2 credentials** - Just Supabase URL & Key
- ✅ **10x faster** - Process 3,000 rows in ~5-10 minutes
- 👉 **[START HERE: SIMPLE_SETUP.md](SIMPLE_SETUP.md)**

### 🤖 **Full Version** (With AI Embeddings)
- ✅ **Zero Data Loss** + Vector Embeddings
- ✅ **AI-Ready** - Semantic search capabilities
- ✅ **3 credentials** - Supabase + Google Gemini
- ⏱️ **Slower** - ~25-40 minutes for 3,000 rows
- 📖 See instructions below

## 📦 What Gets Stored

For each CSV row, you get **4 layers of data**:

```
1. Raw Original Data   → Exact CSV values (with commas, %, etc.)
2. Processed Metadata  → Cleaned for SQL queries
3. Text Content        → Human-readable summary
4. Vector Embedding    → 768-dim for semantic search
```

**Example:**

```json
{
  "raw_data": {
    "original_row": {
      "Day": "2024-11-01",
      "Campaign": "[WHD] Display - Atlanta USA",
      "Impr.": "1,618",     // ← Original with comma
      "CTR": "1.85%",       // ← Original with %
      ...all 13 columns
    }
  },
  "metadata": {
    "day": "2024-11-01",
    "campaign": "[WHD] Display - Atlanta USA",
    "impressions": 1618,    // ← Cleaned for queries
    "ctr": 1.85,            // ← Cleaned for queries
    ...all fields typed
  },
  "embedding": [0.123, -0.456, ...]  // ← 768 dimensions
}
```

---

## ⚡ SIMPLE VERSION (Recommended)

**No embeddings, just data storage - fast and easy!**

### Quick Start

```bash
# 1. Install
pip install -r requirements_simple.txt

# 2. Setup Supabase (run setup_supabase_simple.sql)

# 3. Create .env with just 2 credentials:
SUPABASE_URL=your_url
SUPABASE_KEY=your_key

# 4. Test
python test_setup_simple.py

# 5. Process
python process_google_ads_simple.py
```

**📖 Full instructions:** [SIMPLE_SETUP.md](SIMPLE_SETUP.md)

---

## 🤖 FULL VERSION (With Embeddings)

**Includes vector embeddings for AI/RAG applications**

### Quick Start

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Set Up Supabase

1. Go to your Supabase project
2. Click **"SQL Editor"** in left sidebar
3. Click **"+ New query"** and paste contents of `setup_supabase_enhanced.sql`
4. Click **"Run"**

**📖 Need help running SQL? See [HOW_TO_RUN_SQL.md](HOW_TO_RUN_SQL.md)**

This creates the `google_ads_documents` table with vector embedding support.

### Step 3: Configure Environment

Create a `.env` file:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
GOOGLE_API_KEY=AIzaSyD...
```

**📖 Need help getting credentials?**
- **Supabase**: Settings → API → Project URL & anon/public key
- **Google Gemini**: [AI Studio](https://makersuite.google.com/app/apikey)
- **Detailed guide**: [CREDENTIALS_GUIDE.md](CREDENTIALS_GUIDE.md)

### Step 4: Test Setup

```bash
python test_setup.py
```

Should see all ✅ green checkmarks.

### Step 5: Process Your Data

```bash
python process_google_ads_zero_loss.py
```

This will:
- Read all CSV files from `NBX/Google Ads Export/`
- Store raw original data (100% preservation)
- Create processed metadata (for queries)
- Generate embeddings (for AI search)
- Store everything in Supabase

**Time:** ~25-40 minutes for ~3,000 rows (includes API rate limiting)

## 📊 Data Sources Supported

### Performance Files
`google_ads_performance_*.csv` - 13 properties per row:
- Day, Campaign, Campaign type, Ad group, Landing page
- Currency code, Cost, Impressions, Clicks
- CTR, Avg. CPC, Conversions, Conversion rate

### Action Files
`google_ads_actions_*.csv` - 5 properties per row:
- Day, Campaign, Ad group, Conversion action, Conversions

## 🔍 Query Examples

### Access Raw Original Data

```sql
-- Get original values exactly as in CSV
SELECT 
    raw_data->'original_row'->>'Impr.' as impressions,
    raw_data->'original_row'->>'CTR' as ctr
FROM google_ads_documents
LIMIT 5;

-- Result: "1,618" and "1.85%" (original format)
```

### Query Processed Data

```sql
-- Calculate totals
SELECT 
    metadata->>'campaign' as campaign,
    SUM((metadata->>'cost')::float) as total_cost,
    SUM((metadata->>'clicks')::integer) as total_clicks
FROM google_ads_documents
WHERE metadata->>'period' = '2024_11'
GROUP BY metadata->>'campaign'
ORDER BY total_cost DESC;
```

### Filter and Aggregate

```sql
-- Find high-performing days
SELECT 
    metadata->>'day' as date,
    metadata->>'campaign' as campaign,
    (metadata->>'ctr')::float as ctr,
    (metadata->>'conversions')::float as conversions
FROM google_ads_documents
WHERE (metadata->>'ctr')::float > 2.0
  AND (metadata->>'conversions')::float > 0
ORDER BY (metadata->>'ctr')::float DESC;
```

### Semantic Search

```python
# In Python
from supabase import create_client
import google.generativeai as genai

# Generate query embedding
query = "high performing display campaigns with conversions"
embedding = genai.embed_content(
    model="models/embedding-001",
    content=query,
    task_type="retrieval_query"
)

# Search
result = supabase.rpc(
    'match_google_ads_documents',
    {
        'query_embedding': embedding['embedding'],
        'match_count': 5
    }
).execute()
```

## ✅ Verify Zero Data Loss

After processing, verify nothing was lost:

```sql
-- Check raw data exists
SELECT COUNT(*) FROM google_ads_documents 
WHERE raw_data IS NOT NULL;

-- View original CSV format
SELECT 
    raw_data->'original_row' as original_csv_row
FROM google_ads_documents
LIMIT 1;

-- Verify all columns present
SELECT 
    jsonb_object_keys(raw_data->'original_row') as csv_columns
FROM google_ads_documents
LIMIT 1;
```

## 📁 File Structure

```
Essential Files:
├── README.md                          # This file (overview)
├── SIMPLE_SETUP.md                    # ⚡ Simple version guide
├── process_google_ads_simple.py       # ⚡ Simple processor (no embeddings)
├── setup_supabase_simple.sql          # ⚡ Simple database setup
├── test_setup_simple.py               # ⚡ Simple test
├── requirements_simple.txt            # ⚡ Simple dependencies
│
├── process_google_ads_zero_loss.py    # 🤖 Full processor (with embeddings)
├── setup_supabase_enhanced.sql        # 🤖 Full database setup
├── test_setup.py                      # 🤖 Full test
├── requirements.txt                   # 🤖 Full dependencies
│
├── CREDENTIALS_GUIDE.md               # How to get API keys
├── ZERO_DATA_LOSS_GUIDE.md           # Detailed guide
└── PROJECT_STRUCTURE.md               # Quick reference
```

## 🎓 For RAG AI Assistants

This approach is perfect for RAG because:

1. **Rich Context** - AI gets full campaign details
2. **Semantic Search** - Find relevant data by meaning
3. **Flexible Queries** - Answer diverse user questions
4. **Exact Values** - Can cite original numbers
5. **No Hallucination** - Ground truth in raw_data

### Example AI Queries Your System Can Answer:

- "What was our total spend on November 15th?"
- "Which ad groups have the best CTR?"
- "Show me conversion trends for Q4 2024"
- "Compare Display vs YouTube campaign performance"
- "What's our cost per conversion for Atlanta campaigns?"
- "Find similar high-performing campaigns"

## 💾 Storage Requirements

**Per row:** ~4.7 KB  
**For 3,000 rows:** ~14 MB total  
**Extra cost for zero loss:** ~1.4 MB (only 10% overhead!)

## 🔧 Customization

Want to add custom fields? Edit `process_google_ads_zero_loss.py`:

```python
# Add to metadata
metadata = {
    ...existing fields...,
    'custom_field': compute_something(row),
    'custom_tag': 'your_value'
}
```

## 🆘 Troubleshooting

### "Table does not exist"
→ Run `setup_supabase_enhanced.sql` in Supabase SQL Editor

### "API key invalid"
→ Check your `.env` file has correct keys (no quotes, no spaces)

### "Module not found"
→ Run `pip install -r requirements.txt`

### "Rate limit exceeded"
→ Normal! Script has built-in delays. Increase `time.sleep()` values if needed

### "Can't find data folder"
→ Ensure `NBX/Google Ads Export/` folder exists with CSV files

## 📖 Additional Documentation

**Google Ads:**
- **`CREDENTIALS_GUIDE.md`** - Step-by-step guide to get all API credentials
- **`ZERO_DATA_LOSS_GUIDE.md`** - Complete guide with examples and verification steps
- **`SIMPLE_SETUP.md`** - Quick start for simple version

**TikTok Ads:**
- **`TIKTOK_SETUP_GUIDE.md`** - Complete setup guide for TikTok Ads processing
- **`setup_supabase_tiktok.sql`** - Database schema for TikTok data

**Power BI:**
- **`POWERBI_SETUP_GUIDE.md`** - Complete setup guide for Power BI processing
- **`setup_powerbi.sql`** - Database schema for Power BI data
- **`process_powerbi.py`** - Processing script (no embeddings)

**General:**
- **`PROJECT_STRUCTURE.md`** - Quick reference for project layout
- **`HOW_TO_RUN_SQL.md`** - Guide for running SQL scripts

## 🚀 Next Steps

After processing your marketing data:

1. ✅ **Process TikTok Ads** - See [TIKTOK_SETUP_GUIDE.md](TIKTOK_SETUP_GUIDE.md)
2. ✅ Build semantic search interface
3. ✅ Create RAG AI Assistant
4. ✅ Add automated data updates
5. ✅ Build analytics dashboards
6. ✅ Compare cross-platform performance

## 🔐 Security Notes

- Never commit your `.env` file
- Use environment variables for all credentials
- Consider Row Level Security (RLS) in Supabase for production

## 📊 Database Schema

```sql
google_ads_documents (
  id          BIGSERIAL PRIMARY KEY,
  content     TEXT NOT NULL,
  metadata    JSONB NOT NULL,
  raw_data    JSONB NOT NULL,      -- ← Original CSV data
  embedding   vector(768),
  created_at  TIMESTAMP,
  updated_at  TIMESTAMP
)
```

## 🎯 Key Features

- ✅ Zero data loss - original CSV preserved
- ✅ Efficient queries - typed metadata
- ✅ Semantic search - vector embeddings
- ✅ Audit trail - can reconstruct original files
- ✅ Future-proof - add new queries anytime
- ✅ Cost-effective - minimal storage overhead

## 🤝 Support

- Check `ZERO_DATA_LOSS_GUIDE.md` for detailed documentation
- Review verification queries to ensure data integrity
- Test queries on small sample before production use

## 📝 License

MIT

---

**Ready to build your RAG AI Assistant with zero data loss!** 🚀

Run `python process_google_ads_zero_loss.py` to get started.

