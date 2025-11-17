# Power BI Processing - Quick Start

Get your Power BI sales data into Supabase in 3 steps!

## ⚡ Quick Setup (5 minutes)

### 1. Setup Database
Run this SQL in your Supabase SQL Editor:
```sql
-- Copy contents from setup_powerbi.sql and run
```

### 2. Test Setup
```bash
python test_setup_powerbi.py
```
Should see all ✅ checkmarks.

### 3. Process Data
```bash
python process_powerbi.py
```

## 📁 File Requirements

Your CSV files should be in:
```
NBX/Power BI/
├── powerbi_LFL_Sales_2025_06.csv
├── powerbi_LFL_Sales_2025_07.csv
├── 01 25.csv
├── 02 25.csv
└── ...
```

## 📊 Data Format

CSV columns:
- `Store Name`: Store location
- `Total Sales`: Sales amount (e.g., "$66,022")
- `Year`: Year (e.g., 2025)
- `Month Name`: Month name (e.g., "October")

## ✨ Features

- ✅ No embeddings - super fast!
- ✅ Auto-handles duplicate headers
- ✅ Clean currency parsing
- ✅ All properties preserved
- ✅ Direct SQL queries

## 🔍 Example Queries

### Total by Store
```sql
SELECT store_name, SUM(total_sales) as total
FROM powerbi_sales
GROUP BY store_name
ORDER BY total DESC;
```

### Monthly Trends
```sql
SELECT year, month_name, SUM(total_sales) as total
FROM powerbi_sales
GROUP BY year, month_name
ORDER BY year DESC, month DESC;
```

### Top 10 Stores
```sql
SELECT store_name, total_sales, month_name, year
FROM powerbi_sales
WHERE year = '2025' AND month = '10'
ORDER BY total_sales DESC
LIMIT 10;
```

## 📖 Need More Help?

- **Full Guide:** [POWERBI_SETUP_GUIDE.md](POWERBI_SETUP_GUIDE.md)
- **Implementation Details:** [POWERBI_IMPLEMENTATION_SUMMARY.md](POWERBI_IMPLEMENTATION_SUMMARY.md)

## 🚀 You're Ready!

```bash
python process_powerbi.py
```

That's it! Your Power BI data will be in Supabase.

