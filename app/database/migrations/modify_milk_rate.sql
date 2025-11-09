-- First, remove the is_active column since we won't be using it
ALTER TABLE public.milk_rate_configuration 
    DROP COLUMN is_active;

-- Add a unique constraint to prevent overlapping date ranges
-- This ensures only one rate configuration can exist for any given date
ALTER TABLE public.milk_rate_configuration
    ADD CONSTRAINT no_date_overlap 
    EXCLUDE USING gist (
        daterange(effective_from, COALESCE(effective_to, 'infinity'::date)) WITH &&
    );

-- Add missing constraints
ALTER TABLE public.milk_rate_configuration
    ALTER COLUMN created_at SET DEFAULT CURRENT_TIMESTAMP,
    -- Ensure effective_to is after effective_from when provided
    ADD CONSTRAINT valid_date_range 
        CHECK (effective_to IS NULL OR effective_to > effective_from);

-- Clean up any existing data that might have overlapping dates
-- This should be run carefully in production as it might delete data
WITH ranked_rates AS (
    SELECT 
        id,
        ROW_NUMBER() OVER (
            PARTITION BY date_range 
            ORDER BY created_at DESC
        ) as rn
    FROM (
        SELECT 
            id, 
            created_at,
            daterange(effective_from, COALESCE(effective_to, 'infinity'::date)) as date_range
        FROM public.milk_rate_configuration
    ) t
)
DELETE FROM public.milk_rate_configuration
WHERE id IN (
    SELECT id 
    FROM ranked_rates 
    WHERE rn > 1
);

-- Documentation of the modified table:
COMMENT ON TABLE public.milk_rate_configuration IS 'Stores milk rate configurations with non-overlapping date ranges';
COMMENT ON COLUMN public.milk_rate_configuration.effective_from IS 'Start date of the rate configuration';
COMMENT ON COLUMN public.milk_rate_configuration.effective_to IS 'End date of the rate configuration (NULL means no end date)';
COMMENT ON COLUMN public.milk_rate_configuration.fat_rate IS 'Rate per 0.1% fat above base fat';
COMMENT ON COLUMN public.milk_rate_configuration.snf_rate IS 'Rate per 0.1% SNF above base SNF';
COMMENT ON COLUMN public.milk_rate_configuration.base_fat IS 'Base fat percentage';
COMMENT ON COLUMN public.milk_rate_configuration.base_snf IS 'Base SNF percentage';