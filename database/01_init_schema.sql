-- EXTENSIONS
-- Ensure UUID generation is available (Standard in Supabase, but good practice to be explicit)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- TRANSACTIONS LOG
-- Stores the raw incoming data from the card network/frontend
CREATE TABLE IF NOT EXISTS transactions_log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Business Features
    amount NUMERIC(15, 2) NOT NULL, -- Numeric is better for money than float
    seconds_elapsed FLOAT NOT NULL, -- Corresponds to 'Time' feature
    
    -- The PCA Features (V1-V28) stored as a JSON object
    -- Example: {"v1": -1.3, "v2": 0.5, ...}
    pca_vector JSONB NOT NULL
);

-- FRAUD PREDICTIONS
-- Stores the inference results from our Python Service
CREATE TABLE IF NOT EXISTS fraud_predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Foreign Key to the transaction
    transaction_id UUID NOT NULL REFERENCES transactions_log(id) ON DELETE CASCADE,
    
    -- Model Output
    model_version TEXT DEFAULT 'v1.0.0',
    risk_score FLOAT NOT NULL, -- The probability (0.0 to 1.0)
    prediction_class INT NOT NULL, -- 0 (Safe) or 1 (Fraud)
    
    -- Performance Metrics (Optional but good for monitoring)
    execution_time_ms FLOAT
);

-- PERFORMANCE OPTIMIZATION (INDEXING)
-- Critical for the Dashboard to load history quickly
CREATE INDEX IF NOT EXISTS idx_transactions_created_at ON transactions_log(created_at DESC);

-- Critical for joining predictions with transactions
CREATE INDEX IF NOT EXISTS idx_predictions_transaction_id ON fraud_predictions(transaction_id);

-- Critical for filtering "Show me high risk transactions"
CREATE INDEX IF NOT EXISTS idx_predictions_risk_score ON fraud_predictions(risk_score DESC);

-- SECURE ACCESS (Row Level Security)
-- Standard Supabase practice: Enable RLS.
ALTER TABLE transactions_log ENABLE ROW LEVEL SECURITY;
ALTER TABLE fraud_predictions ENABLE ROW LEVEL SECURITY;

-- For this demo, we allow public read/write to avoid complex auth setup in the Python script.
-- IN PRODUCTION: You would restrict this to a specific Service Role.
CREATE POLICY "Enable access to all users" ON transactions_log FOR ALL USING (true);
CREATE POLICY "Enable access to all users" ON fraud_predictions FOR ALL USING (true);