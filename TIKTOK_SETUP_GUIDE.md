# TikTok Ads Data Processing Guide

This guide will help you process and store TikTok Ads data in Supabase.

## 📋 Prerequisites

1. **Supabase Account** - Get your credentials from [supabase.com](https://supabase.com)
2. **Python 3.8+** installed
3. **TikTok Ads CSV files** in `NBX/TikTok Ads Export/`

## 🚀 Quick Start

### Step 1: Set Up Environment

Create a `.env` file in the project root:

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
GOOGLE_API_KEY=your_google_api_key  # Only needed for zero-loss version
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

Or install individually:

```bash
pip install pandas supabase python-dotenv
pip install google-generativeai  # Only for zero-loss version
```

### Step 3: Set Up Database Tables

Go to your Supabase dashboard → SQL Editor and run:

```sql
-- Run this SQL file
setup_supabase_tiktok.sql
```

This creates:
- `tiktok_ads_performance` - Structured table with individual columns
- `tiktok_ads_documents` - Flexible table for simple/zero-loss versions

### Step 4: Test Your Setup

```bash
# For structured version
python test_setup_tiktok_structured.py

# For simple version
python test_setup_tiktok_simple.py
```

### Step 5: Process Your Data

Choose one of three versions:

#### Option A: Structured Version (Recommended)
**Best for:** SQL queries, analytics, dashboards

```bash
python process_tiktok_ads_structured.py
```

**Features:**
- ✅ All data in individual columns
- ✅ Fast queries with standard SQL
- ✅ Clear schema
- ✅ Best performance

**Table:** `tiktok_ads_performance`

#### Option B: Simple Version
**Best for:** Quick setup, no embeddings needed

```bash
python process_tiktok_ads_simple.py
```

**Features:**
- ✅ Fast processing (no embeddings)
- ✅ 100% data preservation (raw data + metadata)
- ✅ JSONB flexibility
- ⏭️ Can add embeddings later

**Table:** `tiktok_ads_documents`

#### Option C: Zero-Loss Version with Embeddings
**Best for:** AI/ML, semantic search, advanced analytics

```bash
python process_tiktok_ads_zero_loss.py
```

**Features:**
- ✅ Vector embeddings for semantic search
- ✅ 100% data preservation
- ✅ AI-ready
- ⚠️ Slower (generates embeddings)

**Table:** `tiktok_ads_documents`

## 📊 TikTok Ads Data Structure

### CSV Columns Captured

**Campaign Information:**
- Campaign name
- Ad group name
- Ad name
- Website URL
- Date (By Day)

**Performance Metrics:**
- Cost, CPC, CPM
- Impressions, Clicks, CTR
- Reach
- Cost per 1,000 people reached
- Frequency

**Video Metrics:**
- Total video views
- 2-second video views
- 6-second video views
- Video completion rates (25%, 50%, 75%, 100%)
- Average play time per view
- Average play time per user

**Computed Fields:**
- Has clicks (boolean)
- Has video views (boolean)
- Video completion rate (percentage)

## 🔍 Querying Your Data

### Structured Version Examples

```sql
-- Get all campaigns from a specific month
SELECT campaign_name, SUM(cost) as total_cost, SUM(clicks) as total_clicks
FROM tiktok_ads_performance
WHERE year = '2024' AND month = '10'
GROUP BY campaign_name
ORDER BY total_cost DESC;

-- Find high-performing videos (>50% completion rate)
SELECT campaign_name, ad_name, 
       video_views, completion_rate, cost
FROM tiktok_ads_performance
WHERE completion_rate > 50
ORDER BY completion_rate DESC;

-- Daily performance over time
SELECT day, SUM(cost) as daily_cost, 
       SUM(impressions) as daily_impressions,
       SUM(clicks) as daily_clicks
FROM tiktok_ads_performance
GROUP BY day
ORDER BY day DESC;

-- Best performing ad groups by CTR
SELECT ad_group_name, campaign_name,
       AVG(ctr) as avg_ctr,
       SUM(cost) as total_cost,
       SUM(clicks) as total_clicks
FROM tiktok_ads_performance
WHERE has_clicks = TRUE
GROUP BY ad_group_name, campaign_name
ORDER BY avg_ctr DESC
LIMIT 10;

-- Video engagement analysis
SELECT campaign_name,
       SUM(video_views) as total_views,
       AVG(completion_rate) as avg_completion,
       AVG(avg_play_time_per_view) as avg_watch_time
FROM tiktok_ads_performance
WHERE has_video_views = TRUE
GROUP BY campaign_name
ORDER BY total_views DESC;
```

### Simple/Zero-Loss Version Examples

```sql
-- Query using JSONB metadata
SELECT content, metadata->>'campaign_name' as campaign,
       (metadata->>'cost')::numeric as cost
FROM tiktok_ads_documents
WHERE metadata->>'year' = '2024'
  AND metadata->>'month' = '10'
ORDER BY (metadata->>'cost')::numeric DESC;

-- Search text content
SELECT content, metadata->>'day' as date
FROM tiktok_ads_documents
WHERE content ILIKE '%video views%'
LIMIT 10;

-- Filter by video performance
SELECT metadata->>'campaign_name' as campaign,
       (metadata->>'video_views')::int as views,
       (metadata->>'completion_rate')::numeric as completion
FROM tiktok_ads_documents
WHERE (metadata->>'has_video_views')::boolean = true
ORDER BY (metadata->>'video_views')::int DESC;
```

## 🆚 Which Version Should I Use?

| Feature | Structured | Simple | Zero-Loss |
|---------|-----------|--------|-----------|
| **Speed** | ⚡ Fast | ⚡ Fast | 🐌 Slow |
| **SQL Queries** | ✅ Easy | ⚠️ JSONB | ⚠️ JSONB |
| **Data Preservation** | ✅ 100% | ✅ 100% | ✅ 100% |
| **Embeddings** | ❌ No | ❌ No | ✅ Yes |
| **Semantic Search** | ❌ No | ❌ No | ✅ Yes |
| **Storage** | Medium | Small | Large |
| **Use Case** | Analytics | Quick Setup | AI/ML |

**Recommendation:** Start with **Structured Version** for best performance and query simplicity.

## 📝 File Naming Convention

TikTok CSV files should follow this pattern:
```
tiktok_ads_export_YYYY_MM.csv
```

Examples:
- `tiktok_ads_export_2024_10.csv`
- `tiktok_ads_export_2024_11.csv`
- `tiktok_ads_export_2025_01.csv`

## 🔧 Troubleshooting

### "Table does not exist" error
**Solution:** Run `setup_supabase_tiktok.sql` in Supabase SQL Editor

### "Missing environment variables" error
**Solution:** Create `.env` file with `SUPABASE_URL` and `SUPABASE_KEY`

### CSV parsing errors
**Solution:** Ensure CSV files are in the correct format with all expected columns

### Slow processing
**Solution:** 
- Use structured or simple version (not zero-loss)
- Check your internet connection (API calls to Supabase)
- Reduce file size or process in batches

## 📚 Related Files

- `setup_supabase_tiktok.sql` - Database schema
- `process_tiktok_ads_structured.py` - Structured version processor
- `process_tiktok_ads_simple.py` - Simple version processor
- `process_tiktok_ads_zero_loss.py` - Zero-loss with embeddings
- `test_setup_tiktok_structured.py` - Test structured setup
- `test_setup_tiktok_simple.py` - Test simple setup

## 🎯 Next Steps

After processing your TikTok Ads data:

1. **Connect to BI Tools** - Use Tableau, Power BI, or Metabase
2. **Build Dashboards** - Create visualizations of your ad performance
3. **Run Analytics** - Query your data to find insights
4. **Set Up Alerts** - Monitor key metrics
5. **Compare Platforms** - Analyze TikTok vs Google Ads vs Meta Ads

## 💡 Tips

- Process data monthly to keep it organized
- Use the structured version for best SQL query performance
- Keep raw CSV files as backups
- Index frequently queried columns for better performance
- Monitor your Supabase storage and row limits

## 🔗 Additional Resources

- [Supabase Documentation](https://supabase.com/docs)
- [TikTok Ads Manager](https://ads.tiktok.com/)
- [Google Ads Setup Guide](QUICKSTART_SIMPLE.md) - Similar setup for Google Ads
- [Meta Ads Processing](coming soon) - Process Meta/Facebook ads

## 🆘 Need Help?

Check the main `README.md` for general setup instructions or refer to:
- `CREDENTIALS_GUIDE.md` - How to get API credentials
- `HOW_TO_RUN_SQL.md` - Guide for running SQL scripts
- `PROJECT_STRUCTURE.md` - Overall project structure

