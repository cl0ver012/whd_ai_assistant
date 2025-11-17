-- TikTok Ads SQL setup with individual columns (no JSONB)
-- Better performance and clearer schema
-- Run this in your Supabase SQL Editor

-- ============================================================================
-- TABLE 1: TikTok Ads Performance Data (Structured)
-- ============================================================================

CREATE TABLE IF NOT EXISTS tiktok_ads_performance (
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
    ad_group_name TEXT,
    ad_name TEXT,
    website_url TEXT,
    currency_code TEXT DEFAULT 'AUD',
    
    -- Performance Metrics (Original CSV columns)
    cost NUMERIC(10, 2) DEFAULT 0,
    cpc NUMERIC(10, 2) DEFAULT 0,
    cpm NUMERIC(10, 2) DEFAULT 0,
    impressions INTEGER DEFAULT 0,
    clicks INTEGER DEFAULT 0,
    ctr NUMERIC(10, 4) DEFAULT 0,
    reach INTEGER DEFAULT 0,
    cost_per_1000_reached NUMERIC(10, 2) DEFAULT 0,
    frequency NUMERIC(10, 4) DEFAULT 0,
    
    -- Video Metrics
    video_views INTEGER DEFAULT 0,
    video_views_2s INTEGER DEFAULT 0,
    video_views_6s INTEGER DEFAULT 0,
    video_views_100 INTEGER DEFAULT 0,
    video_views_75 INTEGER DEFAULT 0,
    video_views_50 INTEGER DEFAULT 0,
    video_views_25 INTEGER DEFAULT 0,
    avg_play_time_per_view NUMERIC(10, 2) DEFAULT 0,
    avg_play_time_per_user NUMERIC(10, 2) DEFAULT 0,
    
    -- Computed Fields
    has_clicks BOOLEAN DEFAULT FALSE,
    has_video_views BOOLEAN DEFAULT FALSE,
    completion_rate NUMERIC(10, 2) DEFAULT 0,
    
    -- Optional: Text content for search
    content TEXT
);

-- ============================================================================
-- TABLE 2: TikTok Ads Documents (Simple/Zero Loss Version)
-- ============================================================================

CREATE TABLE IF NOT EXISTS tiktok_ads_documents (
    id BIGSERIAL PRIMARY KEY,
    
    -- Content and metadata
    content TEXT NOT NULL,
    metadata JSONB,
    raw_data JSONB,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================================================
-- INDEXES for Performance Table
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_tiktok_performance_day ON tiktok_ads_performance(day);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_campaign ON tiktok_ads_performance(campaign_name);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_ad_group ON tiktok_ads_performance(ad_group_name);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_ad_name ON tiktok_ads_performance(ad_name);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_period ON tiktok_ads_performance(period);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_year_month ON tiktok_ads_performance(year, month);
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_has_clicks ON tiktok_ads_performance(has_clicks) WHERE has_clicks = TRUE;
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_has_video_views ON tiktok_ads_performance(has_video_views) WHERE has_video_views = TRUE;
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_created_at ON tiktok_ads_performance(created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_tiktok_performance_content_search ON tiktok_ads_performance USING GIN (to_tsvector('english', content));

-- ============================================================================
-- INDEXES for Documents Table
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_tiktok_documents_metadata ON tiktok_ads_documents USING GIN (metadata);
CREATE INDEX IF NOT EXISTS idx_tiktok_documents_created_at ON tiktok_ads_documents(created_at);

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_tiktok_documents_content_search ON tiktok_ads_documents USING GIN (to_tsvector('english', content));

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE tiktok_ads_performance IS 'TikTok Ads performance data with structured columns';
COMMENT ON TABLE tiktok_ads_documents IS 'TikTok Ads documents with JSONB storage for flexibility';

COMMENT ON COLUMN tiktok_ads_performance.day IS 'Date of the ad performance';
COMMENT ON COLUMN tiktok_ads_performance.campaign_name IS 'Campaign name';
COMMENT ON COLUMN tiktok_ads_performance.cost IS 'Daily advertising cost';
COMMENT ON COLUMN tiktok_ads_performance.impressions IS 'Number of impressions';
COMMENT ON COLUMN tiktok_ads_performance.clicks IS 'Number of clicks';
COMMENT ON COLUMN tiktok_ads_performance.ctr IS 'Click-through rate (percentage)';
COMMENT ON COLUMN tiktok_ads_performance.video_views IS 'Total video views';
COMMENT ON COLUMN tiktok_ads_performance.completion_rate IS 'Video completion rate (percentage)';

COMMENT ON COLUMN tiktok_ads_documents.content IS 'Human-readable text content';
COMMENT ON COLUMN tiktok_ads_documents.metadata IS 'Processed metadata in JSONB format';
COMMENT ON COLUMN tiktok_ads_documents.raw_data IS 'Original CSV data preserved';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Tables created successfully!' as status,
    (SELECT COUNT(*) FROM tiktok_ads_performance) as performance_rows,
    (SELECT COUNT(*) FROM tiktok_ads_documents) as document_rows;

