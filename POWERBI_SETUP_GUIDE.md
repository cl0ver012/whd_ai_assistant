# Power BI Data Processing Setup Guide

This guide will help you set up and process Power BI sales data into Supabase.

## Overview

The Power BI processing script:
- ✅ Stores all properties as individual columns (no JSONB)
- ✅ **No embeddings** - simple and fast
- ✅ Handles multiple file formats
- ✅ Removes duplicate headers automatically
- ✅ Clean currency parsing
- ✅ All data preserved

## Data Structure

Your Power BI CSV files should have these columns:
- `Store Name`: Name/location of the store
- `Total Sales`: Sales amount (formatted as $XX,XXX)
- `Year`: Year (e.g., 2025)
- `Month Name`: Month name (e.g., October)

## Supported File Formats

The script handles two filename formats:
1. `powerbi_LFL_Sales_2025_10.csv` (detailed format)
2. `01 25.csv` (short format: MM YY)

## Quick Start

### 1. Prepare Your Environment

Ensure your `.env` file has:
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
```

### 2. Set Up Database Table

Run `setup_powerbi.sql` in your Supabase SQL Editor:

```bash
# The SQL file creates the powerbi_sales table with all necessary indexes
```

### 3. Verify Setup

Run the test script:

```bash
python test_setup_powerbi.py
```

This will check:
- ✓ Environment variables are set
- ✓ Supabase connection works
- ✓ Database table exists
- ✓ Data folder exists
- ✓ CSV files are found

### 4. Process Your Data

Run the processing script:

```bash
python process_powerbi.py
```

The script will:
1. Find all CSV files in `NBX/Power BI/`
2. Parse each row
3. Clean currency values
4. Handle duplicate headers
5. Store in Supabase

## Database Schema

Table: `powerbi_sales`

```sql
CREATE TABLE powerbi_sales (
    id BIGSERIAL PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    month_name TEXT NOT NULL,
    
    -- Store Information
    store_name TEXT NOT NULL,
    
    -- Sales Metrics
    total_sales NUMERIC(12, 2) DEFAULT 0,
    
    -- Optional: Text content
    content TEXT
);
```

## Features

### 1. No Embeddings
Unlike the ads processing scripts, this version **does not use embeddings**. It's:
- ✅ Faster
- ✅ Simpler
- ✅ No AI API costs
- ✅ Direct SQL queries

### 2. Automatic Header Cleaning
Some Power BI exports have duplicate headers throughout the file. The script automatically:
- Detects header rows
- Removes duplicates
- Keeps only data rows

### 3. Smart Currency Parsing
Handles various currency formats:
- `$66,022` → `66022.00`
- `$109,684` → `109684.00`
- Removes $ signs and commas
- Converts to proper decimal format

### 4. Flexible Date Parsing
Extracts year/month from:
- Filename: `powerbi_LFL_Sales_2025_10.csv`
- Filename: `01 25.csv`
- CSV columns: `Year` and `Month Name`

## Querying Your Data

### Example Queries

**1. Total sales by store:**
```sql
SELECT 
    store_name,
    SUM(total_sales) as total_sales
FROM powerbi_sales
GROUP BY store_name
ORDER BY total_sales DESC;
```

**2. Monthly trends:**
```sql
SELECT 
    year,
    month,
    month_name,
    SUM(total_sales) as total_sales,
    COUNT(DISTINCT store_name) as store_count
FROM powerbi_sales
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

**3. Top performing stores in a specific month:**
```sql
SELECT 
    store_name,
    total_sales,
    month_name,
    year
FROM powerbi_sales
WHERE year = '2025' AND month = '10'
ORDER BY total_sales DESC
LIMIT 10;
```

**4. Store performance over time:**
```sql
SELECT 
    store_name,
    month_name,
    year,
    total_sales
FROM powerbi_sales
WHERE store_name = 'Moonee Ponds'
ORDER BY year DESC, month DESC;
```

**5. Search stores by name:**
```sql
SELECT 
    store_name,
    total_sales,
    month_name,
    year
FROM powerbi_sales
WHERE store_name ILIKE '%Melbourne%'
ORDER BY total_sales DESC;
```

## File Structure

```
WHD/
├── NBX/
│   └── Power BI/
│       ├── powerbi_LFL_Sales_2025_06.csv
│       ├── powerbi_LFL_Sales_2025_07.csv
│       ├── powerbi_LFL_Sales_2025_08.csv
│       ├── powerbi_LFL_Sales_2025_09.csv
│       ├── powerbi_LFL_Sales_2025_10.csv
│       ├── 01 25.csv
│       ├── 02 25.csv
│       ├── 03 25.csv
│       ├── 04 25.csv
│       └── 05 25.csv
├── process_powerbi.py          # Main processing script
├── setup_powerbi.sql            # Database setup
├── test_setup_powerbi.py        # Setup verification
└── POWERBI_SETUP_GUIDE.md       # This file
```

## Troubleshooting

### Issue: "Table does not exist"
**Solution:** Run `setup_powerbi.sql` in Supabase SQL Editor first.

### Issue: "No CSV files found"
**Solution:** 
- Check that files are in `NBX/Power BI/` folder
- Verify file extensions are `.csv`

### Issue: "Cannot parse currency values"
**Solution:** 
- The script handles `$XX,XXX` format automatically
- Check that Total Sales column has this format

### Issue: "Duplicate data"
**Solution:** 
- The script processes all files each time
- Consider clearing the table before re-processing:
```sql
DELETE FROM powerbi_sales;
```

### Issue: "Wrong date period"
**Solution:** 
- Verify filename format matches one of:
  - `powerbi_LFL_Sales_2025_10.csv`
  - `01 25.csv`

## Performance

The Power BI script is **fast** because:
- ❌ No embeddings to generate
- ❌ No AI API calls
- ✅ Direct database inserts
- ✅ Simple data structure
- ✅ Efficient indexing

Typical processing speed:
- ~20-50 rows per second
- 100 rows = ~2-5 seconds
- 1000 rows = ~20-50 seconds

## Next Steps

1. ✅ Process your Power BI data
2. 🔍 Query and analyze in Supabase
3. 📊 Build dashboards or reports
4. 🔄 Re-run when you have new data

## Related Scripts

This project includes similar processors for:
- Meta Ads: `process_meta_ads.py`
- Google Ads: `process_google_ads_zero_loss.py`
- TikTok Ads: `process_tiktok_ads_zero_loss.py`

Each follows the same pattern but adapted for different data sources.

## Support

If you encounter issues:
1. Run `test_setup_powerbi.py` to diagnose
2. Check error messages carefully
3. Verify your `.env` file
4. Ensure Supabase table is created
5. Check CSV file formats

---

**Happy Processing! 🚀**

