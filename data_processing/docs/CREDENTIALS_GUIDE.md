# Getting Your API Credentials

Complete guide to get all the credentials you need for this project.

## 🔑 Required Credentials

You need **3 credentials** total:

1. **Supabase URL** - Your project's URL
2. **Supabase Key** - API key to access your database
3. **Google API Key** - For generating embeddings with Gemini

---

## 📦 Part 1: Supabase Credentials

### Step 1: Create/Access Your Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign in (or create a free account)
3. Click **"New Project"** or select an existing project

### Step 2: Get Your Supabase URL

1. In your Supabase project dashboard
2. Click **⚙️ Settings** in the left sidebar (bottom)
3. Click **API** under "Configuration"
4. Find **"Project URL"** section
5. Copy the URL (looks like: `https://xxxxxxxxxxxxx.supabase.co`)

**Example:**
```
https://abcdefghijklmnop.supabase.co
```

### Step 3: Get Your Supabase Key

1. On the same **Settings → API** page
2. Find **"Project API keys"** section
3. Copy the **"anon public"** key (NOT the service_role key!)
4. It looks like: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

**Important Notes:**
- ✅ Use the `anon` / `public` key (safe for client-side use)
- ❌ **DO NOT** use the `service_role` key (too powerful, security risk)
- The `anon` key is already restricted by Row Level Security (RLS)

**Visual Guide:**
```
Supabase Dashboard
└── Settings (⚙️)
    └── API
        ├── Project URL: https://xxxxx.supabase.co  ← Copy this
        └── Project API keys:
            ├── anon public: eyJhbGc...             ← Copy this (use this one!)
            └── service_role: eyJhbGc...            ← DON'T use (dangerous)
```

---

## 🤖 Part 2: Google Gemini API Key

### Step 1: Go to Google AI Studio

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account

**Direct link:** https://makersuite.google.com/app/apikey

### Step 2: Create API Key

1. Click **"Get API Key"** or **"Create API Key"**
2. Choose **"Create API key in new project"** (or use existing project)
3. Your key will be generated (looks like: `AIzaSyD...`)
4. **Copy the key immediately** (you may not see it again!)

### Step 3: Verify API Access

1. The key should work immediately
2. Free tier includes:
   - ✅ 60 requests per minute
   - ✅ 1,500 requests per day
   - ✅ Enough for ~3,000+ embeddings

**Visual Guide:**
```
Google AI Studio
└── Get API Key button
    └── Create API key in new project
        └── Your API key: AIzaSyD...  ← Copy this
```

---

## 📝 Part 3: Create Your .env File

### Step 1: Create the File

In your project folder (`WHD/`), create a file named `.env` (with the dot at the start)

**On Windows:**
- Right-click in folder → New → Text Document
- Rename to `.env` (remove the .txt extension)
- If Windows hides extensions, use: `notepad .env` in Command Prompt

**On Mac/Linux:**
```bash
touch .env
nano .env
```

### Step 2: Add Your Credentials

Open `.env` and add your credentials:

```env
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.your-actual-key-here
GOOGLE_API_KEY=AIzaSyD-your-actual-key-here
```

**Example with fake credentials:**
```env
SUPABASE_URL=https://abcdefghijklmnop.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFiY2RlZmdoaWprbG1ub3AiLCJyb2xlIjoiYW5vbiIsImlhdCI6MTYyMzAwMDAwMCwiZXhwIjoxOTM4NTc2MDAwfQ.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz
```

### Step 3: Important Rules

✅ **DO:**
- No spaces around `=`
- No quotes around values
- Each credential on its own line
- Save the file in the root of your project

❌ **DON'T:**
- Add spaces: `SUPABASE_URL = xxx` ❌
- Use quotes: `SUPABASE_URL="xxx"` ❌
- Commit to Git (already in .gitignore)
- Share your .env file

---

## 🧪 Part 4: Test Your Credentials

Run the test script:

```bash
python test_setup.py
```

### Expected Output:

```
============================================================
Google Ads Data Processing - Setup Test
============================================================
Testing Environment Variables...
  ✓ SUPABASE_URL is set
  ✓ SUPABASE_KEY is set
  ✓ GOOGLE_API_KEY is set

Testing Supabase Connection...
  ✓ Successfully connected to Supabase
  ✓ Table 'google_ads_documents' is accessible

Testing Google Gemini API...
  ✓ Successfully generated embedding
  ✓ Embedding dimension: 768

Testing Data Folder...
  ✓ Data folder exists: NBX/Google Ads Export
  ✓ Found 20 performance files
  ✓ Found 13 action files

============================================================
Test Results Summary
============================================================
✅ All tests passed! You're ready to run process_google_ads_zero_loss.py
```

