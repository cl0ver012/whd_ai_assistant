# Quick Start - Simple Version ⚡

Get your data into Supabase in 5 minutes! No Google API needed.

## ✅ What You Need

- Supabase account (free)
- Your Google Ads CSV files
- 5 minutes

## 🚀 3-Step Setup

### Step 1: Get Supabase Credentials (2 minutes)

1. Go to [supabase.com](https://supabase.com) and sign in
2. Select your project (or create new one)
3. Click **Settings** (⚙️) → **API**
4. Copy these 2 values:
   - **Project URL** (e.g., `https://xxxxx.supabase.co`)
   - **anon public key** (starts with `eyJ...`)

### Step 2: Setup Database (1 minute)

1. In Supabase, click **SQL Editor** (⚡ in left sidebar)
2. Click **"+ New query"**
3. Open `setup_supabase_simple.sql` from this project
4. Copy all the SQL code
5. Paste into Supabase SQL Editor
6. Click **"Run"** (or press Ctrl+Enter)

You should see: ✅ "Table created successfully!"

**📖 Detailed guide:** [HOW_TO_RUN_SQL.md](HOW_TO_RUN_SQL.md)

### Step 3: Configure & Run (2 minutes)

```bash
# Install dependencies
pip install -r requirements_simple.txt

# Create .env file (use notepad or any text editor)
# Add these 2 lines with YOUR credentials:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key_here

# Test setup
python test_setup_simple.py

# Process your data!
python process_google_ads_simple.py
```

## ✅ What Happens

The script will:
1. Read all CSV files from `NBX/Google Ads Export/`
2. Store 100% of original data
3. Create queryable metadata
4. Show progress as it runs

**Time:** ~5-10 minutes for 3,000 rows

## 🎉 Done!

Check your Supabase dashboard - your data is there!

Query it:
```sql
SELECT * FROM google_ads_documents LIMIT 10;
```

## 💡 Next Steps

- Query your data with SQL
- Build dashboards
- Later: Add embeddings for AI features

## 🆘 Problems?

### "Module not found"
```bash
pip install -r requirements_simple.txt
```

### "Table does not exist"
Run `setup_supabase_simple.sql` in Supabase SQL Editor

### "Can't find .env"
Make sure the file is named exactly `.env` (with dot, no .txt)

---

**That's it! Fast, simple, effective.** 🎯

