-- Uber Eats Promos Data Tables Setup
-- Creates tables for Uber Eats offers and sales data
-- All original CSV columns preserved as individual database columns
-- No JSONB, no embeddings - simple and fast

-- ============================================================================
-- Table 1: Uber Eats Offers
-- Stores promotional offers data
-- ============================================================================

CREATE TABLE IF NOT EXISTS uber_eats_offers (
    -- Primary key
    id BIGSERIAL PRIMARY KEY,
    
    -- Source information
    file_name TEXT NOT NULL,
    
    -- Offer details (all original CSV columns)
    offer TEXT,
    promo_start_date TEXT,
    promo_end_date TEXT,
    customer_targeting TEXT,
    items TEXT,
    
    -- Computed fields
    has_discount BOOLEAN DEFAULT false,
    has_fixed_price BOOLEAN DEFAULT false,
    
    -- Text content for search/display
    content TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_uber_eats_offers_file_name ON uber_eats_offers(file_name);
CREATE INDEX IF NOT EXISTS idx_uber_eats_offers_promo_start_date ON uber_eats_offers(promo_start_date);
CREATE INDEX IF NOT EXISTS idx_uber_eats_offers_promo_end_date ON uber_eats_offers(promo_end_date);
CREATE INDEX IF NOT EXISTS idx_uber_eats_offers_customer_targeting ON uber_eats_offers(customer_targeting);
CREATE INDEX IF NOT EXISTS idx_uber_eats_offers_created_at ON uber_eats_offers(created_at);

-- Enable Row Level Security (optional)
ALTER TABLE uber_eats_offers ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust as needed)
CREATE POLICY "Allow all operations on uber_eats_offers" ON uber_eats_offers
    FOR ALL USING (true) WITH CHECK (true);

-- Add comments
COMMENT ON TABLE uber_eats_offers IS 'Uber Eats promotional offers data - all CSV columns preserved';
COMMENT ON COLUMN uber_eats_offers.offer IS 'Offer description';
COMMENT ON COLUMN uber_eats_offers.promo_start_date IS 'Promotion start date';
COMMENT ON COLUMN uber_eats_offers.promo_end_date IS 'Promotion end date';
COMMENT ON COLUMN uber_eats_offers.customer_targeting IS 'Customer targeting criteria';
COMMENT ON COLUMN uber_eats_offers.items IS 'Items included in the promotion';
COMMENT ON COLUMN uber_eats_offers.content IS 'Human-readable text content for search and display';

-- ============================================================================
-- Table 2: Uber Eats Sales
-- Stores sales data
-- ============================================================================

CREATE TABLE IF NOT EXISTS uber_eats_sales (
    -- Primary key
    id BIGSERIAL PRIMARY KEY,
    
    -- Source information
    file_name TEXT NOT NULL,
    
    -- Sales details (all original CSV columns)
    date TEXT,
    store_name TEXT,
    channel_type TEXT,
    total_sales NUMERIC(10, 2),
    
    -- Parsed fields
    parsed_date DATE,
    year TEXT,
    month TEXT,
    month_name TEXT,
    period TEXT,
    
    -- Computed fields
    has_sales BOOLEAN DEFAULT false,
    
    -- Text content for search/display
    content TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Add indexes for common queries
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_file_name ON uber_eats_sales(file_name);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_date ON uber_eats_sales(date);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_parsed_date ON uber_eats_sales(parsed_date);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_store_name ON uber_eats_sales(store_name);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_channel_type ON uber_eats_sales(channel_type);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_year ON uber_eats_sales(year);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_month ON uber_eats_sales(month);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_period ON uber_eats_sales(period);
CREATE INDEX IF NOT EXISTS idx_uber_eats_sales_created_at ON uber_eats_sales(created_at);

-- Enable Row Level Security (optional)
ALTER TABLE uber_eats_sales ENABLE ROW LEVEL SECURITY;

-- Create policy to allow all operations (adjust as needed)
CREATE POLICY "Allow all operations on uber_eats_sales" ON uber_eats_sales
    FOR ALL USING (true) WITH CHECK (true);

-- Add comments
COMMENT ON TABLE uber_eats_sales IS 'Uber Eats sales data - all CSV columns preserved';
COMMENT ON COLUMN uber_eats_sales.date IS 'Sales date from CSV';
COMMENT ON COLUMN uber_eats_sales.store_name IS 'Store name';
COMMENT ON COLUMN uber_eats_sales.channel_type IS 'Sales channel type (e.g., Uber)';
COMMENT ON COLUMN uber_eats_sales.total_sales IS 'Total sales amount';
COMMENT ON COLUMN uber_eats_sales.parsed_date IS 'Parsed date for easier querying';
COMMENT ON COLUMN uber_eats_sales.content IS 'Human-readable text content for search and display';

-- ============================================================================
-- Summary
-- ============================================================================

SELECT 'Uber Eats Promos tables created successfully!' as status;
SELECT 'Table 1: uber_eats_offers - Promotional offers data' as info;
SELECT 'Table 2: uber_eats_sales - Sales data' as info;

