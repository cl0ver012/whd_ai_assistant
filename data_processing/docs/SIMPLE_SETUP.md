# Simple Setup - No Embeddings

Fast and easy setup - just store your data directly in Supabase!

## 🎯 What This Does

- ✅ Stores 100% of your original CSV data
- ✅ Creates queryable metadata
- ✅ Fast processing (no API calls for embeddings)
- ✅ Only requires Supabase (no Google API needed)
- ⏭️ Skip embeddings for now (can add later)

## 🚀 Quick Start (3 Steps!)

### Step 1: Install Dependencies

```bash
pip install -r requirements_simple.txt
```

### Step 2: Setup Supabase

1. Go to your Supabase project
2. Click **"SQL Editor"** in left sidebar (⚡ icon)
3. Click **"+ New query"** button
4. Copy and paste contents of `setup_supabase_simple.sql`
5. Click **"Run"** button (or press Ctrl+Enter)

**📖 Need help? See detailed guide: [HOW_TO_RUN_SQL.md](HOW_TO_RUN_SQL.md)**

You should see: ✅ "Table created successfully!"

### Step 3: Configure .env

Create a `.env` file with just 2 credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_key
```

**Get these from:** Supabase Dashboard → Settings → API

## ✅ Test Your Setup

```bash
python test_setup_simple.py
```

Should see:
```
✅ All tests passed! You're ready to run process_google_ads_simple.py
```

## 🎯 Process Your Data

```bash
python process_google_ads_simple.py
```

This will:
- ✅ Read all CSV files from `NBX/Google Ads Export/`
- ✅ Store raw original data (100% preservation)
- ✅ Create processed metadata (for queries)
- ✅ Store text content (human-readable)
- ⏭️ Skip embeddings (much faster!)

**Time:** ~5-10 minutes for 3,000 rows (10x faster than with embeddings!)

## 📊 What Gets Stored

```json
{
  "raw_data": {
    "original_row": {
      "Day": "2024-11-01",
      "Campaign": "[WHD] Display",
      "Impr.": "1,618",     // Original with comma
      "CTR": "1.85%",       // Original with %
      ...all 13 columns
    }
  },
  "metadata": {
    "day": "2024-11-01",
    "campaign": "[WHD] Display",
    "impressions": 1618,    // Cleaned for queries
    "ctr": 1.85,            // Cleaned for queries
    ...all fields
  },
  "content": "Google Ads Performance Record...",
  "embedding": null        // No embedding yet
}
```

## 🔍 Query Your Data

### Total cost by campaign
```sql
SELECT 
    metadata->>'campaign' as campaign,
    SUM((metadata->>'cost')::float) as total_cost
FROM google_ads_documents
GROUP BY metadata->>'campaign'
ORDER BY total_cost DESC;
```

### Filter by date
```sql
SELECT *
FROM google_ads_documents
WHERE metadata->>'day' = '2024-11-01';
```

### Find conversions
```sql
SELECT 
    metadata->>'campaign' as campaign,
    metadata->>'day' as day,
    (metadata->>'conversions')::float as conversions
FROM google_ads_documents
WHERE (metadata->>'conversions')::float > 0
ORDER BY conversions DESC;
```

## ⚡ Benefits of Simple Version

### Advantages:
- ✅ **10x faster** - No API calls for embeddings
- ✅ **Simpler setup** - Only need Supabase
- ✅ **No costs** - No embedding API usage
- ✅ **All data preserved** - Still have 100% of your data
- ✅ **Can add embeddings later** - Not locked in

### What You're Missing (for now):
- ❌ Semantic search ("find similar campaigns")
- ❌ Vector similarity search
- ❌ AI-powered recommendations

**But you can add these later!**

## 💡 Add Embeddings Later

When you're ready for AI features:

1. Install embedding dependencies:
   ```bash
   pip install google-generativeai
   ```

2. Add Google API key to `.env`:
   ```env
   GOOGLE_API_KEY=your_key
   ```

3. Run the full version:
   ```bash
   python process_google_ads_zero_loss.py
   ```

Or update existing records with embeddings.

## 📁 Files for Simple Setup

```
Essential Files:
├── process_google_ads_simple.py      ← Run this
├── setup_supabase_simple.sql         ← Run in Supabase
├── test_setup_simple.py              ← Test your setup
├── requirements_simple.txt           ← Simple dependencies
└── SIMPLE_SETUP.md                   ← This file
```

## 🆘 Troubleshooting

### "Table does not exist"
→ Run `setup_supabase_simple.sql` in Supabase SQL Editor

### "Missing environment variables"
→ Create `.env` file with SUPABASE_URL and SUPABASE_KEY

### "Module not found"
→ Run `pip install -r requirements_simple.txt`

### "Can't find data folder"
→ Ensure `NBX/Google Ads Export/` folder exists with CSV files

## ✅ Checklist

- [ ] Installed dependencies (`requirements_simple.txt`)
- [ ] Ran `setup_supabase_simple.sql` in Supabase
- [ ] Created `.env` with Supabase credentials
- [ ] Tested setup (`test_setup_simple.py`)
- [ ] Data folder exists with CSV files
- [ ] Ready to process!

## 🎉 That's It!

Run:
```bash
python process_google_ads_simple.py
```

Your data will be stored with zero loss, ready to query!

**Fast, simple, and effective.** 🚀