### If Tests Fail:

#### ❌ "SUPABASE_URL is NOT set"
- Check your `.env` file exists in the project root
- Check the variable name is exact: `SUPABASE_URL` (all caps)
- No spaces or quotes

#### ❌ "Table does not exist"
- You need to run `setup_supabase_enhanced.sql` in Supabase first
- Go to Supabase → SQL Editor → paste and run the SQL

#### ❌ "Supabase connection failed"
- Check your URL is correct (should end with `.supabase.co`)
- Check your key is the `anon` key, not `service_role`
- Check no extra spaces in `.env` file

#### ❌ "Gemini API test failed"
- Check your API key starts with `AIzaSy`
- Make sure you're using the correct key from AI Studio
- Check you haven't hit rate limits (unlikely on first test)

---

## 🔒 Security Best Practices

### ✅ DO:
- Keep your `.env` file local (never commit)
- Use the `anon` key for Supabase (not `service_role`)
- Regenerate keys if accidentally exposed
- Use Row Level Security (RLS) in production

### ❌ DON'T:
- Commit `.env` to Git (already in .gitignore ✅)
- Share your credentials publicly
- Use `service_role` key (too powerful)
- Hardcode keys in scripts

---

## 📊 API Limits & Costs

### Supabase Free Tier:
- ✅ 500 MB database
- ✅ 1 GB file storage
- ✅ 5 GB bandwidth
- ✅ 50,000 monthly active users
- ✅ More than enough for this project!

### Google Gemini Free Tier:
- ✅ 60 requests per minute
- ✅ 1,500 requests per day
- ✅ Free embeddings (generous limits)
- ✅ Can process ~3,000+ records easily

**Your ~3,000 rows will cost: $0** (within free tiers) 🎉

---

## 🆘 Troubleshooting

### Problem: Can't find Supabase API page
**Solution:** 
1. Go to your project dashboard
2. Look for ⚙️ icon at bottom of left sidebar
3. Click "Settings" → "API"

### Problem: Google AI Studio link not working
**Solution:**
- Try: https://aistudio.google.com/app/apikey
- Or: https://makersuite.google.com/app/apikey
- Or: Search "Google AI Studio API Key"

### Problem: .env file not working
**Solution:**
- Make sure filename is exactly `.env` (with dot, no extension)
- File must be in project root (same folder as scripts)
- Check file isn't named `.env.txt` (Windows sometimes hides extensions)

### Problem: "Invalid API key" errors
**Solution:**
- Make sure you copied the entire key (they're very long)
- Check no extra spaces before/after the key
- Regenerate the key if needed

---

## 📝 Quick Checklist

Before running the main script, verify:

- [ ] Created Supabase account & project
- [ ] Copied Supabase URL from Settings → API
- [ ] Copied Supabase `anon` key (not service_role)
- [ ] Created Google AI Studio API key
- [ ] Created `.env` file in project root
- [ ] Added all 3 credentials to `.env`
- [ ] No quotes or spaces in `.env` file
- [ ] Ran `setup_supabase_enhanced.sql` in Supabase
- [ ] Ran `python test_setup.py` successfully

All checked? You're ready! ✅

---

## 🎯 Summary

**What you need:**
1. Supabase URL (from Settings → API)
2. Supabase anon key (from Settings → API)
3. Google API key (from AI Studio)

**Where it goes:**
All three in a `.env` file in your project root

**Test it:**
```bash
python test_setup.py
```

**Start processing:**
```bash
python process_google_ads_zero_loss.py
```

---

## 💡 Pro Tips

1. **Bookmark these pages:**
   - Supabase: Settings → API (for quick access)
   - Google AI Studio: https://makersuite.google.com/app/apikey

2. **Save credentials securely:**
   - Use a password manager
   - Don't email them to yourself
   - Don't screenshot and save to cloud

3. **Multiple environments:**
   - Use `.env.development` and `.env.production`
   - Never mix development and production keys

4. **Regenerate if compromised:**
   - Supabase: Settings → API → "Reset Database Password"
   - Google: Revoke old key, create new one

---

**Ready to process your data with zero data loss!** 🚀

