-- Structured SQL setup with individual columns (no JSONB)
-- Better performance and clearer schema
-- Run this in your Supabase SQL Editor

-- ============================================================================
-- TABLE 1: Google Ads Performance Data
-- ============================================================================

CREATE TABLE IF NOT EXISTS google_ads_performance (
    id BIGSERIAL PRIMARY KEY,
    
    -- Date and Time
    day DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    report_title TEXT,
    report_date_range TEXT,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    
    -- Campaign Details
    campaign TEXT NOT NULL,
    campaign_type TEXT,
    ad_group TEXT,
    landing_page TEXT,
    currency_code TEXT DEFAULT 'AUD',
    
    -- Performance Metrics (Original CSV columns)
    cost NUMERIC(10, 2) DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    ctr NUMERIC(10, 4) DEFAULT 0,
    avg_cpc NUMERIC(10, 2) DEFAULT 0,
    conversions NUMERIC(10, 2) DEFAULT 0,
    conversion_rate NUMERIC(10, 4) DEFAULT 0,
    
    -- Computed Fields
    has_conversions BOOLEAN DEFAULT FALSE,
    has_clicks BOOLEAN DEFAULT FALSE,
    cost_per_conversion NUMERIC(10, 2),
    
    -- Optional: Text content for search
    content TEXT,
    
    -- Optional: Embedding for AI (can add later)
    embedding TEXT
);

-- ============================================================================
-- TABLE 2: Google Ads Conversion Actions
-- ============================================================================

CREATE TABLE IF NOT EXISTS google_ads_actions (
    id BIGSERIAL PRIMARY KEY,
    
    -- Date and Time
    day DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    report_title TEXT,
    report_date_range TEXT,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    
    -- Campaign Details
    campaign TEXT NOT NULL,
    ad_group TEXT,
    conversion_action TEXT NOT NULL,
    
    -- Metrics
    conversions NUMERIC(10, 2) DEFAULT 0,
    
    -- Optional: Text content for search
    content TEXT,
    
    -- Optional: Embedding for AI (can add later)
    embedding TEXT
);

-- ============================================================================
-- INDEXES for Performance Table
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_performance_day ON google_ads_performance(day);
CREATE INDEX IF NOT EXISTS idx_performance_campaign ON google_ads_performance(campaign);
CREATE INDEX IF NOT EXISTS idx_performance_campaign_type ON google_ads_performance(campaign_type);
CREATE INDEX IF NOT EXISTS idx_performance_ad_group ON google_ads_performance(ad_group);
CREATE INDEX IF NOT EXISTS idx_performance_period ON google_ads_performance(period);
CREATE INDEX IF NOT EXISTS idx_performance_year_month ON google_ads_performance(year, month);
CREATE INDEX IF NOT EXISTS idx_performance_has_conversions ON google_ads_performance(has_conversions) WHERE has_conversions = TRUE;
CREATE INDEX IF NOT EXISTS idx_performance_created_at ON google_ads_performance(created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_performance_content_search ON google_ads_performance USING GIN (to_tsvector('english', content));

-- ============================================================================
-- INDEXES for Actions Table
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_actions_day ON google_ads_actions(day);
CREATE INDEX IF NOT EXISTS idx_actions_campaign ON google_ads_actions(campaign);
CREATE INDEX IF NOT EXISTS idx_actions_ad_group ON google_ads_actions(ad_group);
CREATE INDEX IF NOT EXISTS idx_actions_conversion_action ON google_ads_actions(conversion_action);
CREATE INDEX IF NOT EXISTS idx_actions_period ON google_ads_actions(period);
CREATE INDEX IF NOT EXISTS idx_actions_year_month ON google_ads_actions(year, month);
CREATE INDEX IF NOT EXISTS idx_actions_created_at ON google_ads_actions(created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_actions_content_search ON google_ads_actions USING GIN (to_tsvector('english', content));

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE google_ads_performance IS 'Google Ads performance data with structured columns';
COMMENT ON TABLE google_ads_actions IS 'Google Ads conversion actions with structured columns';

COMMENT ON COLUMN google_ads_performance.day IS 'Date of the ad performance';
COMMENT ON COLUMN google_ads_performance.campaign IS 'Campaign name';
COMMENT ON COLUMN google_ads_performance.cost IS 'Daily advertising cost';
COMMENT ON COLUMN google_ads_performance.impressions IS 'Number of impressions';
COMMENT ON COLUMN google_ads_performance.clicks IS 'Number of clicks';
COMMENT ON COLUMN google_ads_performance.ctr IS 'Click-through rate (percentage)';
COMMENT ON COLUMN google_ads_performance.conversions IS 'Number of conversions';

COMMENT ON COLUMN google_ads_actions.conversion_action IS 'Type of conversion action';
COMMENT ON COLUMN google_ads_actions.conversions IS 'Number of conversions';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Tables created successfully!' as status,
    (SELECT COUNT(*) FROM google_ads_performance) as performance_rows,
    (SELECT COUNT(*) FROM google_ads_actions) as action_rows;

