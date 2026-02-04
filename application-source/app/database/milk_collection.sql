-- Milk Collection Table
CREATE TABLE
    public.milk_collection (
        id SERIAL PRIMARY KEY,
        farmer_id INTEGER NOT NULL REFERENCES public.customer (id),
        quantity DECIMAL(10, 2) NOT NULL, -- in liters
        fat_content DECIMAL(4, 2) NOT NULL, -- percentage
        snf_content DECIMAL(4, 2) NOT NULL, -- Solids-Not-Fat percentage
        rate_per_liter DECIMAL(10, 2) NOT NULL,
        collection_date TIMESTAMP
        WITH
            TIME ZONE NOT NULL,
            total_amount DECIMAL(12, 2) NOT NULL, -- calculated field (quantity * rate)
            created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT valid_quantity CHECK (quantity > 0),
            CONSTRAINT valid_fat CHECK (fat_content BETWEEN 0 AND 100),
            CONSTRAINT valid_snf CHECK (snf_content BETWEEN 0 AND 100)
    );