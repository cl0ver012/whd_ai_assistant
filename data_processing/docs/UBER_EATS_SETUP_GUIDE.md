# Uber Eats Promos Setup Guide

Complete guide for processing and storing Uber Eats promotional offers and sales data in Supabase.

## Overview

This system processes two types of Uber Eats data:
1. **Promotional Offers** - Marketing promotions and discounts
2. **Sales Data** - Daily sales by store and channel

All data is stored in Supabase with **all original CSV columns preserved** as individual database columns. No JSONB, no embeddings - simple and fast!

## Features

✅ **Zero Data Loss** - All CSV columns preserved as database columns  
✅ **Fast Batch Processing** - 100 rows at a time  
✅ **Duplicate Detection** - Automatically skips existing records  
✅ **Two Data Types** - Handles both offers and sales files  
✅ **Date Parsing** - Intelligent date format handling  
✅ **Computed Fields** - Automatic calculation of useful metrics  

## File Structure

### Expected CSV Files

The script processes files in `NBX/Uber Eats Promos/`:

1. **Offers Files** (containing "Offers" in filename):
   - Example: `UberEats Offers - 12 Months.csv`
   - Columns: Offer, Promo Start Date, Promo End Date, Customer Targeting, Items

2. **Sales Files** (containing "Sales" in filename):
   - Example: `UberEats Sales - Export.csv`
   - Columns: Date, Store Name, Channel Type, Total Sales

## Database Tables

### Table 1: `uber_eats_offers`

Stores promotional offers data.

**Original CSV Columns:**
- `offer` - TEXT - Offer description (e.g., "20% off select items")
- `promo_start_date` - TEXT - Promotion start date
- `promo_end_date` - TEXT - Promotion end date
- `customer_targeting` - TEXT - Customer targeting criteria
- `items` - TEXT - Items included in the promotion

**Computed Fields:**
- `has_discount` - BOOLEAN - True if offer contains % or "off"
- `has_fixed_price` - BOOLEAN - True if offer has fixed price (e.g., "$15 items")

**System Fields:**
- `id` - BIGSERIAL - Primary key
- `file_name` - TEXT - Source file name
- `content` - TEXT - Human-readable description
- `created_at` - TIMESTAMPTZ - Creation timestamp
- `updated_at` - TIMESTAMPTZ - Update timestamp

### Table 2: `uber_eats_sales`

Stores sales data by store and channel.

**Original CSV Columns:**
- `date` - TEXT - Original date string from CSV
- `store_name` - TEXT - Store name
- `channel_type` - TEXT - Sales channel (e.g., "Uber")
- `total_sales` - NUMERIC(10, 2) - Total sales amount

**Parsed Fields:**
- `parsed_date` - DATE - Parsed date for querying
- `year` - TEXT - Year extracted from date
- `month` - TEXT - Month number (01-12)
- `month_name` - TEXT - Month name (e.g., "October")
- `period` - TEXT - Format: YYYY_MM (e.g., "2024_10")

**Computed Fields:**
- `has_sales` - BOOLEAN - True if total_sales > 0

**System Fields:**
- `id` - BIGSERIAL - Primary key
- `file_name` - TEXT - Source file name
- `content` - TEXT - Human-readable description
- `created_at` - TIMESTAMPTZ - Creation timestamp
- `updated_at` - TIMESTAMPTZ - Update timestamp

## Setup Instructions

### Step 1: Create Database Tables

Run the SQL setup file in your Supabase SQL Editor:

```sql
-- File: data_processing/sql/setup_uber_eats_promos.sql
```

Or via command line:
```bash
psql -h your-supabase-host -U postgres -d postgres -f data_processing/sql/setup_uber_eats_promos.sql
```

This creates:
- `uber_eats_offers` table with indexes
- `uber_eats_sales` table with indexes
- Row Level Security policies (optional)

### Step 2: Configure Environment

Ensure your `.env` file contains:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key
```

### Step 3: Install Dependencies

```bash
pip install pandas supabase python-dotenv
```

### Step 4: Process Data

#### Option A: Normal Mode (Recommended)
Skips existing records - safe to re-run:

```bash
python data_processing/scripts/process_uber_eats_promos.py
```

#### Option B: Fresh Start Mode
Deletes all existing data first (faster, no duplicate checks):

```bash
python data_processing/scripts/process_uber_eats_promos.py --clear
```

## How It Works

### Processing Flow

1. **File Detection**
   - Scans `NBX/Uber Eats Promos/` for CSV files
   - Identifies offers files (contains "Offers")
   - Identifies sales files (contains "Sales")

2. **Data Reading**
   - Reads CSV files with pandas
   - Handles various date formats automatically

3. **Data Processing**
   - **Offers**: Extracts promo details, identifies discount types
   - **Sales**: Parses dates, extracts period information

4. **Duplicate Detection**
   - Queries existing records once per file
   - Fast set-based lookup for duplicates
   - Skips records already in database

5. **Batch Insert**
   - Collects 100 rows at a time
   - Inserts in batches for speed
   - No artificial delays

6. **Progress Tracking**
   - Real-time progress updates
   - Success/failed/skipped counts
   - Performance metrics (records/second)

### Date Format Handling

The script automatically handles multiple date formats:

**Sales Files:**
- "Tuesday, October 01, 2024" → 2024-10-01
- Extracts: year, month, month_name, period

**Offers Files:**
- "1-Jul-24" → 2024-07-01
- "15-Jul-24" → 2024-07-15

## Example Queries

### Query Offers

```sql
-- All active promotions
SELECT offer, promo_start_date, promo_end_date, items
FROM uber_eats_offers
ORDER BY promo_start_date DESC;

