# TikTok Ads Processing Files - Summary

Quick reference for all TikTok Ads related files in this project.

## 📝 Processing Scripts

### `process_tiktok_ads_structured.py`
**Recommended for most users**

- Stores data in structured columns (no JSONB)
- Best for SQL queries and analytics
- Fast processing (no embeddings)
- Table: `tiktok_ads_performance`

**Run:** `python process_tiktok_ads_structured.py`

### `process_tiktok_ads_simple.py`
**For quick setup without embeddings**

- Stores data with JSONB metadata
- Fast processing (no embeddings)
- 100% data preservation
- Table: `tiktok_ads_documents`

**Run:** `python process_tiktok_ads_simple.py`

### `process_tiktok_ads_zero_loss.py`
**For AI/ML and semantic search**

- Includes vector embeddings
- 100% data preservation
- Slower (generates embeddings)
- Requires Google API key
- Table: `tiktok_ads_documents`

**Run:** `python process_tiktok_ads_zero_loss.py`

## 🗄️ Database Setup

### `setup_supabase_tiktok.sql`
**Database schema for TikTok ads**

Creates two tables:
1. `tiktok_ads_performance` - Structured columns version
2. `tiktok_ads_documents` - Simple/zero-loss version

Includes:
- Table definitions
- Indexes for performance
- Full-text search support
- Vector search support (for embeddings)

**Run in:** Supabase SQL Editor

## 🧪 Test Scripts

### `test_setup_tiktok_structured.py`
Tests the structured version setup:
- Environment variables
- Database connection
- Table accessibility
- Data folder existence

**Run:** `python test_setup_tiktok_structured.py`

### `test_setup_tiktok_simple.py`
Tests the simple/zero-loss version setup:
- Environment variables
- Database connection
- Documents table
- Data folder existence

**Run:** `python test_setup_tiktok_simple.py`

## 📖 Documentation

### `TIKTOK_SETUP_GUIDE.md`
**Complete guide for TikTok ads processing**

Includes:
- Prerequisites and setup
- All three version comparisons
- SQL query examples
- Troubleshooting tips
- Best practices

## 📊 Data Files

### `NBX/TikTok Ads Export/`
Location for your TikTok CSV files

**Naming convention:** `tiktok_ads_export_YYYY_MM.csv`

**Example files:**
- `tiktok_ads_export_2024_10.csv`
- `tiktok_ads_export_2024_11.csv`
- `tiktok_ads_export_2025_01.csv`

## 🔄 Processing Flow

```
1. CSV Files (NBX/TikTok Ads Export/)
        ↓
2. Processing Script (choose one):
   - process_tiktok_ads_structured.py
   - process_tiktok_ads_simple.py
   - process_tiktok_ads_zero_loss.py
        ↓
3. Supabase Database
   - tiktok_ads_performance (structured)
   - tiktok_ads_documents (simple/zero-loss)
        ↓
4. Query & Analyze
```

## 🚀 Quick Start Checklist

- [ ] Place CSV files in `NBX/TikTok Ads Export/`
- [ ] Create `.env` file with Supabase credentials
- [ ] Run `setup_supabase_tiktok.sql` in Supabase
- [ ] Run test script: `python test_setup_tiktok_structured.py`
- [ ] Process data: `python process_tiktok_ads_structured.py`
- [ ] Query your data in Supabase

## 📏 Data Columns Processed

### Campaign Information
- Campaign name
- Ad group name
- Ad name
- Website URL
- Date (By Day)
- Currency

### Performance Metrics
- Cost
- CPC (Cost Per Click)
- CPM (Cost Per Mille)
- Impressions
- Clicks
- CTR (Click-Through Rate)
- Reach
- Cost per 1,000 reached
- Frequency

### Video Metrics
- Total video views
- 2-second video views
- 6-second video views
- Video views at 100%
- Video views at 75%
- Video views at 50%
- Video views at 25%
- Average play time per view
- Average play time per user

### Computed Fields
- Has clicks (boolean)
- Has video views (boolean)
- Video completion rate (percentage)

## 💡 Which Files Do I Need?

### For Basic Analytics (Recommended)
1. `setup_supabase_tiktok.sql`
2. `process_tiktok_ads_structured.py`
3. `test_setup_tiktok_structured.py` (optional, for testing)

### For Quick Start (No Embeddings)
1. `setup_supabase_tiktok.sql`
2. `process_tiktok_ads_simple.py`
3. `test_setup_tiktok_simple.py` (optional, for testing)

### For AI/ML Applications
1. `setup_supabase_tiktok.sql`
2. `process_tiktok_ads_zero_loss.py`
3. Google API key in `.env`
4. `test_setup_tiktok_simple.py` (optional, for testing)

## 🔗 Related Files

**Also check:**
- `README.md` - Main project overview
- `CREDENTIALS_GUIDE.md` - How to get API credentials
- `HOW_TO_RUN_SQL.md` - SQL setup guide
- `requirements.txt` - Python dependencies

## 🆘 Common Issues

| Issue | Solution |
|-------|----------|
| Table doesn't exist | Run `setup_supabase_tiktok.sql` in Supabase |
| Missing credentials | Add `SUPABASE_URL` and `SUPABASE_KEY` to `.env` |
| CSV not found | Check files are in `NBX/TikTok Ads Export/` |
| Slow processing | Use structured or simple version (not zero-loss) |

## 📈 Performance Comparison

| Version | Processing Time (1000 rows) | Storage Size | Best For |
|---------|----------------------------|--------------|----------|
| Structured | ~3-5 minutes | Medium | Analytics, Dashboards |
| Simple | ~3-5 minutes | Small | Quick Setup |
| Zero-Loss | ~25-35 minutes | Large | AI, ML, Semantic Search |

---

**Need help?** See [TIKTOK_SETUP_GUIDE.md](TIKTOK_SETUP_GUIDE.md) for detailed instructions.

