-- Enhanced SQL script for ZERO data loss
-- Stores both processed metadata AND original raw data
-- Run this in your Supabase SQL Editor

-- Enable the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create table with enhanced data preservation
CREATE TABLE IF NOT EXISTS google_ads_documents (
    id BIGSERIAL PRIMARY KEY,
    
    -- Human-readable content (for embeddings)
    content TEXT NOT NULL,
    
    -- Processed metadata (for querying)
    metadata JSONB NOT NULL,
    
    -- RAW original data (100% preservation) ← NEW!
    raw_data JSONB NOT NULL,
    
    -- Vector embedding
    embedding vector(768),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for fast querying
CREATE INDEX IF NOT EXISTS google_ads_documents_embedding_idx 
ON google_ads_documents 
USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

CREATE INDEX IF NOT EXISTS google_ads_documents_metadata_idx 
ON google_ads_documents 
USING GIN (metadata);

CREATE INDEX IF NOT EXISTS google_ads_documents_raw_data_idx 
ON google_ads_documents 
USING GIN (raw_data);

CREATE INDEX IF NOT EXISTS google_ads_documents_content_idx 
ON google_ads_documents 
USING GIN (to_tsvector('english', content));

-- Create function for similarity search
CREATE OR REPLACE FUNCTION match_google_ads_documents (
    query_embedding vector(768),
    match_threshold float DEFAULT 0.5,
    match_count int DEFAULT 10
)
RETURNS TABLE (
    id bigint,
    content text,
    metadata jsonb,
    raw_data jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        google_ads_documents.id,
        google_ads_documents.content,
        google_ads_documents.metadata,
        google_ads_documents.raw_data,
        1 - (google_ads_documents.embedding <=> query_embedding) as similarity
    FROM google_ads_documents
    WHERE 1 - (google_ads_documents.embedding <=> query_embedding) > match_threshold
    ORDER BY google_ads_documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

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
COMMENT ON TABLE google_ads_documents IS 'Stores Google Ads data with 100% preservation - includes raw data, processed metadata, and embeddings';
COMMENT ON COLUMN google_ads_documents.content IS 'Human-readable text for embeddings';
COMMENT ON COLUMN google_ads_documents.metadata IS 'Processed metadata for efficient querying';
COMMENT ON COLUMN google_ads_documents.raw_data IS 'Original raw CSV data - 100% preservation of source';
COMMENT ON COLUMN google_ads_documents.embedding IS 'Vector embedding from Google Gemini (768 dimensions)';
COMMENT ON FUNCTION match_google_ads_documents IS 'Semantic similarity search function';

-- Verification query
SELECT 
    'Table created successfully!' as status,
    COUNT(*) as row_count
FROM google_ads_documents;

