-- Add is_featured column to listings table if it doesn't exist
ALTER TABLE listings ADD COLUMN IF NOT EXISTS is_featured BOOLEAN DEFAULT FALSE;

-- Record the migration
INSERT INTO migrations (name) VALUES ('0002_add_is_featured_to_listings.sql')
ON CONFLICT (name) DO NOTHING;
