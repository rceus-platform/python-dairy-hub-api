-- Add shift column to milk_collection table
ALTER TABLE public.milk_collection
ADD COLUMN shift VARCHAR(10) NOT NULL DEFAULT 'morning' CHECK (shift IN ('morning', 'evening'));

-- Add a unique constraint to prevent duplicate collections for same farmer, date and shift
ALTER TABLE public.milk_collection ADD CONSTRAINT unique_farmer_collection UNIQUE (farmer_id, collection_date, shift);

-- Create index for faster lookups
CREATE INDEX idx_milk_collection_shift ON public.milk_collection (shift, collection_date);