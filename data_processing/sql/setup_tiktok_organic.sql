-- TikTok Organic Data SQL Setup - All Properties as Individual Columns
-- No JSONB, No Embeddings - Simple and fast
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS tiktok_organic (
    id BIGSERIAL PRIMARY KEY,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    month_name TEXT NOT NULL,
    
    -- Date Information
    date TEXT NOT NULL,
    day_of_month TEXT,
    
    -- Engagement Metrics (All Original CSV Columns)
    video_views INTEGER DEFAULT 0,
    profile_views INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    
    -- Computed Fields
    has_views BOOLEAN DEFAULT FALSE,
    has_engagement BOOLEAN DEFAULT FALSE,
    total_engagement INTEGER DEFAULT 0,
    
    -- Optional: Text content for search/display
    content TEXT
);

-- ============================================================================
-- INDEXES for Fast Querying
-- ============================================================================

-- Primary lookup indexes
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_period ON tiktok_organic(period);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_year ON tiktok_organic(year);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_month ON tiktok_organic(month);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_year_month ON tiktok_organic(year, month);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_date ON tiktok_organic(date);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_file_name ON tiktok_organic(file_name);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_created_at ON tiktok_organic(created_at);

-- Indexes for engagement metrics
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_video_views ON tiktok_organic(video_views);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_profile_views ON tiktok_organic(profile_views);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_likes ON tiktok_organic(likes);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_comments ON tiktok_organic(comments);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_shares ON tiktok_organic(shares);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_total_engagement ON tiktok_organic(total_engagement);

-- Indexes for computed fields
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_has_views ON tiktok_organic(has_views) WHERE has_views = TRUE;
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_has_engagement ON tiktok_organic(has_engagement) WHERE has_engagement = TRUE;

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_content_search ON tiktok_organic USING GIN (to_tsvector('english', content));

-- Combined indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_period_date ON tiktok_organic(period, date);
CREATE INDEX IF NOT EXISTS idx_tiktok_organic_file_date ON tiktok_organic(file_name, date);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE tiktok_organic IS 'TikTok Organic performance data - all properties as individual columns';

COMMENT ON COLUMN tiktok_organic.file_name IS 'Source CSV filename';
COMMENT ON COLUMN tiktok_organic.period IS 'Period extracted from filename (YYYY_MM)';
COMMENT ON COLUMN tiktok_organic.year IS 'Year (e.g., 2025)';
COMMENT ON COLUMN tiktok_organic.month IS 'Month number (01-12)';
COMMENT ON COLUMN tiktok_organic.month_name IS 'Month name (e.g., November)';
COMMENT ON COLUMN tiktok_organic.date IS 'Date from CSV (e.g., "1 April")';
COMMENT ON COLUMN tiktok_organic.day_of_month IS 'Day of month extracted from date';
COMMENT ON COLUMN tiktok_organic.video_views IS 'Number of video views';
COMMENT ON COLUMN tiktok_organic.profile_views IS 'Number of profile views';
COMMENT ON COLUMN tiktok_organic.likes IS 'Number of likes';
COMMENT ON COLUMN tiktok_organic.comments IS 'Number of comments';
COMMENT ON COLUMN tiktok_organic.shares IS 'Number of shares';
COMMENT ON COLUMN tiktok_organic.total_engagement IS 'Total engagement (likes + comments + shares)';
COMMENT ON COLUMN tiktok_organic.has_views IS 'Whether the record has any video views';
COMMENT ON COLUMN tiktok_organic.has_engagement IS 'Whether the record has any engagement';
COMMENT ON COLUMN tiktok_organic.content IS 'Human-readable text for search/display';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM tiktok_organic;

