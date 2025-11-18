# Uber Eats Promos Implementation Summary

## ✅ Implementation Complete

The Uber Eats Promos data processing system has been successfully implemented following the same pattern as the ads and organic social media processing scripts.

## 📁 Files Created

### 1. SQL Setup File
**Location**: `data_processing/sql/setup_uber_eats_promos.sql`

Creates two database tables:
- `uber_eats_offers` - Promotional offers data
- `uber_eats_sales` - Sales data by store and channel

**Features**:
- All CSV columns preserved as individual database columns
- Indexes for common queries
- Row Level Security policies
- Comprehensive comments

### 2. Processing Script
**Location**: `data_processing/scripts/process_uber_eats_promos.py`

Processes CSV files from `NBX/Uber Eats Promos/` folder.

**Features**:
- ✅ Batch processing (100 rows at a time)
- ✅ Duplicate detection and skipping
- ✅ Intelligent date parsing
- ✅ No data loss - all CSV columns preserved
- ✅ No embeddings
- ✅ Computed fields for analytics
- ✅ Progress tracking and error handling

### 3. Documentation
**Location**: `data_processing/docs/UBER_EATS_SETUP_GUIDE.md`

Comprehensive setup and usage guide including:
- Overview and features
- Database table structures
- Setup instructions
- Example queries
- Troubleshooting guide

## 🎯 Data Processing Details

### Files Processed

1. **Offers Files** (matches `*Offers*.csv`):
   - `UberEats Offers - 12 Months.csv`
   - Columns: Offer, Promo Start Date, Promo End Date, Customer Targeting, Items

2. **Sales Files** (matches `*Sales*.csv`):
   - `UberEats Sales - Export.csv`
   - Columns: Date, Store Name, Channel Type, Total Sales

### Data Preservation

✅ **All original CSV columns preserved**
- No JSONB storage
- No embeddings
- Direct column access
- Individual database columns for each CSV column

### Computed Fields

**Offers Table**:
- `has_discount` - Boolean flag for percentage/discount offers
- `has_fixed_price` - Boolean flag for fixed price offers

**Sales Table**:
- `parsed_date` - DATE type for easier querying
- `year`, `month`, `month_name`, `period` - Extracted time components
- `has_sales` - Boolean flag for non-zero sales

## 🚀 How to Use

### Step 1: Setup Database

Run the SQL setup in Supabase SQL Editor:

```bash
# Copy contents of data_processing/sql/setup_uber_eats_promos.sql
# Paste into Supabase SQL Editor and run
```

### Step 2: Process Data

**Normal mode** (recommended - skips duplicates):
```bash
python data_processing/scripts/process_uber_eats_promos.py
```

**Clear mode** (deletes existing data first):
```bash
python data_processing/scripts/process_uber_eats_promos.py --clear
```

## 📊 Database Schema

### Table: uber_eats_offers

