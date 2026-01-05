CREATE TABLE IF NOT EXISTS fact_billing (
    patient_id VARCHAR(20),
    visit_date DATE,
    department VARCHAR(50),
    procedure VARCHAR(100),
    charges NUMERIC,
    collections NUMERIC,
    ar_amount NUMERIC,
    payment_status VARCHAR(20),
    load_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_department_access (
    user_name VARCHAR(50),
    department VARCHAR(50)
);
