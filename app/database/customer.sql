CREATE TABLE
    public.customer (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        email VARCHAR(255),
        phone VARCHAR(20) NOT NULL,
        address TEXT NOT NULL,
        customer_type VARCHAR(20) NOT NULL CHECK (customer_type IN ('regular', 'wholesale')),
        created_at TIMESTAMP
        WITH
            TIME ZONE DEFAULT CURRENT_TIMESTAMP,
            is_active BOOLEAN DEFAULT TRUE
    );

-- Create an index on email for faster lookups
CREATE INDEX idx_customer_email ON public.customer (email);

-- Create an index on phone number for faster lookups
CREATE INDEX idx_customer_phone ON public.customer (phone);

-- Add some comments to the table and columns for better documentation
COMMENT ON TABLE public.customer IS 'Stores information about dairy customers';

COMMENT ON COLUMN public.customer.customer_type IS 'Type of customer: regular or wholesale';

COMMENT ON COLUMN public.customer.is_active IS 'Flag to indicate if the customer account is active';