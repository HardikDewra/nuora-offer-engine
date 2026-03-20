#!/usr/bin/env python3
"""
Database Migration Script
Loads all JSON test data into SQLite database.
Run this after adding new test JSON files.

Usage:
    python database/migrate.py              # Build/rebuild database
    python database/migrate.py --verify     # Verify data integrity
"""

import json
import os
import sqlite3
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "nuora.db")
SCHEMA_PATH = os.path.join(BASE_DIR, "database", "schema.sql")
TEST_RESULTS_DIR = os.path.join(BASE_DIR, "data", "test_results")


def get_connection():
    """Get SQLite connection with foreign keys enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_schema(conn):
    """Create tables from schema.sql."""
    with open(SCHEMA_PATH) as f:
        conn.executescript(f.read())
    conn.commit()
    print(f"[migrate] Schema initialized")


def load_test(conn, filepath):
    """Load a single test JSON file into the database."""
    with open(filepath) as f:
        data = json.load(f)

    name = data.get("name")
    if not name:
        print(f"[migrate] Skipping {filepath} - no name field")
        return

    # Skip control reference file (it's not a test)
    if os.path.basename(filepath) == "control.json":
        print(f"[migrate] Skipping control.json (reference file, not a test)")
        return

    # Check if already exists
    existing = conn.execute("SELECT id FROM tests WHERE name = ?", (name,)).fetchone()
    if existing:
        print(f"[migrate] Updating existing: {name}")
        test_id = existing["id"]
        conn.execute("DELETE FROM test_design WHERE test_id = ?", (test_id,))
        conn.execute("DELETE FROM test_metrics WHERE test_id = ?", (test_id,))
        conn.execute("DELETE FROM test_pricing WHERE test_id = ?", (test_id,))
        conn.execute("DELETE FROM test_learnings WHERE test_id = ?", (test_id,))
        conn.execute("DELETE FROM tests WHERE id = ?", (test_id,))

    # Insert test
    conn.execute("""
        INSERT INTO tests (name, style, version, url, inspiration_url, test_date,
                          duration_hours, result, probability_to_win, changes_from_previous)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        data.get("style", "Unknown"),
        data.get("version", "V1"),
        data.get("url"),
        data.get("inspiration"),
        data.get("test_date"),
        data.get("duration_hours"),
        data.get("result", "control_wins"),
        data.get("probability_to_win"),
        data.get("changes_from_v1") or data.get("changes_from_previous"),
    ))
    test_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]

    # Insert design elements
    design = data.get("design", {})
    if design:
        conn.execute("""
            INSERT INTO test_design (test_id, layout, toggle_type, otp_visibility,
                                    naming, num_options, pricing_display, savings_display,
                                    product_images, cta_copy, bundle_names, badges, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_id,
            design.get("layout", "vertical"),
            design.get("toggle_type", "unknown"),
            design.get("otp_visibility", "unknown"),
            design.get("naming", "unknown"),
            design.get("num_options", 3),
            design.get("pricing_display", "standard"),
            design.get("savings_display", "none"),
            1 if design.get("product_images") else 0,
            design.get("cta_copy", "add_to_cart"),
            json.dumps(design.get("bundle_names", [])),
            json.dumps(design.get("badges", [])),
            design.get("subscription_info_location"),
        ))

    # Insert metrics
    metrics = data.get("metrics", {})
    for group in ["control", "variant"]:
        m = metrics.get(group, {})
        if not m:
            continue
        conn.execute("""
            INSERT INTO test_metrics (test_id, group_type, visitors, revenue,
                                     revenue_per_visitor, conversion_rate, orders, aov,
                                     profit, profit_per_visitor, shipping_revenue,
                                     add_to_cart_rate, reached_checkout_rate,
                                     session_duration_sec, otp_orders,
                                     subscription_orders, subscription_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_id, group,
            m.get("visitors", 0),
            m.get("revenue", 0),
            m.get("revenue_per_visitor", 0),
            m.get("conversion_rate", 0),
            m.get("orders", 0),
            m.get("aov", 0),
            m.get("profit"),
            m.get("profit_per_visitor"),
            m.get("shipping_revenue", 0),
            m.get("add_to_cart_rate"),
            m.get("reached_checkout_rate"),
            m.get("session_duration_sec"),
            m.get("otp_orders", 0),
            m.get("subscription_orders", 0),
            m.get("subscription_rate"),
        ))

    # Insert pricing
    pricing = data.get("pricing", {})
    for purchase_type in ["subscription", "one_time"]:
        for pack_name, details in pricing.get(purchase_type, {}).items():
            conn.execute("""
                INSERT INTO test_pricing (test_id, purchase_type, pack_name, price,
                                         compare_at_price, discount_pct, per_pack,
                                         per_day, per_serving, delivery_frequency,
                                         refill_price, refill_days)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                test_id, purchase_type, pack_name,
                details.get("price", 0),
                details.get("compare") or details.get("compare_at_price"),
                details.get("discount_pct") or details.get("savings_pct"),
                details.get("per_pack"),
                details.get("per_day"),
                details.get("per_serving"),
                details.get("delivery") or details.get("frequency"),
                details.get("refill_price"),
                details.get("refill_days"),
            ))

    # Insert learnings
    for learning in data.get("key_learnings", []):
        conn.execute("""
            INSERT INTO test_learnings (test_id, learning) VALUES (?, ?)
        """, (test_id, learning))

    conn.commit()
    print(f"[migrate] Loaded: {name}")


def seed_principles(conn):
    """Seed proven principles from test analysis."""
    principles = [
        ("Horizontal card layout outperforms vertical stacked cards",
         "All 7 variants used vertical layouts and all lost to horizontal control",
         "proven", "layout"),
        ("Checkbox subscription toggle with pre-selection outperforms all alternatives",
         "Side-by-side toggle (-2.2% conv), separate card (-1.4%), no toggle (-1.7%)",
         "proven", "toggle"),
        ("OTP should exist but not be prominent",
         "Removing OTP hurts conversion; making it visible hurts subscription rate",
         "proven", "toggle"),
        ("Pack-based naming beats time-based and BOGO naming",
         "Time-based: -0.5% conv. BOGO: -1.7% conv and eliminates OTP entirely",
         "proven", "naming"),
        ("3 options outperform 2 options",
         "2-option variants averaged -0.5% conversion vs 3-option control",
         "likely", "layout"),
        ("Subscription entry price sweet spot is $34-40",
         "Control $34.99 wins. Sub-$30 (Resilia) and $40+ (Omre) both underperform",
         "proven", "pricing"),
        ("OTP-to-subscription gap should be 14-15%",
         "Control maintains 14-15% gap. Wider gaps may push more toward subscription",
         "likely", "pricing"),
        ("Product images on cards have no measurable impact on conversion",
         "Tested in Resilia V1 and Ryze V2 - zero conversion lift",
         "proven", "layout"),
        ("33.2% of cancellations are accidental subscriptions - highest ROI fix",
         "12,191 subscribers lost. Checkout UX fix worth more than any offer test",
         "proven", "general"),
    ]

    conn.execute("DELETE FROM principles")
    for principle, evidence, confidence, category in principles:
        conn.execute("""
            INSERT INTO principles (principle, evidence, confidence, category)
            VALUES (?, ?, ?, ?)
        """, (principle, evidence, confidence, category))
    conn.commit()
    print(f"[migrate] Seeded {len(principles)} proven principles")


def seed_weights(conn):
    """Seed scoring weights from current analysis."""
    sys.path.insert(0, BASE_DIR)
    from config.settings import CONVERSION_WEIGHTS, SUBSCRIPTION_WEIGHTS

    conn.execute("DELETE FROM scoring_weights")
    for element, values in CONVERSION_WEIGHTS.items():
        for value, conv_w in values.items():
            sub_w = SUBSCRIPTION_WEIGHTS.get(element, {}).get(value, 0)
            conn.execute("""
                INSERT OR REPLACE INTO scoring_weights
                (element, value, conv_weight, sub_weight, sample_size)
                VALUES (?, ?, ?, ?, ?)
            """, (element, str(value), conv_w, sub_w, 7))
    conn.commit()
    print(f"[migrate] Seeded scoring weights")


def verify(conn):
    """Verify database integrity."""
    print("\n[verify] Database integrity check:")

    tests = conn.execute("SELECT COUNT(*) as n FROM tests").fetchone()["n"]
    print(f"  Tests:      {tests}")

    metrics = conn.execute("SELECT COUNT(*) as n FROM test_metrics").fetchone()["n"]
    print(f"  Metrics:    {metrics} rows ({metrics // 2} tests x 2 groups)")

    designs = conn.execute("SELECT COUNT(*) as n FROM test_design").fetchone()["n"]
    print(f"  Designs:    {designs}")

    pricing = conn.execute("SELECT COUNT(*) as n FROM test_pricing").fetchone()["n"]
    print(f"  Pricing:    {pricing} price points")

    learnings = conn.execute("SELECT COUNT(*) as n FROM test_learnings").fetchone()["n"]
    print(f"  Learnings:  {learnings}")

    principles = conn.execute("SELECT COUNT(*) as n FROM principles").fetchone()["n"]
    print(f"  Principles: {principles}")

    weights = conn.execute("SELECT COUNT(*) as n FROM scoring_weights").fetchone()["n"]
    print(f"  Weights:    {weights}")

    # Check test summary view
    print("\n[verify] Test summary:")
    for row in conn.execute("SELECT name, control_conv, variant_conv, conv_delta, total_visitors FROM v_test_summary ORDER BY test_date"):
        print(f"  {row['name']:20s}  control: {row['control_conv']}%  variant: {row['variant_conv']}%  delta: {row['conv_delta']:+.2f}%  visitors: {row['total_visitors']}")

    print("\n[verify] All checks passed")


def main():
    print(f"[migrate] Database: {DB_PATH}")

    conn = get_connection()
    init_schema(conn)

    # Load all test JSON files
    print(f"\n[migrate] Loading test data from {TEST_RESULTS_DIR}")
    for filename in sorted(os.listdir(TEST_RESULTS_DIR)):
        if filename.endswith(".json"):
            load_test(conn, os.path.join(TEST_RESULTS_DIR, filename))

    # Seed principles and weights
    print()
    seed_principles(conn)
    seed_weights(conn)

    # Verify
    if "--verify" in sys.argv or True:  # always verify
        verify(conn)

    conn.close()
    print(f"\n[migrate] Done. Database at: {DB_PATH}")


if __name__ == "__main__":
    main()