-- Discount promotions only
SELECT offer, customer_targeting, items
FROM uber_eats_offers
WHERE has_discount = true;

-- Fixed price promotions
SELECT offer, items
FROM uber_eats_offers
WHERE has_fixed_price = true;
```

### Query Sales

```sql
-- Sales by store for a specific month
SELECT store_name, SUM(total_sales) as total
FROM uber_eats_sales
WHERE period = '2024_10'
GROUP BY store_name
ORDER BY total DESC;

-- Daily sales for a specific store
SELECT parsed_date, total_sales
FROM uber_eats_sales
WHERE store_name = 'Albany Creek'
ORDER BY parsed_date DESC;

-- Monthly sales summary
SELECT year, month_name, COUNT(*) as transactions, SUM(total_sales) as total
FROM uber_eats_sales
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;

-- Top performing stores
SELECT store_name, COUNT(*) as orders, SUM(total_sales) as total_revenue
FROM uber_eats_sales
WHERE has_sales = true
GROUP BY store_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### Combined Analysis

```sql
-- Sales during promotional periods
-- (This is a conceptual query - adjust based on your date matching needs)
SELECT 
    s.period,
    s.store_name,
    COUNT(DISTINCT o.offer) as active_promos,
    SUM(s.total_sales) as sales
FROM uber_eats_sales s
LEFT JOIN uber_eats_offers o ON 
    -- Add your date matching logic here
    true
GROUP BY s.period, s.store_name
ORDER BY s.period DESC, sales DESC;
```

## Data Preservation

### What's Preserved

✅ **All CSV Columns** - Every column from the CSV files  
✅ **Original Values** - No modifications to source data  
✅ **Original Format** - Dates stored as-is plus parsed versions  
✅ **Computed Fields** - Added for convenience without losing originals  

### What's Added

- `id` - Database primary key
- `file_name` - Source file tracking
- `content` - Human-readable text for search
- `created_at` / `updated_at` - Timestamps
- Computed boolean flags (offers: `has_discount`, `has_fixed_price`)
- Computed sales metrics (sales: `has_sales`)
- Parsed date fields (sales: `parsed_date`, `year`, `month`, etc.)

## Performance

### Expected Performance

- **Offers**: ~1,000 records/second
- **Sales**: ~500-1,000 records/second
- **Batch Size**: 100 rows (configurable)
- **No Delays**: Maximum speed processing

### Optimization Tips

1. **First Run**: Use `--clear` flag if starting fresh (fastest)
2. **Re-runs**: Normal mode skips duplicates automatically
3. **Large Files**: Batch processing handles files of any size
4. **Network**: Ensure good connection to Supabase for best speed

## Troubleshooting

### Common Issues

**Issue**: "Error: Missing environment variables"
- **Solution**: Check `.env` file contains `SUPABASE_URL` and `SUPABASE_KEY`

**Issue**: "Error: Data folder not found"
- **Solution**: Ensure `NBX/Uber Eats Promos/` folder exists with CSV files

**Issue**: "Error storing batch"
- **Solution**: Check database tables exist (run SQL setup first)
- **Solution**: Verify Supabase credentials are correct

**Issue**: Dates not parsing correctly
- **Solution**: The script handles multiple formats automatically
- **Solution**: Check CSV date format matches expected patterns

**Issue**: Duplicates being created
- **Solution**: The script checks duplicates based on key fields
- **Solution**: Offers: (offer, promo_start_date, promo_end_date)
- **Solution**: Sales: (date, store_name, channel_type, total_sales)

### Getting Help

If you encounter issues:
1. Check the console output for specific error messages
2. Verify database tables exist and are accessible
3. Check CSV file format matches expected structure
4. Review the SQL setup file for table definitions

## File Locations

```
data_processing/
├── scripts/
│   └── process_uber_eats_promos.py    # Main processing script
├── sql/
│   └── setup_uber_eats_promos.sql     # Database setup
└── docs/
    └── UBER_EATS_SETUP_GUIDE.md       # This file

NBX/
└── Uber Eats Promos/
    ├── UberEats Offers - 12 Months.csv
    └── UberEats Sales - Export.csv
```

## Next Steps

1. ✅ Create database tables (Step 1)
2. ✅ Configure environment (Step 2)
3. ✅ Install dependencies (Step 3)
4. ✅ Run processing script (Step 4)
5. 📊 Query your data in Supabase
6. 🔄 Re-run anytime to add new data

## Summary

This implementation provides a complete solution for Uber Eats promotional data:
- **Zero data loss** - all CSV columns preserved
- **Fast processing** - batch inserts with no delays
- **Duplicate-safe** - can be run multiple times
- **Two data types** - handles both offers and sales
- **Production-ready** - robust error handling and logging

Your Uber Eats data is now ready for analysis! 🎉

