# Organic Social Media Data Processing

Quick reference guide for processing organic social media data.

## 🚀 Quick Start

### 1. Setup Database (One Time)

Open Supabase SQL Editor and run:
```sql
-- Copy and paste contents of setup_organic_social.sql
```

### 2. Verify Setup

```bash
source venv/bin/activate
python test_setup_organic_social.py
```

### 3. Process Data

```bash
# Normal mode (incremental)
python process_organic_social.py

# Fast mode (clears existing data first)
python process_organic_social.py --clear
```

## 📊 What Gets Processed

- **24 CSV files** from `NBX/Organic Social Media/`
- **Instagram posts** (images, reels, videos)
- **Engagement metrics** (views, likes, comments, shares, saves)
- **Account information** (username, account name, account ID)

## 📁 Data Structure

### Input Files
```
NBX/Organic Social Media/
├── Nov-01-2024_Nov-30-2024_1174490457462648.csv
├── Dec-01-2024_Dec-31-2024_1144231361188601.csv
├── Jan-01-2025_Jan-31-2025_1337112227467239.csv
└── ... (21 more files)
```

### CSV Columns
- Post ID, Account ID, Account username, Account name
- Description, Duration (sec), Publish time, Permalink
- Post type, Data comment, Date
- Views, Reach, Likes, Shares, Follows, Comments, Saves

### Database Table
All data stored in `organic_social_media` table with:
- Individual columns for each metric (no JSONB)
- Indexed for fast queries
- Full-text search enabled

## 🔍 Quick Queries

### Top Posts by Views
```sql
SELECT account_username, post_type, description, views, likes, permalink
FROM organic_social_media
ORDER BY views DESC LIMIT 10;
```

### Monthly Performance
```sql
SELECT year, month_name, COUNT(*) as posts, 
       SUM(views) as total_views, SUM(likes) as total_likes
FROM organic_social_media
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

### Video Content
```sql
SELECT description, duration_sec, views, likes, permalink
FROM organic_social_media
WHERE is_video = TRUE
ORDER BY views DESC;
```

## ✅ Features

- ✅ All CSV properties preserved as individual columns
- ✅ No JSONB - direct column access
- ✅ No embeddings - simple and fast
- ✅ Batch processing (100 rows at a time)
- ✅ Automatic duplicate detection
- ✅ Safe to re-run
- ✅ Full-text search
- ✅ Comprehensive indexing

## 📚 Documentation

- **ORGANIC_SOCIAL_SETUP_GUIDE.md** - Detailed setup and usage
- **ORGANIC_SOCIAL_IMPLEMENTATION_SUMMARY.md** - Technical details
- **setup_organic_social.sql** - Database schema
- **process_organic_social.py** - Processing script
- **test_setup_organic_social.py** - Setup verification

## 🔧 Troubleshooting

**Table doesn't exist?**
→ Run `setup_organic_social.sql` in Supabase SQL Editor

**Missing environment variables?**
→ Check `.env` file has `SUPABASE_URL` and `SUPABASE_KEY`

**Processing slow?**
→ Use `--clear` flag for first run

## 💡 Tips

1. Use `--clear` for fastest initial import
2. Run without `--clear` for incremental updates
3. All columns are directly queryable
4. Check `content` field for full-text search
5. Use computed fields (`has_views`, `has_engagement`, `is_video`) for filtering

## 🎯 Next Steps

1. ✅ Run setup SQL
2. ✅ Test connection
3. ✅ Process data
4. 📊 Build queries
5. 📈 Create dashboards
6. 🚀 Automate updates

---

**Need more details?** See `ORGANIC_SOCIAL_SETUP_GUIDE.md`

