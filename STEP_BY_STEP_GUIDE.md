# Build Your AI Assistant - Step by Step

## ✅ Cleaned Up!

I've removed all the messy workflow files. Now we have:
- **`step1_generate_sql.json`** - Just generates SQL (test this first!)
- **`n8n_gemini_simple.json`** - Complete workflow (use after Step 1 works)

---

## 🎯 Step 1: Test SQL Generation

Let's start with the simplest possible workflow - just generate SQL from a question.

### Your Database Schema

The LLM knows about **6 tables**:

**JSONB Tables** (use metadata->>'field'):
1. `google_ads_documents` - Google Ads with JSONB metadata
2. `tiktok_ads_documents` - TikTok Ads with JSONB metadata

**Structured Tables** (use direct column names):
3. `tiktok_ads_performance` - TikTok Ads with typed columns
4. `meta_ads_performance` - Meta/Facebook Ads with typed columns
5. `organic_social_media` - Instagram posts with typed columns
6. `powerbi_sales` - Power BI sales data with typed columns

**See full schema:** `llm_sql_prompt.txt`

### Import the Workflow

1. Import **`step1_generate_sql.json`** into n8n
2. You'll see **4 simple nodes:**
   - Webhook (receives question)
   - Gemini Generate SQL (calls Gemini API with comprehensive prompt)
   - Extract SQL (cleans up the response)
   - Respond (returns the result)

### Configure Google API Key

1. Get your API key from: https://makersuite.google.com/app/apikey
2. In the **"Gemini Generate SQL"** node:
3. Find the line that says:
   ```
   "value": "PUT_YOUR_GOOGLE_API_KEY_HERE"
   ```
4. Replace `PUT_YOUR_GOOGLE_API_KEY_HERE` with your actual API key
5. Example:
   ```
   "value": "AIzaSyD1234567890abcdefghijklmnopqrstuvwxyz"
   ```

### Activate & Test

1. Click **"Active"** toggle
2. Copy the test webhook URL (will be shown)
3. Test in Postman!

---

## 🧪 Test in Postman

**Method:** `POST`

**URL:** (Copy from n8n test webhook)
```
https://w-h-d.app.n8n.cloud/webhook-test/step1-test
```

**Body (JSON):**
```json
{
  "question": "What is our total Google Ads spend?"
}
```

**Expected Response:**
```json
{
  "success": true,
  "question": "What is our total Google Ads spend?",
  "sql": "SELECT SUM((((metadata::jsonb->>0)::jsonb)->>'cost')::float) as total_spend FROM google_ads_documents",
  "prompt": "The user asked about total Google Ads spending. Analyze the total_spend value and provide a clear answer formatted as currency (e.g., $45,678.90). Add brief context about the spending level.",
  "raw_gemini_response": { ... }
}
```

**The LLM now returns TWO properties with TWO MODES:**

**MODE 1 - Question needs data (sql has query):**
1. **`sql`** - The SQL query to execute
2. **`prompt`** - Instructions for another LLM on HOW to analyze results and answer

**MODE 2 - Question doesn't need data (sql is empty):**
1. **`sql`** - Empty string `""`
2. **`prompt`** - DIRECT FINAL ANSWER to the user (ready to display)

**Examples:**
- "Hello" → `sql=""`, `prompt="Hello! I'm your assistant..."`
- "What is our total spend?" → `sql="SELECT SUM(...)"`, `prompt="Present total as currency"`

### Try Different Questions

**MODE 1 - Non-Data Questions (sql will be empty, prompt is direct answer):**
```json
{"question": "Hello"}
{"question": "What can you help me with?"}
{"question": "Thank you"}
```

Expected response:
```json
{
  "sql": "",
  "prompt": "Hello! I'm your marketing analytics assistant...",
  "needs_database": false
}
```

**MODE 2 - Data Questions (sql will be query, prompt is instructions):**

**Google Ads (JSONB):**
```json
{"question": "What is our total Google Ads spend?"}
{"question": "Show me top 5 Google campaigns by clicks"}
{"question": "What is the average CTR for Google Ads?"}
```

**TikTok (Structured):**
```json
{"question": "What is our total TikTok Ads spend?"}
{"question": "Show me top TikTok campaigns by video views"}
```

**Meta (Structured):**
```json
{"question": "Show me Meta campaigns with the most link clicks"}
```

**Multi-Table:**
```json
{"question": "Compare Google Ads and TikTok Ads spend"}
{"question": "Show me total spend across all platforms"}
```

Expected response:
```json
{
  "sql": "SELECT SUM(...) FROM ...",
  "prompt": "Instructions for analyzing the data...",
  "needs_database": true
}
```

---

## ✅ Success Criteria

If you see:
- ✅ `"success": true`
- ✅ `"generated_sql"` contains a SELECT query
- ✅ No errors

**Then Step 1 is working!** Tell me and we'll move to Step 2 (executing the SQL).

---

## 🐛 If You Get Errors

### "Invalid API key"
→ Check your Google API key is correct
→ Make sure you replaced `PUT_YOUR_GOOGLE_API_KEY_HERE`

### "Model not found" or "403"
→ Your API key might not have access to Gemini
→ Try creating a new key at https://makersuite.google.com/app/apikey

### "Network error"
→ Check your internet connection
→ Make sure n8n can reach external APIs

---

## 📊 What We're Testing

This simple workflow tests:
1. ✅ Webhook receives data correctly
2. ✅ Gemini API call works
3. ✅ Response parsing works
4. ✅ SQL generation quality

Once this works, we'll add:
- Step 2: Execute the SQL in Supabase
- Step 3: Format the results
- Step 4: Generate natural language answer

---

## 🎯 Next Steps

**After Step 1 works:**

1. Test with different questions:
   ```
   "What is the average CTR?"
   "Show me top 5 campaigns"
   "Which campaigns have conversions?"
   ```

2. Verify the SQL queries look correct

3. Tell me it works, and I'll give you Step 2!

---

## 📝 Current File Structure

```
✅ KEEP THESE:
  - step1_generate_sql.json          (Step 1 - Test first!)
  - n8n_gemini_simple.json           (Complete workflow - Use after Step 1 works)
  - chat_interface.html              (Web UI)
  - test_n8n_webhook.py              (Testing script)
  
📖 DOCUMENTATION:
  - STEP_BY_STEP_GUIDE.md            (This file - Your guide!)
  - N8N_TROUBLESHOOTING.md           (If you have issues)
  - SUPABASE_FIX_GUIDE.md            (Supabase setup help)
```

---

**Import `step1_generate_sql.json` and test it in Postman. Let me know what happens!** 🚀

