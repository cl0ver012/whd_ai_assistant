-- Simple SQL setup without embeddings requirement
-- Stores raw data and metadata only
-- Run this in your Supabase SQL Editor

-- Create table without vector requirement
CREATE TABLE IF NOT EXISTS google_ads_documents (
    id BIGSERIAL PRIMARY KEY,
    
    -- Human-readable content
    content TEXT NOT NULL,
    
    -- Processed metadata (for querying)
    metadata JSONB NOT NULL,
    
    -- RAW original data (100% preservation)
    raw_data JSONB NOT NULL,
    
    -- Embedding (optional - can add later)
    embedding TEXT,
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for fast querying
CREATE INDEX IF NOT EXISTS google_ads_documents_metadata_idx 
ON google_ads_documents 
USING GIN (metadata);

CREATE INDEX IF NOT EXISTS google_ads_documents_raw_data_idx 
ON google_ads_documents 
USING GIN (raw_data);

CREATE INDEX IF NOT EXISTS google_ads_documents_content_idx 
ON google_ads_documents 
USING GIN (to_tsvector('english', content));

CREATE INDEX IF NOT EXISTS google_ads_documents_created_at_idx 
ON google_ads_documents (created_at);

-- Add update timestamp trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_google_ads_documents_updated_at
    BEFORE UPDATE ON google_ads_documents
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE google_ads_documents IS 'Google Ads data with 100% preservation - raw data + processed metadata';
COMMENT ON COLUMN google_ads_documents.content IS 'Human-readable text content';
COMMENT ON COLUMN google_ads_documents.metadata IS 'Processed metadata for efficient querying';
COMMENT ON COLUMN google_ads_documents.raw_data IS 'Original raw CSV data - 100% preservation';
COMMENT ON COLUMN google_ads_documents.embedding IS 'Optional: Vector embedding (can be added later)';

-- Verification query
SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM google_ads_documents;