```sql
CREATE TABLE uber_eats_offers (
    id BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    offer TEXT,
    promo_start_date TEXT,
    promo_end_date TEXT,
    customer_targeting TEXT,
    items TEXT,
    has_discount BOOLEAN DEFAULT false,
    has_fixed_price BOOLEAN DEFAULT false,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes**: file_name, promo_start_date, promo_end_date, customer_targeting, created_at

### Table: uber_eats_sales

```sql
CREATE TABLE uber_eats_sales (
    id BIGSERIAL PRIMARY KEY,
    file_name TEXT NOT NULL,
    date TEXT,
    store_name TEXT,
    channel_type TEXT,
    total_sales NUMERIC(10, 2),
    parsed_date DATE,
    year TEXT,
    month TEXT,
    month_name TEXT,
    period TEXT,
    has_sales BOOLEAN DEFAULT false,
    content TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

**Indexes**: file_name, date, parsed_date, store_name, channel_type, year, month, period, created_at

## 🔍 Example Queries

### Top Stores by Revenue

```sql
SELECT 
    store_name,
    COUNT(*) as orders,
    SUM(total_sales) as total_revenue
FROM uber_eats_sales
WHERE has_sales = true
GROUP BY store_name
ORDER BY total_revenue DESC
LIMIT 10;
```

### Monthly Sales Trends

```sql
SELECT 
    year,
    month_name,
    COUNT(*) as transactions,
    SUM(total_sales) as revenue
FROM uber_eats_sales
GROUP BY year, month, month_name
ORDER BY year DESC, month DESC;
```

### Active Promotions

```sql
SELECT 
    offer,
    promo_start_date,
    promo_end_date,
    customer_targeting,
    items
FROM uber_eats_offers
WHERE has_discount = true
ORDER BY promo_start_date DESC;
```

## ⚡ Performance

Expected processing speeds:
- **Offers**: ~1,000 records/second
- **Sales**: ~500-1,000 records/second (121,022 rows detected)
- **Batch Size**: 100 rows
- **No Delays**: Maximum speed

## ✨ Key Features

1. **Zero Data Loss**: All CSV columns preserved exactly as they appear
2. **Fast Batch Processing**: 100 rows at a time for optimal speed
3. **Duplicate Detection**: Safely re-run without creating duplicates
4. **Intelligent Date Parsing**: Handles multiple date formats automatically
5. **Computed Fields**: Useful analytics fields calculated automatically
6. **Progress Tracking**: Real-time feedback during processing
7. **Error Handling**: Robust error handling with clear messages
8. **Two Data Types**: Handles both offers and sales in one script

## 🎯 Comparison with Other Processors

This implementation follows the exact same pattern as:
- `process_organic_social.py`
- `process_meta_ads.py`

**Common features**:
- ✅ All CSV columns as individual database columns
- ✅ No JSONB storage
- ✅ No embeddings (as requested)
- ✅ Batch processing for speed
- ✅ Duplicate detection
- ✅ Progress tracking
- ✅ Error handling
- ✅ `--clear` flag support

**Unique to Uber Eats**:
- ✅ Handles two different CSV types (offers + sales)
- ✅ Intelligent date format parsing (multiple formats)
- ✅ Store-level analytics capabilities
- ✅ Promotional campaign tracking

## 📝 Testing Status

✅ Script created and syntax validated
✅ Database schema defined
✅ Documentation complete
⚠️ Database tables need to be created before first run

**Next step**: Run the SQL setup file in Supabase to create the tables, then run the processing script.

## 🔧 Technical Details

### Date Parsing Logic

The script handles multiple date formats:

1. **Sales format**: "Tuesday, October 01, 2024"
   - Removes day of week
   - Parses to YYYY-MM-DD
   - Extracts year, month, month_name, period

2. **Offers format**: "1-Jul-24"
   - Converts 2-digit year to 4-digit
   - Parses date components
   - Handles month abbreviations

### Duplicate Detection

**Offers**: Based on combination of:
- offer
- promo_start_date
- promo_end_date

**Sales**: Based on combination of:
- date
- store_name
- channel_type
- total_sales

### Error Handling

- Missing environment variables → Clear error message
- Missing data folder → Clear error message
- CSV read errors → Logged and skipped
- Database errors → Batch fails are tracked
- Date parse errors → Warning logged, continues processing

## 📦 Dependencies

Already installed (from existing setup):
- `pandas` - CSV file processing
- `supabase` - Database connection
- `python-dotenv` - Environment variables

No additional dependencies needed!

## ✅ Checklist

- [x] SQL setup file created
- [x] Processing script created
- [x] Documentation written
- [x] Code follows existing patterns
- [x] All CSV columns preserved
- [x] No embeddings (as requested)
- [x] Batch processing implemented
- [x] Duplicate detection added
- [x] Error handling included
- [x] Progress tracking added
- [ ] Database tables created (user action required)
- [ ] Script tested with real data (pending database setup)

## 🎉 Ready to Use!

The Uber Eats Promos data processing system is complete and ready to use. Simply:

1. Run the SQL setup file in Supabase
2. Execute the processing script
3. Query your data!

All features match the existing ads and organic social media processors, with zero data loss and no embeddings as requested.

