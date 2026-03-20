-- Nuora Offer Intelligence Database Schema
-- Compatible with both SQLite (local) and PostgreSQL (production)
--
-- Data flow:
--   JSON files (intake) -> migrate.py -> SQLite/Postgres (analysis)
--   MD files store PRINCIPLES and METHODOLOGY only (not test data)
--   Database stores ALL quantitative test data for query precision

-- Tests: every A/B test we run
CREATE TABLE IF NOT EXISTS tests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    style TEXT NOT NULL,           -- e.g. 'Ankhway', 'Ryze', 'Omre', 'Resilia', 'Custom'
    version TEXT NOT NULL,         -- e.g. 'V1', 'V2', 'V3'
    url TEXT,
    inspiration_url TEXT,
    test_date DATE NOT NULL,
    duration_hours REAL,
    result TEXT NOT NULL,          -- 'control_wins', 'variant_wins', 'inconclusive'
    probability_to_win REAL,      -- variant's probability to win (%)
    changes_from_previous TEXT,   -- what changed from prior version
    product TEXT DEFAULT 'vaginal_probiotic_gummies',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name)
);

-- Design elements: the specific UI/UX choices in each test
CREATE TABLE IF NOT EXISTS test_design (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL REFERENCES tests(id),
    layout TEXT NOT NULL,              -- 'horizontal', 'vertical'
    toggle_type TEXT NOT NULL,         -- 'checkbox', 'side_by_side', 'none', 'separate_card'
    otp_visibility TEXT NOT NULL,      -- 'behind_toggle', 'separate_card', 'equal_weight', 'not_available'
    naming TEXT NOT NULL,              -- 'pack_based', 'time_based', 'creative', 'bogo'
    num_options INTEGER NOT NULL,      -- 2 or 3
    pricing_display TEXT NOT NULL,     -- 'standard', 'rounded'
    savings_display TEXT NOT NULL,     -- 'none', 'dollar', 'percent'
    product_images BOOLEAN DEFAULT 0,
    cta_copy TEXT NOT NULL,            -- 'add_to_cart', 'buy_now', 'get_started'
    bundle_names TEXT,                 -- JSON array of names used
    badges TEXT,                       -- JSON array of badges used
    notes TEXT,                        -- any other design notes
    UNIQUE(test_id)
);

-- Metrics: control and variant performance numbers
CREATE TABLE IF NOT EXISTS test_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL REFERENCES tests(id),
    group_type TEXT NOT NULL,          -- 'control' or 'variant'
    visitors INTEGER NOT NULL,
    revenue REAL NOT NULL,
    revenue_per_visitor REAL NOT NULL,
    conversion_rate REAL NOT NULL,
    orders INTEGER NOT NULL,
    aov REAL NOT NULL,
    profit REAL,
    profit_per_visitor REAL,
    shipping_revenue REAL DEFAULT 0,
    add_to_cart_rate REAL,
    reached_checkout_rate REAL,
    session_duration_sec REAL,
    otp_orders INTEGER DEFAULT 0,
    subscription_orders INTEGER DEFAULT 0,
    subscription_rate REAL,
    UNIQUE(test_id, group_type)
);

-- Pricing: what prices were used in each test
CREATE TABLE IF NOT EXISTS test_pricing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL REFERENCES tests(id),
    purchase_type TEXT NOT NULL,       -- 'subscription' or 'one_time'
    pack_name TEXT NOT NULL,           -- e.g. '1_pack', '3_month', 'starter_kit'
    price REAL NOT NULL,
    compare_at_price REAL,
    discount_pct REAL,
    per_pack REAL,
    per_day REAL,
    per_serving REAL,
    delivery_frequency TEXT,           -- e.g. 'monthly', 'quarterly'
    refill_price REAL,
    refill_days INTEGER
);

-- Learnings: key takeaways from each test (intelligence data)
CREATE TABLE IF NOT EXISTS test_learnings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    test_id INTEGER NOT NULL REFERENCES tests(id),
    learning TEXT NOT NULL,
    category TEXT,                     -- 'pricing', 'layout', 'toggle', 'naming', 'general'
    severity TEXT                      -- 'critical', 'high', 'medium', 'low'
);

-- Proven principles: distilled from multiple tests (stored in MD files too)
CREATE TABLE IF NOT EXISTS principles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    principle TEXT NOT NULL,
    evidence TEXT NOT NULL,            -- which tests support this
    confidence TEXT NOT NULL,          -- 'proven', 'likely', 'hypothesis'
    category TEXT,                     -- 'layout', 'pricing', 'toggle', 'naming', 'general'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Element weights: scoring model weights (updated as more tests come in)
CREATE TABLE IF NOT EXISTS scoring_weights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    element TEXT NOT NULL,             -- e.g. 'layout', 'toggle_type'
    value TEXT NOT NULL,               -- e.g. 'horizontal', 'checkbox'
    conv_weight REAL NOT NULL,         -- conversion rate impact
    sub_weight REAL NOT NULL,          -- subscription rate impact
    sample_size INTEGER NOT NULL,      -- number of tests this is based on
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(element, value)
);

-- Views for common queries

-- Summary of all tests with key metrics
CREATE VIEW IF NOT EXISTS v_test_summary AS
SELECT
    t.id,
    t.name,
    t.style,
    t.version,
    t.test_date,
    t.result,
    t.probability_to_win,
    mc.conversion_rate AS control_conv,
    mv.conversion_rate AS variant_conv,
    (mv.conversion_rate - mc.conversion_rate) AS conv_delta,
    mc.subscription_rate AS control_sub_rate,
    mv.subscription_rate AS variant_sub_rate,
    mc.aov AS control_aov,
    mv.aov AS variant_aov,
    mc.revenue_per_visitor AS control_rpv,
    mv.revenue_per_visitor AS variant_rpv,
    (mc.visitors + mv.visitors) AS total_visitors
FROM tests t
JOIN test_metrics mc ON mc.test_id = t.id AND mc.group_type = 'control'
JOIN test_metrics mv ON mv.test_id = t.id AND mv.group_type = 'variant';

-- Element impact analysis
CREATE VIEW IF NOT EXISTS v_element_impact AS
SELECT
    d.layout,
    d.toggle_type,
    d.otp_visibility,
    d.naming,
    d.num_options,
    d.pricing_display,
    d.savings_display,
    d.product_images,
    d.cta_copy,
    AVG(mv.conversion_rate - mc.conversion_rate) AS avg_conv_delta,
    AVG(mv.subscription_rate - mc.subscription_rate) AS avg_sub_delta,
    COUNT(*) AS test_count
FROM test_design d
JOIN tests t ON t.id = d.test_id
JOIN test_metrics mc ON mc.test_id = t.id AND mc.group_type = 'control'
JOIN test_metrics mv ON mv.test_id = t.id AND mv.group_type = 'variant'
GROUP BY d.layout, d.toggle_type, d.otp_visibility, d.naming,
         d.num_options, d.pricing_display, d.savings_display,
         d.product_images, d.cta_copy;
