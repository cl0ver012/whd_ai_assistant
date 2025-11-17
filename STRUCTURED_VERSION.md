# Structured Version - Individual Columns

Better performance with structured columns instead of JSONB!

## 🎯 What's Different

### ❌ Old Version (JSONB)
```sql
-- Hard to query
SELECT metadata->>'campaign', metadata->>'cost' FROM google_ads_documents;
```

### ✅ New Version (Structured)
```sql
-- Clean and fast
SELECT campaign, cost FROM google_ads_performance;
```

## 📊 Database Structure

### Table 1: google_ads_performance

**All 13 original CSV properties as individual columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Auto-increment ID |
| `day` | DATE | Date of the record |
| `campaign` | TEXT | Campaign name |
| `campaign_type` | TEXT | Campaign type |
| `ad_group` | TEXT | Ad group name |
| `landing_page` | TEXT | Landing page URL |
| `currency_code` | TEXT | Currency (AUD, USD, etc.) |
| `cost` | NUMERIC | Advertising cost |
| `impressions` | INTEGER | Number of impressions |
| `clicks` | INTEGER | Number of clicks |
| `ctr` | NUMERIC | Click-through rate |
| `avg_cpc` | NUMERIC | Average cost per click |
| `conversions` | NUMERIC | Number of conversions |
| `conversion_rate` | NUMERIC | Conversion rate |
| `has_conversions` | BOOLEAN | Quick filter |
| `has_clicks` | BOOLEAN | Quick filter |
| `cost_per_conversion` | NUMERIC | Computed metric |
| `file_name` | TEXT | Source file |
| `period` | TEXT | YYYY_MM format |
| `year` | TEXT | Year |
| `month` | TEXT | Month |
| `content` | TEXT | Full text for search |
| `created_at` | TIMESTAMP | When inserted |

### Table 2: google_ads_actions

**All 5 original properties as individual columns:**

| Column | Type | Description |
|--------|------|-------------|
| `id` | BIGSERIAL | Auto-increment ID |
| `day` | DATE | Date of conversion |
| `campaign` | TEXT | Campaign name |
| `ad_group` | TEXT | Ad group name |
| `conversion_action` | TEXT | Type of conversion |
| `conversions` | NUMERIC | Number of conversions |
| `file_name` | TEXT | Source file |
| `period` | TEXT | YYYY_MM format |
| `year` | TEXT | Year |
| `month` | TEXT | Month |
| `content` | TEXT | Full text for search |
| `created_at` | TIMESTAMP | When inserted |

## 🚀 Setup

### Step 1: Run New SQL
```bash
# In Supabase SQL Editor, run:
setup_supabase_structured.sql
```

This creates **2 tables**:
- `google_ads_performance`
- `google_ads_actions`

### Step 2: Test
```bash
python test_setup_structured.py
```

### Step 3: Process Data
```bash
python process_google_ads_structured.py
```

## 📈 Benefits

### ✅ Better Performance
- Indexed columns = faster queries
- No JSONB parsing overhead
- Direct column access

### ✅ Clearer Schema
- See all columns in table viewer
- Understand data structure at a glance
- Type safety enforced by database

### ✅ Easier Queries
```sql
-- Old way (JSONB)
WHERE (metadata->>'cost')::float > 100

-- New way (Structured)
WHERE cost > 100
```

### ✅ Better Joins
```sql
-- Join tables easily
SELECT 
    p.campaign,
    p.cost,
    a.conversions
FROM google_ads_performance p
LEFT JOIN google_ads_actions a 
    ON p.campaign = a.campaign 
    AND p.day = a.day;
```

## 🔍 Example Queries

### Total cost by campaign
```sql
SELECT 
    campaign,
    SUM(cost) as total_cost,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions
FROM google_ads_performance
GROUP BY campaign
ORDER BY total_cost DESC;
```

### Daily performance
```sql
SELECT 
    day,
    campaign,
    cost,
    clicks,
    conversions
FROM google_ads_performance
WHERE day >= '2024-11-01'
ORDER BY day DESC;
```

### Filter by campaign type
```sql
SELECT *
FROM google_ads_performance
WHERE campaign_type = 'Display'
  AND conversions > 0;
```

### High performing ads
```sql
SELECT 
    campaign,
    ad_group,
    ctr,
    conversion_rate,
    cost_per_conversion
FROM google_ads_performance
WHERE ctr > 2.0
  AND has_conversions = TRUE
ORDER BY conversion_rate DESC;
```

### Monthly summary
```sql
SELECT 
    year,
    month,
    COUNT(*) as records,
    SUM(cost) as total_cost,
    SUM(clicks) as total_clicks,
    SUM(conversions) as total_conversions
FROM google_ads_performance
GROUP BY year, month
ORDER BY year DESC, month DESC;
```

### Conversion details
```sql
SELECT 
    day,
    campaign,
    ad_group,
    conversion_action,
    conversions
FROM google_ads_actions
WHERE conversions > 0
ORDER BY conversions DESC;
```

## 📊 Data Integrity

### All Original Properties Preserved
- ✅ Every CSV column has its own database column
- ✅ Original data types enforced
- ✅ NULL handling for missing values
- ✅ Computed fields added automatically

### Indexes Created
- Fast filtering by day, campaign, ad_group
- Quick lookups by period (year/month)
- Efficient full-text search on content
- Optimized for common queries

## 🔄 Comparison

| Feature | JSONB Version | Structured Version |
|---------|---------------|-------------------|
| **Query Speed** | Slower | ✅ Faster |
| **Schema Clarity** | Hidden in JSON | ✅ Visible columns |
| **Type Safety** | Runtime check | ✅ Database enforced |
| **Indexing** | Limited | ✅ Full indexing |
| **Join Performance** | Slower | ✅ Faster |
| **SQL Complexity** | More complex | ✅ Simpler |
| **Storage** | Similar | Similar |

## 📁 Files

```
Structured Version:
├── setup_supabase_structured.sql      # Database setup
├── process_google_ads_structured.py   # Data processor
├── test_setup_structured.py           # Test script
└── STRUCTURED_VERSION.md              # This file
```

## ✅ Checklist

- [ ] Run `setup_supabase_structured.sql` in Supabase
- [ ] Verify tables created (2 tables)
- [ ] Run `python test_setup_structured.py`
- [ ] See both tables accessible
- [ ] Run `python process_google_ads_structured.py`
- [ ] Query your data with standard SQL!

## 🎉 Result

Clean, fast, structured data - no JSONB complexity! 🚀

