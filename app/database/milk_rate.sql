CREATE TABLE
    public.milk_rate_configuration (
        id SERIAL PRIMARY KEY,
        base_rate DECIMAL(10, 2) NOT NULL,
        fat_rate DECIMAL(10, 2) NOT NULL,
        snf_rate DECIMAL(10, 2) NOT NULL,
        base_fat DECIMAL(5, 2) NOT NULL,
        base_snf DECIMAL(5, 2) NOT NULL,
        effective_from DATE NOT NULL,
        effective_to DATE,
        description TEXT,
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );