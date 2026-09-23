CREATE DATABASE ecom_db;
GO
USE ecom_db; -- Or your target MSSQL DB
GO

CREATE TABLE legacy_ledger (
    entry_id INT PRIMARY KEY IDENTITY(1,1),
    account_code VARCHAR(20) NOT NULL,    -- e.g., '1010' for Cash, '4010' for Revenue
    account_name VARCHAR(100) NOT NULL,
    amount DECIMAL(18,4) NOT NULL,        -- Strict financial precision
    entry_type VARCHAR(10) NOT NULL,       -- 'DEBIT' or 'CREDIT'
    currency VARCHAR(3) NOT NULL,          -- 'USD' or 'PHP'
    posted_at DATETIME NOT NULL,
    reconciliation_status VARCHAR(20) DEFAULT 'unverified'
);

-- Seed financial records
INSERT INTO legacy_ledger (account_code, account_name, amount, entry_type, currency, posted_at, reconciliation_status) VALUES
('1010', 'Cash Operating Account', 50000.0000, 'DEBIT',  'PHP', '2026-01-15 09:00:00', 'completed'),
('4010', 'Product Sales Revenue',  1000.0000,  'CREDIT', 'USD', '2026-01-15 10:30:00', 'completed'),
('1200', 'Accounts Receivable',   1000.0000,  'DEBIT',  'USD', '2026-01-15 10:30:00', 'completed'),
('4010', 'Product Sales Revenue',  25000.0000, 'CREDIT', 'PHP', '2026-01-16 14:15:00', 'COMPLETED'), -- Text anomaly
('1010', 'Cash Operating Account', 25000.0000, 'DEBIT',  'PHP', '2026-01-16 14:15:00', 'completed');