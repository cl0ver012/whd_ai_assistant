# Organic Social Media Data Processing Setup Guide

This guide will help you set up and process your Organic Social Media data into Supabase.

## 📋 Overview

The Organic Social Media processing system:
- ✅ Stores all CSV properties as individual database columns
- ✅ No JSONB - direct column access for better performance
- ✅ No embeddings - simple and fast
- ✅ Batch processing for maximum speed
- ✅ Safe to re-run - automatically skips duplicates
- ✅ Processes Instagram posts (images, reels, videos)

## 📊 Data Structure

The system processes CSV files with the following columns:
- **Post ID** - Unique post identifier
- **Account ID** - Social media account ID
- **Account username** - Social media username
- **Account name** - Display name
- **Description** - Post caption/description
- **Duration (sec)** - Video duration
- **Publish time** - When the post was published
- **Permalink** - Direct link to post
- **Post type** - Type (IG image, IG reel, etc.)
- **Date** - Date information
- **Views** - Number of views
- **Reach** - Unique users reached
- **Likes** - Number of likes
- **Shares** - Number of shares
- **Follows** - Follows generated
- **Comments** - Number of comments
- **Saves** - Number of saves

## 🚀 Quick Start

### Step 1: Set Up Database

1. Open your Supabase SQL Editor
2. Run the setup SQL file:
   ```bash
   # Copy the contents of setup_organic_social.sql and run in Supabase SQL Editor
   ```

This creates:
- `organic_social_media` table with all properties as individual columns
- Indexes for fast querying
- Full-text search capabilities

### Step 2: Prepare Your Data

Your CSV files should be in the format:
```
NBX/Organic Social Media/
  Apr-01-2025_Apr-30-2025_1541562187185864.csv
  Nov-01-2024_Nov-30-2024_1174490457462648.csv
  ...
```

File naming convention: `MMM-DD-YYYY_MMM-DD-YYYY_ACCOUNTID.csv`

### Step 3: Configure Environment

Ensure your `.env` file has:
```
SUPABASE_URL=your-supabase-url
SUPABASE_KEY=your-supabase-key
```

### Step 4: Run Processing Script

```bash
# Activate virtual environment
source venv/bin/activate

# Run the script
python process_organic_social.py

# Or clear existing data first (fastest)
python process_organic_social.py --clear
```

## 📈 What Gets Stored

### Database Columns

All data is stored in structured columns:

```sql
-- Source Information
file_name, period, year, month, month_name

-- Post Identification
post_id, account_id, account_username, account_name

-- Post Details
description, duration_sec, publish_time, permalink, 
post_type, data_comment, date

-- Engagement Metrics
views, reach, likes, shares, follows, comments, saves

-- Computed Fields
has_views, has_engagement, is_video

-- Search Content
content (human-readable text for search/display)
```

## 🔍 Example Queries

### Get top performing posts
```sql
SELECT 
    account_username,
    post_type,
    description,
    views,
    likes,
    comments,
    shares,
    publish_time,
    permalink
FROM organic_social_media
WHERE month = '11' AND year = '2024'
ORDER BY views DESC
LIMIT 10;
```

### Analyze engagement by post type
```sql
SELECT 
    post_type,
    COUNT(*) as post_count,
    AVG(views) as avg_views,
    AVG(likes) as avg_likes,
    AVG(comments) as avg_comments,
    SUM(shares) as total_shares
FROM organic_social_media
WHERE year = '2025'
GROUP BY post_type
ORDER BY avg_views DESC;
```

### Get video content performance
```sql
SELECT 
    post_id,
    description,
    duration_sec,
    views,
    reach,
    likes,
    comments,
    permalink
FROM organic_social_media
WHERE is_video = TRUE
  AND year = '2025'
ORDER BY views DESC;
```

