# TikTok Organic Data Processing - Setup Guide

## Overview

This guide will help you set up and process TikTok Organic performance data into Supabase. All data properties are preserved as individual database columns for fast querying - no JSONB, no embeddings.

## Data Structure

TikTok Organic CSV files contain daily performance metrics:

### CSV Columns
- **Date**: Day and month (e.g., "1 April", "15 December")
- **Video Views**: Number of video views
- **Profile Views**: Number of profile views
- **Likes**: Number of likes
- **Comments**: Number of comments
- **Shares**: Number of shares

### File Naming Convention
Files should be named: `TikTok {Month} {YY}.csv`
- Examples: `TikTok Apr 25.csv`, `TikTok Dec 24.csv`
- Month can be abbreviated (Apr, Dec) or full (July, June, Sept)
- YY is two-digit year (24 = 2024, 25 = 2025)

## Setup Instructions

### Step 1: Set Up Database

1. Open your Supabase SQL Editor
2. Run the setup script:

```sql
-- Located at: data_processing/sql/setup_tiktok_organic.sql
```

This creates:
- `tiktok_organic` table with all properties as individual columns
- Indexes for fast querying
- Full-text search support

### Step 2: Configure Environment

Ensure your `.env` file contains:

```bash
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_service_role_key
```

### Step 3: Prepare Data

Place your TikTok Organic CSV files in:
```
NBX/TikTok Organic/
```

Expected files:
- TikTok Apr 25.csv
- TikTok May 25.csv
- TikTok Jun 25.csv
- etc.

### Step 4: Run Processing Script

```bash
# Process all files (skips existing records)
python data_processing/scripts/process_tiktok_organic.py

# Fresh start (delete all existing data first)
python data_processing/scripts/process_tiktok_organic.py --clear
```

## Database Schema

```sql
CREATE TABLE tiktok_organic (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    period TEXT NOT NULL,              -- e.g., "2025_04"
    year TEXT NOT NULL,                -- e.g., "2025"
    month TEXT NOT NULL,               -- e.g., "04"
    month_name TEXT NOT NULL,          -- e.g., "April"
    
    -- Date Information
    date TEXT NOT NULL,                -- e.g., "1 April"
    day_of_month TEXT,                 -- e.g., "1"
    
    -- Engagement Metrics
    video_views INTEGER DEFAULT 0,
    profile_views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    
    -- Computed Fields
    has_views BOOLEAN DEFAULT FALSE,
    has_engagement BOOLEAN DEFAULT FALSE,
    total_engagement INTEGER DEFAULT 0,
    
    -- Text content for search
    content TEXT
);
```

## Example Queries

### Get Daily Performance for a Month

```sql
SELECT 
    date,
    video_views,
    profile_views,
    likes,
    comments,
    shares,
    total_engagement
FROM tiktok_organic
WHERE year = '2025' 
  AND month = '04'
ORDER BY day_of_month::INTEGER;
```

### Get Monthly Summary

```sql
SELECT 
    year,
    month_name,
    COUNT(*) as days,
    SUM(video_views) as total_video_views,
    SUM(profile_views) as total_profile_views,
    SUM(likes) as total_likes,
    SUM(comments) as total_comments,
    SUM(shares) as total_shares,
    SUM(total_engagement) as total_engagement,
    ROUND(AVG(video_views)) as avg_daily_video_views,
    ROUND(AVG(total_engagement)) as avg_daily_engagement
FROM tiktok_organic
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

### Get Top Performing Days

```sql
SELECT 
    date,
    period,
    video_views,
    total_engagement,
    ROUND((likes::FLOAT / NULLIF(video_views, 0) * 100), 2) as engagement_rate
FROM tiktok_organic
WHERE video_views > 0
ORDER BY total_engagement DESC
LIMIT 20;
```

### Search by Date

```sql
SELECT *
FROM tiktok_organic
WHERE content ILIKE '%October%'
  AND video_views > 10000
ORDER BY video_views DESC;
```

### Get Performance Trends

```sql
SELECT 
    date,
    video_views,
    total_engagement,
    LAG(video_views) OVER (ORDER BY year, month, day_of_month::INTEGER) as prev_day_views,
    video_views - LAG(video_views) OVER (ORDER BY year, month, day_of_month::INTEGER) as views_change
FROM tiktok_organic
WHERE year = '2025'
ORDER BY month, day_of_month::INTEGER;
```

## Features

✅ **Zero Data Loss**: All CSV columns preserved as database columns
✅ **No Embeddings**: Simple and fast - no AI embeddings needed
✅ **Batch Processing**: Processes 100 rows at a time for speed
✅ **Duplicate Detection**: Automatically skips existing records
✅ **Full-Text Search**: Search through content field
✅ **Computed Fields**: Automatic calculation of totals and flags
✅ **Fast Queries**: Optimized indexes for all common queries

## Performance

- **Processing Speed**: ~100-200 records/second
- **Batch Size**: 100 rows per batch
- **No Rate Limiting**: No external API calls, maximum speed
- **Safe Re-runs**: Automatically skips duplicate records

## Troubleshooting

### Error: Missing environment variables
Make sure your `.env` file contains `SUPABASE_URL` and `SUPABASE_KEY`.

### Error: Data folder not found
Ensure `NBX/TikTok Organic/` folder exists with CSV files.

### Error: Could not extract period from filename
Check that files follow naming convention: `TikTok {Month} {YY}.csv`

### Duplicate records
Use `--clear` flag to delete all existing data before processing:
```bash
python data_processing/scripts/process_tiktok_organic.py --clear
```

## Data Validation

After processing, verify your data:

```sql
-- Check total records
SELECT COUNT(*) as total_records FROM tiktok_organic;

-- Check records by month
SELECT 
    year,
    month_name,
    COUNT(*) as records
FROM tiktok_organic
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;

-- Check for any missing data
SELECT *
FROM tiktok_organic
WHERE video_views IS NULL 
   OR profile_views IS NULL;
```

## Support

For issues or questions:
1. Check that the SQL setup script ran successfully
2. Verify environment variables are set correctly
3. Ensure CSV files match the expected format
4. Check the console output for specific error messages

