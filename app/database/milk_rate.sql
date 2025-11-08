CREATE TABLE
    public.milk_rate_configuration (
        id SERIAL PRIMARY KEY,
        base_rate DECIMAL(10, 2) NOT NULL,
        fat_rate DECIMAL(10, 2) NOT NULL, -- Rate per 0.1% fat above base fat
        snf_rate DECIMAL(10, 2) NOT NULL, -- Rate per 0.1% SNF above base SNF
        base_fat DECIMAL(4, 2) NOT NULL, -- Base fat percentage
        base_snf DECIMAL(4, 2) NOT NULL, -- Base SNF percentage
        effective_from DATE NOT NULL,
        effective_to DATE, -- NULL means currently active
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            CONSTRAINT valid_base_rate CHECK (base_rate > 0),
            CONSTRAINT valid_fat_rate CHECK (fat_rate >= 0),
            CONSTRAINT valid_snf_rate CHECK (snf_rate >= 0),
            CONSTRAINT valid_base_fat CHECK (base_fat BETWEEN 0 AND 100),
            CONSTRAINT valid_base_snf CHECK (base_snf BETWEEN 0 AND 100)
    );