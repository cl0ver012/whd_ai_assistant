-- Power BI SQL Setup - All Properties as Individual Columns
-- No JSONB, No Embeddings - Simple and fast
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS powerbi_sales (
    id BIGSERIAL PRIMARY KEY,
    
    -- Timestamp
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
    
    -- Optional: Text content for search/display
    content TEXT
);

-- ============================================================================
-- INDEXES for Fast Querying
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_powerbi_store_name ON powerbi_sales(store_name);
CREATE INDEX IF NOT EXISTS idx_powerbi_period ON powerbi_sales(period);
CREATE INDEX IF NOT EXISTS idx_powerbi_year ON powerbi_sales(year);
CREATE INDEX IF NOT EXISTS idx_powerbi_month ON powerbi_sales(month);
CREATE INDEX IF NOT EXISTS idx_powerbi_month_name ON powerbi_sales(month_name);
CREATE INDEX IF NOT EXISTS idx_powerbi_year_month ON powerbi_sales(year, month);
CREATE INDEX IF NOT EXISTS idx_powerbi_created_at ON powerbi_sales(created_at);

-- Index for sales queries
CREATE INDEX IF NOT EXISTS idx_powerbi_total_sales ON powerbi_sales(total_sales);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_powerbi_content_search ON powerbi_sales USING GIN (to_tsvector('english', content));

-- Combined index for common queries (store + period)
CREATE INDEX IF NOT EXISTS idx_powerbi_store_period ON powerbi_sales(store_name, period);
CREATE INDEX IF NOT EXISTS idx_powerbi_store_year_month ON powerbi_sales(store_name, year, month);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE powerbi_sales IS 'Power BI sales data - all properties as individual columns';

COMMENT ON COLUMN powerbi_sales.file_name IS 'Source CSV filename';
COMMENT ON COLUMN powerbi_sales.period IS 'Period in format YYYY_MM';
COMMENT ON COLUMN powerbi_sales.year IS 'Year (e.g., 2025)';
COMMENT ON COLUMN powerbi_sales.month IS 'Month number (01-12)';
COMMENT ON COLUMN powerbi_sales.month_name IS 'Month name (e.g., October)';
COMMENT ON COLUMN powerbi_sales.store_name IS 'Store name/location';
COMMENT ON COLUMN powerbi_sales.total_sales IS 'Total sales in AUD';
COMMENT ON COLUMN powerbi_sales.content IS 'Human-readable text for search/display';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM powerbi_sales;

