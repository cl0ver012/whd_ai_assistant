-- Organic Social Media SQL Setup - All Properties as Individual Columns
-- No JSONB, No Embeddings - Simple and fast
-- Run this in your Supabase SQL Editor

CREATE TABLE IF NOT EXISTS organic_social_media (
    id BIGSERIAL PRIMARY KEY,
    
    -- Timestamp
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Source Information
    file_name TEXT NOT NULL,
    period TEXT NOT NULL,
    year TEXT NOT NULL,
    month TEXT NOT NULL,
    month_name TEXT NOT NULL,
    
    -- Post Identification
    post_id TEXT NOT NULL,
    account_id TEXT NOT NULL,
    account_username TEXT NOT NULL,
    account_name TEXT NOT NULL,
    
    -- Post Details
    description TEXT,
    duration_sec INTEGER DEFAULT 0,
    publish_time TEXT,
    permalink TEXT,
    post_type TEXT,
    data_comment TEXT,
    date TEXT,
    
    -- Engagement Metrics (All Original CSV Columns)
    views INTEGER DEFAULT 0,
    reach INTEGER DEFAULT 0,
    likes INTEGER DEFAULT 0,
    shares INTEGER DEFAULT 0,
    follows INTEGER DEFAULT 0,
    comments INTEGER DEFAULT 0,
    saves INTEGER DEFAULT 0,
    
    -- Computed Fields
    has_views BOOLEAN DEFAULT FALSE,
    has_engagement BOOLEAN DEFAULT FALSE,
    is_video BOOLEAN DEFAULT FALSE,
    
    -- Optional: Text content for search/display
    content TEXT
);

-- ============================================================================
-- INDEXES for Fast Querying
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_organic_post_id ON organic_social_media(post_id);
CREATE INDEX IF NOT EXISTS idx_organic_account_id ON organic_social_media(account_id);
CREATE INDEX IF NOT EXISTS idx_organic_account_username ON organic_social_media(account_username);
CREATE INDEX IF NOT EXISTS idx_organic_period ON organic_social_media(period);
CREATE INDEX IF NOT EXISTS idx_organic_year ON organic_social_media(year);
CREATE INDEX IF NOT EXISTS idx_organic_month ON organic_social_media(month);
CREATE INDEX IF NOT EXISTS idx_organic_year_month ON organic_social_media(year, month);
CREATE INDEX IF NOT EXISTS idx_organic_post_type ON organic_social_media(post_type);
CREATE INDEX IF NOT EXISTS idx_organic_created_at ON organic_social_media(created_at);

-- Indexes for engagement metrics
CREATE INDEX IF NOT EXISTS idx_organic_views ON organic_social_media(views);
CREATE INDEX IF NOT EXISTS idx_organic_reach ON organic_social_media(reach);
CREATE INDEX IF NOT EXISTS idx_organic_likes ON organic_social_media(likes);
CREATE INDEX IF NOT EXISTS idx_organic_shares ON organic_social_media(shares);
CREATE INDEX IF NOT EXISTS idx_organic_comments ON organic_social_media(comments);

-- Indexes for computed fields
CREATE INDEX IF NOT EXISTS idx_organic_has_views ON organic_social_media(has_views) WHERE has_views = TRUE;
CREATE INDEX IF NOT EXISTS idx_organic_has_engagement ON organic_social_media(has_engagement) WHERE has_engagement = TRUE;
CREATE INDEX IF NOT EXISTS idx_organic_is_video ON organic_social_media(is_video) WHERE is_video = TRUE;

-- Full-text search on content
CREATE INDEX IF NOT EXISTS idx_organic_content_search ON organic_social_media USING GIN (to_tsvector('english', content));

-- Combined indexes for common queries
CREATE INDEX IF NOT EXISTS idx_organic_account_period ON organic_social_media(account_username, period);
CREATE INDEX IF NOT EXISTS idx_organic_post_type_period ON organic_social_media(post_type, period);

-- ============================================================================
-- COMMENTS
-- ============================================================================

COMMENT ON TABLE organic_social_media IS 'Organic social media performance data - all properties as individual columns';

COMMENT ON COLUMN organic_social_media.file_name IS 'Source CSV filename';
COMMENT ON COLUMN organic_social_media.period IS 'Period extracted from filename';
COMMENT ON COLUMN organic_social_media.year IS 'Year (e.g., 2025)';
COMMENT ON COLUMN organic_social_media.month IS 'Month number (01-12)';
COMMENT ON COLUMN organic_social_media.month_name IS 'Month name (e.g., November)';
COMMENT ON COLUMN organic_social_media.post_id IS 'Unique post identifier';
COMMENT ON COLUMN organic_social_media.account_id IS 'Social media account ID';
COMMENT ON COLUMN organic_social_media.account_username IS 'Social media account username';
COMMENT ON COLUMN organic_social_media.account_name IS 'Social media account display name';
COMMENT ON COLUMN organic_social_media.description IS 'Post description/caption';
COMMENT ON COLUMN organic_social_media.duration_sec IS 'Video duration in seconds (0 for non-video posts)';
COMMENT ON COLUMN organic_social_media.publish_time IS 'Post publish timestamp';
COMMENT ON COLUMN organic_social_media.permalink IS 'Direct link to the post';
COMMENT ON COLUMN organic_social_media.post_type IS 'Type of post (IG image, IG reel, etc.)';
COMMENT ON COLUMN organic_social_media.views IS 'Number of views';
COMMENT ON COLUMN organic_social_media.reach IS 'Number of unique users reached';
COMMENT ON COLUMN organic_social_media.likes IS 'Number of likes';
COMMENT ON COLUMN organic_social_media.shares IS 'Number of shares';
COMMENT ON COLUMN organic_social_media.follows IS 'Number of follows generated';
COMMENT ON COLUMN organic_social_media.comments IS 'Number of comments';
COMMENT ON COLUMN organic_social_media.saves IS 'Number of saves';
COMMENT ON COLUMN organic_social_media.content IS 'Human-readable text for search/display';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM organic_social_media;

