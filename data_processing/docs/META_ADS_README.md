# Meta Ads Data Processing

## What This Does

Processes your Meta Ads CSV files and stores **ALL properties as individual columns** in Supabase:
- ✅ **All CSV columns preserved** - Every property stored as a database column
- ✅ **No JSONB** - Direct column access for better performance
- ✅ **No embeddings** - Fast processing, no API costs
- ✅ **Easy to query** - Standard SQL, no special operators needed

---

## Quick Start

### Step 1: Create Database Table

Open **Supabase SQL Editor** and run the file:

```bash
setup_meta_ads.sql
```

This creates the `meta_ads_performance` table with **39 columns** covering all your CSV data.

### Step 2: Process Your Data

```bash
python process_meta_ads.py
```

Done! ✅

---

## What Gets Stored

**Table:** `meta_ads_performance`

**All Original CSV Columns:**
- `campaign_name`, `ad_set_name`, `ad_name`
- `objective`, `result_type`, `website_url`
- `day`, `starts`, `ends`, `reporting_starts`, `reporting_ends`
- `reach`, `impressions`, `frequency`
- `results`, `amount_spent`, `cost_per_result`
- `link_clicks`, `cpc`, `cpm`
- `video_avg_play_time`, `cost_per_thruplay`, `thru_plays`
- `video_plays_25`, `video_plays_50`, `video_plays_75`, `video_plays_95`, `video_plays_100`
- Plus computed fields: `has_results`, `has_link_clicks`, `has_video_content`

**No JSONB** - All properties are direct columns!

---

## Query Examples

### Total Spend by Campaign
```sql
SELECT 
    campaign_name,
    SUM(amount_spent) as total_spent,
    SUM(link_clicks) as total_clicks,
    AVG(cpc) as avg_cpc
FROM meta_ads_performance
GROUP BY campaign_name
ORDER BY total_spent DESC;
```

### Video Performance
```sql
SELECT 
    ad_name,
    video_avg_play_time,
    thru_plays,
    video_plays_100,
    CASE 
        WHEN video_plays_25 > 0 
        THEN (video_plays_100::float / video_plays_25 * 100)
        ELSE 0 
    END as completion_rate
FROM meta_ads_performance
WHERE has_video_content = TRUE
ORDER BY thru_plays DESC;
```

### Daily Performance
```sql
SELECT 
    day,
    COUNT(*) as num_ads,
    SUM(amount_spent) as daily_spend,
    SUM(impressions) as daily_impressions,
    SUM(link_clicks) as daily_clicks
FROM meta_ads_performance
WHERE day >= '2025-10-01'
GROUP BY day
ORDER BY day DESC;
```

### Top Performing by Objective
```sql
SELECT 
    objective,
    ad_name,
    results,
    amount_spent,
    cost_per_result
FROM meta_ads_performance
WHERE has_results = TRUE
ORDER BY objective, results DESC;
```

---

## CSV File Location

Your files should be in:
```
NBX/Meta Ads Export/
  - meta_ads_export_2024_11.csv
  - meta_ads_export_2024_12.csv
  - meta_ads_export_2025_01.csv
  - etc.
```

---

## Environment Setup

Make sure your `.env` file has:
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

---

## Advantages of This Approach

✅ **All properties preserved** - Every CSV column stored
✅ **Direct access** - `SELECT campaign_name` (not `metadata->>'campaign_name'`)
✅ **Better performance** - Database can index and optimize individual columns
✅ **Type safety** - Proper data types (INTEGER, NUMERIC, DATE, etc.)
✅ **Easier queries** - Standard SQL, no JSON operators
✅ **Clear schema** - See all columns in database structure

---

## Compare: JSONB vs Structured

### ❌ JSONB Approach (Not Used)
```sql
-- Harder to query
SELECT metadata->>'campaign_name',
       (metadata->>'amount_spent')::numeric
FROM meta_ads_documents
```

### ✅ Structured Approach (What We Use)
```sql
-- Clean and simple
SELECT campaign_name, amount_spent
FROM meta_ads_performance
```

---

## Troubleshooting

**"Missing environment variables"**
→ Check your `.env` file has `SUPABASE_URL` and `SUPABASE_KEY`

**"Data folder not found"**
→ Ensure `NBX/Meta Ads Export/` directory exists

**"Table doesn't exist"**
→ Run `setup_meta_ads.sql` in Supabase first

**"Error storing data"**
→ Check Supabase connection and table permissions

---

## Next Steps

1. Run `setup_meta_ads.sql` in Supabase ✅
2. Run `python process_meta_ads.py` ✅
3. Query your data using the examples above 📊
4. Build dashboards and reports 📈

---

That's it! All your Meta Ads data is now stored with **all properties preserved** as individual columns. 🎉