### Monthly performance summary
```sql
SELECT 
    year,
    month_name,
    COUNT(*) as total_posts,
    SUM(views) as total_views,
    SUM(reach) as total_reach,
    SUM(likes) as total_likes,
    SUM(comments) as total_comments,
    SUM(shares) as total_shares,
    AVG(views) as avg_views_per_post
FROM organic_social_media
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

### Search posts by keyword
```sql
SELECT 
    post_id,
    description,
    post_type,
    views,
    likes,
    permalink
FROM organic_social_media
WHERE description ILIKE '%noodle%'
  OR content ILIKE '%noodle%'
ORDER BY views DESC;
```

### Get posts with high engagement rate
```sql
SELECT 
    post_id,
    account_username,
    post_type,
    description,
    views,
    likes,
    comments,
    shares,
    CASE 
        WHEN reach > 0 
        THEN ROUND((likes + comments + shares)::numeric / reach * 100, 2)
        ELSE 0 
    END as engagement_rate_percent,
    permalink
FROM organic_social_media
WHERE reach > 0
  AND year = '2025'
ORDER BY engagement_rate_percent DESC
LIMIT 20;
```

## ⚙️ Processing Options

### Normal Mode (Default)
```bash
python process_organic_social.py
```
- Checks for existing records
- Only inserts new posts
- Safe for incremental updates

### Clear Mode (Fastest)
```bash
python process_organic_social.py --clear
```
- Deletes all existing data first
- Fastest processing
- Use for fresh import

## 📋 Data Verification

After processing, verify your data:

```sql
-- Check total records
SELECT COUNT(*) FROM organic_social_media;

-- Check by period
SELECT 
    year,
    month_name,
    COUNT(*) as record_count
FROM organic_social_media
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;

-- Check by account
SELECT 
    account_username,
    COUNT(*) as post_count
FROM organic_social_media
GROUP BY account_username;

-- Check post types
SELECT 
    post_type,
    COUNT(*) as count
FROM organic_social_media
GROUP BY post_type
ORDER BY count DESC;
```

## 🎯 Performance Features

1. **Batch Processing**: Inserts 100 rows at a time for maximum speed
2. **Duplicate Detection**: Uses post_id to avoid duplicates
3. **Indexed Columns**: All important fields are indexed for fast queries
4. **No JSONB**: Direct column access for better performance
5. **No Embeddings**: Simplified storage for speed

## 🔧 Troubleshooting

### Issue: "Table does not exist"
**Solution**: Run the SQL setup file in Supabase first

### Issue: "Missing environment variables"
**Solution**: Check your `.env` file has SUPABASE_URL and SUPABASE_KEY

### Issue: "Could not extract period from filename"
**Solution**: Ensure filenames follow the format: `MMM-DD-YYYY_MMM-DD-YYYY_ACCOUNTID.csv`

### Issue: Processing is slow
**Solution**: Use `--clear` flag to skip duplicate checking on first run

## 📚 File Structure

```
NBX/Organic Social Media/
├── Apr-01-2025_Apr-30-2025_1541562187185864.csv
├── Apr-01-2025_Apr-30-2025_2783681948639464.csv
├── Nov-01-2024_Nov-30-2024_1174490457462648.csv
└── ... (more CSV files)
```

Each file contains posts for a specific period and account.

## ✅ Success Indicators

After successful processing, you should see:
```
✨ ALL PROPERTIES PRESERVED:
  ✓ All CSV columns stored as individual database columns
  ✓ No JSONB - direct column access
  ✓ No embeddings - simple and fast
  ✓ Batch processing for maximum speed
  ✓ Safe to re-run - skips existing records
```

## 🎉 Next Steps

1. Run example queries to explore your data
2. Build dashboards using the structured data
3. Integrate with your analytics tools
4. Set up automated processing for new data

## 💡 Tips

- Use `--clear` flag for the fastest initial import
- Re-run without `--clear` to add new posts incrementally
- All columns are directly queryable - no JSON parsing needed
- Use the `content` field for full-text search
- Check the indexes match your most common queries

---

Need help? Check the main README.md or contact support.

