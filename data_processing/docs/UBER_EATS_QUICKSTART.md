# Uber Eats Promos - Quick Start Guide

Get your Uber Eats promotional and sales data into Supabase in 3 easy steps!

## 🚀 Quick Start (3 Steps)

### Step 1: Create Database Tables

Open Supabase SQL Editor and run:

```sql
-- Copy and paste the entire contents of:
-- data_processing/sql/setup_uber_eats_promos.sql
```

Or use command line (if you have psql):

```bash
psql -h your-project.supabase.co -U postgres -d postgres -f data_processing/sql/setup_uber_eats_promos.sql
```

This creates:
- ✅ `uber_eats_offers` table (promotional offers)
- ✅ `uber_eats_sales` table (sales by store)

### Step 2: Verify Environment

Make sure your `.env` file has:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-service-role-key-here
```

### Step 3: Run the Script

```bash
python data_processing/scripts/process_uber_eats_promos.py
```

That's it! 🎉

## 📊 What Gets Processed

The script automatically finds and processes:

1. **Offers Files**: `*Offers*.csv` (65 rows detected)
   - Promotional campaigns
   - Discount types
   - Target customers
   - Included items

2. **Sales Files**: `*Sales*.csv` (121,022 rows detected)
   - Daily sales by store
   - Channel information
   - Sales amounts
   - Date/time data

## ⚡ Performance

- **Speed**: ~500-1,000 records/second
- **Batch Processing**: 100 rows at a time
- **Safe to Re-run**: Automatically skips duplicates
- **No Data Loss**: All CSV columns preserved

## 🔍 Quick Query Examples

### View Latest Offers

```sql
SELECT offer, promo_start_date, promo_end_date, items
FROM uber_eats_offers
ORDER BY promo_start_date DESC
LIMIT 10;
```

### Top 10 Stores by Revenue

```sql
SELECT store_name, SUM(total_sales) as revenue
FROM uber_eats_sales
GROUP BY store_name
ORDER BY revenue DESC
LIMIT 10;
```

### Monthly Sales Summary

```sql
SELECT month_name, year, SUM(total_sales) as total
FROM uber_eats_sales
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

## 🎯 Features

✅ **Zero Data Loss** - All CSV columns preserved  
✅ **Fast Processing** - Batch inserts, no delays  
✅ **Duplicate Safe** - Run multiple times safely  
✅ **Two Data Types** - Handles offers + sales  
✅ **Smart Date Parsing** - Multiple formats supported  
✅ **Progress Tracking** - Real-time feedback  

## 🔄 Re-running the Script

### Normal Mode (Recommended)
Skips existing records - safe to run anytime:

```bash
python data_processing/scripts/process_uber_eats_promos.py
```

### Clear Mode (Fresh Start)
Deletes all existing data first (faster):

```bash
python data_processing/scripts/process_uber_eats_promos.py --clear
```

⚠️ Clear mode requires confirmation!

## 📁 Files Location

```
data_processing/
├── scripts/
│   └── process_uber_eats_promos.py    ← Run this
├── sql/
│   └── setup_uber_eats_promos.sql     ← Run this first
└── docs/
    ├── UBER_EATS_QUICKSTART.md        ← You are here
    └── UBER_EATS_SETUP_GUIDE.md       ← Full documentation

NBX/
└── Uber Eats Promos/
    ├── UberEats Offers - 12 Months.csv
    └── UberEats Sales - Export.csv
```

## ❓ Troubleshooting

### "Missing environment variables"
- Check `.env` file exists in project root
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set

### "Table does not exist"
- Run the SQL setup file first (Step 1)

### "Data folder not found"
- Ensure `NBX/Uber Eats Promos/` folder exists
- Check CSV files are in the folder

## 📚 More Information

For detailed documentation, see:
- **Full Setup Guide**: `data_processing/docs/UBER_EATS_SETUP_GUIDE.md`
- **Implementation Details**: `data_processing/docs/UBER_EATS_IMPLEMENTATION_SUMMARY.md`

## ✅ Expected Output

When successful, you'll see:

```
======================================================================
PROCESSING COMPLETE
======================================================================
Total records processed: 121,087
Successfully stored: 121,087
Failed: 0
Skipped (already exist): 0
Time elapsed: 120.45 seconds
Speed: 1005.2 records/second

✨ ALL PROPERTIES PRESERVED:
  ✓ All CSV columns stored as individual database columns
  ✓ No JSONB - direct column access
  ✓ No embeddings - simple and fast
  ✓ Batch processing for maximum speed
  ✓ Safe to re-run - skips existing records
```

## 🎉 Done!

Your Uber Eats data is now in Supabase and ready for analysis!

**Next steps**:
1. Query your data in Supabase
2. Build dashboards
3. Run analytics
4. Re-run script when you have new data

---

Need help? Check the full documentation in `UBER_EATS_SETUP_GUIDE.md`

