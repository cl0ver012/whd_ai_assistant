-- Meta Ads SQL Setup - All Properties as Individual Columns
-- No JSONB - Better performance and clearer schema
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS meta_ads_performance (
    id BIGSERIAL PRIMARY KEY,
    
    -- Date and Time
    day DATE NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    
    -- Campaign Details
    campaign_name TEXT NOT NULL,
    ad_set_name TEXT,
    ad_name TEXT,
    objective TEXT,
    result_type TEXT,
    website_url TEXT,
    
    -- Campaign Timeline
    starts TEXT,
    ends TEXT,
    reporting_starts TEXT,
    reporting_ends TEXT,
    
    -- Performance Metrics (All Original CSV Columns)
    reach INTEGER DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    frequency NUMERIC(10, 6) DEFAULT 0,
    results NUMERIC(10, 2) DEFAULT 0,
    amount_spent NUMERIC(10, 2) DEFAULT 0,
    cost_per_result NUMERIC(10, 2) DEFAULT 0,
    link_clicks INTEGER DEFAULT 0,
    cpc NUMERIC(10, 2) DEFAULT 0,
    cpm NUMERIC(10, 2) DEFAULT 0,
    
    -- Video Metrics (All Original CSV Columns)
    video_avg_play_time NUMERIC(10, 2) DEFAULT 0,
    cost_per_thruplay NUMERIC(10, 2) DEFAULT 0,
    thru_plays INTEGER DEFAULT 0,
    video_plays_25 INTEGER DEFAULT 0,
    video_plays_50 INTEGER DEFAULT 0,
    video_plays_75 INTEGER DEFAULT 0,
    video_plays_95 INTEGER DEFAULT 0,
    video_plays_100 INTEGER DEFAULT 0,
    
    -- Computed Fields
    has_results BOOLEAN DEFAULT FALSE,
    has_link_clicks BOOLEAN DEFAULT FALSE,
    has_video_content BOOLEAN DEFAULT FALSE,
    
    -- Optional: Text content for search
    content TEXT,
    
    -- Optional: Embedding for AI (can add later)
    embedding TEXT
);

-- ============================================================================
-- INDEXES for Fast Querying
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_meta_day ON meta_ads_performance(day);
CREATE INDEX IF NOT EXISTS idx_meta_campaign_name ON meta_ads_performance(campaign_name);
CREATE INDEX IF NOT EXISTS idx_meta_ad_set_name ON meta_ads_performance(ad_set_name);
CREATE INDEX IF NOT EXISTS idx_meta_ad_name ON meta_ads_performance(ad_name);
CREATE INDEX IF NOT EXISTS idx_meta_objective ON meta_ads_performance(objective);
CREATE INDEX IF NOT EXISTS idx_meta_period ON meta_ads_performance(period);
CREATE INDEX IF NOT EXISTS idx_meta_year_month ON meta_ads_performance(year, month);
CREATE INDEX IF NOT EXISTS idx_meta_has_results ON meta_ads_performance(has_results) WHERE has_results = TRUE;
CREATE INDEX IF NOT EXISTS idx_meta_has_link_clicks ON meta_ads_performance(has_link_clicks) WHERE has_link_clicks = TRUE;
CREATE INDEX IF NOT EXISTS idx_meta_has_video_content ON meta_ads_performance(has_video_content) WHERE has_video_content = TRUE;
CREATE INDEX IF NOT EXISTS idx_meta_created_at ON meta_ads_performance(created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_meta_content_search ON meta_ads_performance USING GIN (to_tsvector('english', content));

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_meta_amount_spent ON meta_ads_performance(amount_spent);
CREATE INDEX IF NOT EXISTS idx_meta_impressions ON meta_ads_performance(impressions);
CREATE INDEX IF NOT EXISTS idx_meta_link_clicks ON meta_ads_performance(link_clicks);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE meta_ads_performance IS 'Meta Ads performance data - all properties as individual columns';

COMMENT ON COLUMN meta_ads_performance.day IS 'Date of the ad performance';
COMMENT ON COLUMN meta_ads_performance.campaign_name IS 'Campaign name';
COMMENT ON COLUMN meta_ads_performance.ad_set_name IS 'Ad set name';
COMMENT ON COLUMN meta_ads_performance.ad_name IS 'Individual ad name';
COMMENT ON COLUMN meta_ads_performance.objective IS 'Campaign objective (Traffic, Engagement, Leads, etc.)';
COMMENT ON COLUMN meta_ads_performance.result_type IS 'Type of result measured';
COMMENT ON COLUMN meta_ads_performance.reach IS 'Number of unique users reached';
COMMENT ON COLUMN meta_ads_performance.impressions IS 'Number of impressions';
COMMENT ON COLUMN meta_ads_performance.frequency IS 'Average frequency per user';
COMMENT ON COLUMN meta_ads_performance.results IS 'Number of results based on objective';
COMMENT ON COLUMN meta_ads_performance.amount_spent IS 'Amount spent in AUD';
COMMENT ON COLUMN meta_ads_performance.cost_per_result IS 'Cost per result in AUD';
COMMENT ON COLUMN meta_ads_performance.link_clicks IS 'Number of link clicks';
COMMENT ON COLUMN meta_ads_performance.cpc IS 'Cost per click (link click) in AUD';
COMMENT ON COLUMN meta_ads_performance.cpm IS 'Cost per 1,000 impressions in AUD';
COMMENT ON COLUMN meta_ads_performance.video_avg_play_time IS 'Average video play time in seconds';
COMMENT ON COLUMN meta_ads_performance.thru_plays IS 'Number of ThruPlays (video watched to completion or 15s)';
COMMENT ON COLUMN meta_ads_performance.video_plays_25 IS 'Video plays at 25%';
COMMENT ON COLUMN meta_ads_performance.video_plays_50 IS 'Video plays at 50%';
COMMENT ON COLUMN meta_ads_performance.video_plays_75 IS 'Video plays at 75%';
COMMENT ON COLUMN meta_ads_performance.video_plays_95 IS 'Video plays at 95%';
COMMENT ON COLUMN meta_ads_performance.video_plays_100 IS 'Video plays at 100%';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM meta_ads_performance;
