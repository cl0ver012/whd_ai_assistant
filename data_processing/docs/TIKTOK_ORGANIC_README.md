# TikTok Organic Data Processing

## Quick Summary

This implementation processes TikTok Organic performance data into Supabase with **zero data loss**. All CSV columns are preserved as individual database columns for fast querying.

## Key Features

✅ **All Data Preserved**: Every CSV column stored as a database column  
✅ **No Embeddings**: Simple, fast, and cost-effective  
✅ **No JSONB**: Direct SQL column access  
✅ **Batch Processing**: 100 rows at a time for speed  
✅ **Duplicate Detection**: Automatically skips existing records  
✅ **Full-Text Search**: Search through content field  

## Files Created

### 1. SQL Setup
**File**: `data_processing/sql/setup_tiktok_organic.sql`
- Creates `tiktok_organic` table
- Adds indexes for fast querying
- Includes full-text search support

### 2. Processing Script
**File**: `data_processing/scripts/process_tiktok_organic.py`
- Reads all TikTok Organic CSV files
- Processes and stores data in Supabase
- Preserves all original data
- No embeddings needed

### 3. Test Script
**File**: `data_processing/tests/test_setup_tiktok_organic.py`
- Validates database setup
- Tests table structure
- Verifies queries work correctly

### 4. Documentation
**File**: `data_processing/docs/TIKTOK_ORGANIC_SETUP_GUIDE.md`
- Complete setup instructions
- Example queries
- Troubleshooting guide

## Quick Start

### Step 1: Setup Database
```sql
-- Run in Supabase SQL Editor
-- File: data_processing/sql/setup_tiktok_organic.sql
```

### Step 2: Run Test (Optional)
```bash
python data_processing/tests/test_setup_tiktok_organic.py
```

### Step 3: Process Data
```bash
# Process all files
python data_processing/scripts/process_tiktok_organic.py

# Fresh start (clear existing data first)
python data_processing/scripts/process_tiktok_organic.py --clear
```

## Data Structure

### Input (CSV)
Files in `NBX/TikTok Organic/`:
```
TikTok Apr 25.csv
TikTok May 25.csv
TikTok Jun 25.csv
...
```

Each CSV contains:
- Date
- Video Views
- Profile Views
- Likes
- Comments
- Shares

### Output (Database)
Table: `tiktok_organic`

All columns preserved:
- Source info (file_name, period, year, month)
- Date info (date, day_of_month)
- Metrics (video_views, profile_views, likes, comments, shares)
- Computed fields (total_engagement, has_views, has_engagement)
- Search field (content)

## Example Queries

### Monthly Summary
```sql
SELECT 
    year,
    month_name,
    SUM(video_views) as total_video_views,
    SUM(likes) as total_likes,
    SUM(total_engagement) as total_engagement,
    ROUND(AVG(video_views)) as avg_daily_views
FROM tiktok_organic
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

### Top Performing Days
```sql
SELECT 
    date,
    video_views,
    total_engagement
FROM tiktok_organic
ORDER BY total_engagement DESC
LIMIT 10;
```

### Daily Trends
```sql
SELECT 
    date,
    video_views,
    LAG(video_views) OVER (ORDER BY year, month, day_of_month::INTEGER) as prev_day_views
FROM tiktok_organic
WHERE year = '2025'
ORDER BY month, day_of_month::INTEGER;
```

## Performance

- **Processing Speed**: ~100-200 records/second
- **Batch Size**: 100 rows per batch
- **No Rate Limiting**: No external API calls
- **Safe Re-runs**: Skips duplicate records

## Comparison with Other Implementations

| Feature | TikTok Ads (Zero Loss) | Organic Social | TikTok Organic |
|---------|------------------------|----------------|----------------|
| Embeddings | ✅ Yes | ❌ No | ❌ No |
| JSONB | ✅ Yes | ❌ No | ❌ No |
| Individual Columns | ✅ Yes | ✅ Yes | ✅ Yes |
| Batch Processing | ❌ No | ✅ Yes | ✅ Yes |
| Speed | Slow (0.5s delay) | Fast (~200/s) | Fast (~200/s) |

**TikTok Organic follows the Organic Social pattern**: Fast, simple, no embeddings.

## Directory Structure

```
data_processing/
├── scripts/
│   └── process_tiktok_organic.py      # Main processing script
├── sql/
│   └── setup_tiktok_organic.sql       # Database setup
├── tests/
│   └── test_setup_tiktok_organic.py   # Validation tests
└── docs/
    ├── TIKTOK_ORGANIC_README.md       # This file
    └── TIKTOK_ORGANIC_SETUP_GUIDE.md  # Detailed guide

NBX/
└── TikTok Organic/
    ├── TikTok Apr 25.csv
    ├── TikTok May 25.csv
    └── ...
```

## Troubleshooting

### Missing Environment Variables
```bash
# Check .env file contains:
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Table Not Found
Run the SQL setup script first:
```sql
-- data_processing/sql/setup_tiktok_organic.sql
```

### Duplicate Records
Use `--clear` flag to start fresh:
```bash
python data_processing/scripts/process_tiktok_organic.py --clear
```

## Support

For detailed instructions, see:
- **Setup Guide**: `data_processing/docs/TIKTOK_ORGANIC_SETUP_GUIDE.md`
- **Test Script**: `data_processing/tests/test_setup_tiktok_organic.py`

## Next Steps

1. ✅ Run SQL setup script
2. ✅ Test with test script (optional)
3. ✅ Process your data
4. ✅ Query with standard SQL

That's it! Your TikTok Organic data is now in Supabase with zero data loss.

