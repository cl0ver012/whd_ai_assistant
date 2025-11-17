# How to Run SQL in Supabase

Step-by-step guide with visual descriptions.

## 📍 Method 1: SQL Editor (Recommended)

### Step 1: Open Your Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign in with your account
3. You'll see your list of projects
4. **Click on your project** to open the dashboard

### Step 2: Find the SQL Editor

Look at the **left sidebar** of your Supabase dashboard:

```
Left Sidebar Menu:
├── 🏠 Home
├── 📊 Table Editor
├── 🔍 Authentication
├── 📦 Storage
├── 🔌 Edge Functions
├── ⚡ SQL Editor         ← Click here!
├── 📚 Database
├── ⚙️  Settings
└── ...
```

**Click on "SQL Editor"** (it has a lightning bolt ⚡ icon)

### Step 3: Create a New Query

Once in SQL Editor, you'll see:

```
Top of the page:
[+ New query] button
```

1. Click **"+ New query"** button (top left)
2. A blank editor will appear

### Step 4: Paste Your SQL Code

1. **Open** the file `setup_supabase_simple.sql` from your project folder
2. **Copy all the code** (Ctrl+A, then Ctrl+C)
3. **Go back to Supabase SQL Editor**
4. **Paste** the code (Ctrl+V) into the blank editor

You should see something like:
```sql
-- Simple SQL setup without embeddings requirement
-- Stores raw data and metadata only
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS google_ads_documents (
    ...
```

### Step 5: Run the SQL

1. Look for the **"Run"** button (usually green, top right of editor)
2. **Click "Run"** (or press Ctrl+Enter)
3. Wait a few seconds...

### Step 6: Check for Success

After running, you should see:

```
✅ Success message at the bottom
Results panel showing:
status                       | row_count
"Table created successfully!" | 0
```

**That means it worked!** 🎉

---

## 📍 Method 2: Database > Tables (Visual Check)

After running the SQL, verify the table exists:

1. In the left sidebar, click **"Table Editor"** or **"Database"**
2. You should see a table named: **`google_ads_documents`**
3. Click on it to see the columns

You should see columns:
- `id`
- `content`
- `metadata`
- `raw_data`
- `embedding`
- `created_at`
- `updated_at`

---

## 🎯 Complete Visual Guide

### What You'll See:

```
Supabase Dashboard
│
└─ Left Sidebar
   │
   └─ Click "SQL Editor" ⚡
      │
      └─ SQL Editor Page Opens
         │
         ├─ [+ New query] button (top left) ← Click this
         │
         ├─ Editor area (middle) ← Paste SQL code here
         │
         ├─ [Run] button (top right) ← Click to execute
         │
         └─ Results panel (bottom) ← See success/errors here
```

---

## 📋 Step-by-Step Checklist

- [ ] Go to supabase.com and sign in
- [ ] Select your project
- [ ] Click "SQL Editor" in left sidebar
- [ ] Click "+ New query" button
- [ ] Open `setup_supabase_simple.sql` file
- [ ] Copy all the code
- [ ] Paste into Supabase SQL Editor
- [ ] Click "Run" button
- [ ] Wait for success message
- [ ] See "Table created successfully!"

---

## 🎥 Alternative: SQL Editor Shortcut

Some Supabase versions have:

```
Top Navigation Bar:
... | SQL | Settings | ...
      ↑
   Click here (alternative way to open SQL Editor)
```

---

## 🆘 Troubleshooting

### Can't Find SQL Editor?

**Try these locations:**
1. Left sidebar → "SQL Editor" (with ⚡ icon)
2. Left sidebar → "Database" → "SQL Editor" tab
3. Top menu → "SQL"

### "Run" Button Doesn't Work?

**Try:**
- Press `Ctrl+Enter` (Windows) or `Cmd+Enter` (Mac)
- Check if all SQL code is selected
- Look for any error messages in red at the bottom

### Error: "relation already exists"

**This means:**
- The table already exists (that's OK!)
- The SQL ran successfully before
- You can skip this step and continue

### Error: "permission denied"

**This means:**
- You might be using the wrong API key
- Make sure you're logged into the correct Supabase project
- Try refreshing the page and signing in again

---

## ✅ How to Verify It Worked

### Method 1: Check in Table Editor
```
Left sidebar → Table Editor → Look for "google_ads_documents"
```

### Method 2: Run a Quick Query
In SQL Editor, run:
```sql
SELECT COUNT(*) FROM google_ads_documents;
```

Should return: `0` (empty table, ready for data)

### Method 3: Check Columns
In SQL Editor, run:
```sql
SELECT column_name 
FROM information_schema.columns 
WHERE table_name = 'google_ads_documents';
```

Should show: id, content, metadata, raw_data, embedding, created_at, updated_at

---

## 💡 Pro Tips

### Save Your Query
After running the SQL:
1. Click the "..." menu (top right)
2. Click "Save"
3. Name it: "Setup Google Ads Table"
4. You can run it again later if needed

### View Query History
- SQL Editor has a history tab
- Shows all queries you've run
- Can re-run previous queries

### Multiple Queries
You can run multiple SQL statements at once:
- Separate with semicolons `;`
- SQL Editor will run them in order

---

## 🎯 Quick Reference

**Location:** Left Sidebar → SQL Editor ⚡

**Keyboard Shortcut:** `Ctrl+Enter` or `Cmd+Enter` to run

**Success Indicator:** Green checkmark + "Table created successfully!"

**Next Step:** Close SQL Editor and continue with your setup

---

## 📸 What It Looks Like

```
┌─────────────────────────────────────────────────────────┐
│ Supabase Dashboard                              [User]  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Sidebar    │  SQL Editor                              │
│             │                                           │
│  🏠 Home    │  [+ New query]  [Run] [Save]  ...       │
│  📊 Tables  │  ┌─────────────────────────────────────┐ │
│  ⚡ SQL ◄───┤  │ CREATE TABLE IF NOT EXISTS ...      │ │
│  ⚙️  Settings│  │                                     │ │
│             │  │ ...your SQL code here...            │ │
│             │  │                                     │ │
│             │  └─────────────────────────────────────┘ │
│             │                                           │
│             │  Results:                                │
│             │  ✅ Success! Table created               │
└─────────────────────────────────────────────────────────┘
```

---

## ✨ You're Ready!

After running the SQL successfully, you can:

1. ✅ Close the SQL Editor
2. ✅ Continue with your setup
3. ✅ Run the Python script to load data

**Your database is ready to receive data!** 🎉

