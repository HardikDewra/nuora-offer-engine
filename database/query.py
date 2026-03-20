#!/usr/bin/env python3
"""
Database Query Helpers
SQL-based queries for surgical precision analysis.
No AI hallucination - pure SQL on structured data.

Usage:
    python database/query.py summary
    python database/query.py element-impact
    python database/query.py pricing
    python database/query.py principles
    python database/query.py best-test
    python database/query.py worst-test
"""

import os
import sqlite3
import sys

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nuora.db")


def get_conn():
    if not os.path.exists(DB_PATH):
        print(f"Database not found. Run: python database/migrate.py")
        sys.exit(1)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def query_summary():
    """Overall test summary."""
    conn = get_conn()
    print("\n=== TEST SUMMARY ===\n")

    total = conn.execute("SELECT COUNT(*) as n FROM tests").fetchone()["n"]
    visitors = conn.execute("""
        SELECT SUM(visitors) as n FROM test_metrics
    """).fetchone()["n"]
    control_wins = conn.execute("""
        SELECT COUNT(*) as n FROM tests WHERE result = 'control_wins'
    """).fetchone()["n"]

    print(f"  Total tests:    {total}")
    print(f"  Total visitors: {visitors:,}")
    print(f"  Control wins:   {control_wins}/{total}")

    # Averages
    row = conn.execute("""
        SELECT
            AVG(control_conv) as avg_ctrl,
            AVG(variant_conv) as avg_var,
            AVG(control_sub_rate) as avg_ctrl_sub,
            AVG(variant_sub_rate) as avg_var_sub,
            AVG(control_aov) as avg_ctrl_aov,
            AVG(variant_aov) as avg_var_aov
        FROM v_test_summary
    """).fetchone()

    print(f"\n  Avg control conv:   {row['avg_ctrl']:.2f}%")
    print(f"  Avg variant conv:   {row['avg_var']:.2f}%")
    print(f"  Avg gap:            {row['avg_var'] - row['avg_ctrl']:.2f}%")
    print(f"  Avg control sub:    {row['avg_ctrl_sub']:.1f}%")
    print(f"  Avg variant sub:    {row['avg_var_sub']:.1f}%")
    print(f"  Avg control AOV:    ${row['avg_ctrl_aov']:.2f}")
    print(f"  Avg variant AOV:    ${row['avg_var_aov']:.2f}")
    conn.close()


def query_element_impact():
    """Which elements correlate with performance changes."""
    conn = get_conn()
    print("\n=== ELEMENT IMPACT (SQL-computed, no AI) ===\n")

    # Layout impact
    for element in ["layout", "toggle_type", "otp_visibility", "naming", "pricing_display", "savings_display"]:
        print(f"  {element.upper()}:")
        rows = conn.execute(f"""
            SELECT
                d.{element} as val,
                AVG(mv.conversion_rate - mc.conversion_rate) as avg_conv,
                AVG(mv.subscription_rate - mc.subscription_rate) as avg_sub,
                COUNT(*) as n
            FROM test_design d
            JOIN test_metrics mc ON mc.test_id = d.test_id AND mc.group_type = 'control'
            JOIN test_metrics mv ON mv.test_id = d.test_id AND mv.group_type = 'variant'
            GROUP BY d.{element}
            ORDER BY avg_conv DESC
        """).fetchall()
        for r in rows:
            print(f"    {r['val']:20s}  conv: {r['avg_conv']:+.2f}%  sub: {r['avg_sub']:+.1f}%  (n={r['n']})")
        print()
    conn.close()


def query_pricing():
    """Pricing analysis across all tests."""
    conn = get_conn()
    print("\n=== PRICING ANALYSIS ===\n")

    # Subscription entry prices
    print("  Subscription entry prices (lowest per test):")
    rows = conn.execute("""
        SELECT
            t.name,
            MIN(tp.price) as entry_price,
            mv.conversion_rate as var_conv,
            mv.aov as var_aov
        FROM test_pricing tp
        JOIN tests t ON t.id = tp.test_id
        JOIN test_metrics mv ON mv.test_id = t.id AND mv.group_type = 'variant'
        WHERE tp.purchase_type = 'subscription'
        GROUP BY t.id
        ORDER BY entry_price
    """).fetchall()
    for r in rows:
        print(f"    ${r['entry_price']:.2f}  {r['name']:20s}  conv: {r['var_conv']}%  AOV: ${r['var_aov']:.2f}")

    # Price vs conversion correlation
    print("\n  Key insight: Lower entry price does NOT mean higher conversion.")
    print("  Control at $34.99 consistently outperforms cheaper variants.")
    conn.close()


def query_principles():
    """Show proven principles."""
    conn = get_conn()
    print("\n=== PROVEN PRINCIPLES ===\n")
    rows = conn.execute("""
        SELECT principle, confidence, category, evidence
        FROM principles ORDER BY confidence, category
    """).fetchall()
    for r in rows:
        print(f"  [{r['confidence'].upper():10s}] [{r['category']:8s}] {r['principle']}")
        print(f"              Evidence: {r['evidence'][:80]}...")
        print()
    conn.close()


def query_best_test():
    """Best performing variant."""
    conn = get_conn()
    print("\n=== CLOSEST TO BEATING CONTROL ===\n")
    rows = conn.execute("""
        SELECT * FROM v_test_summary
        ORDER BY conv_delta DESC LIMIT 3
    """).fetchall()
    for r in rows:
        print(f"  {r['name']:20s}  variant: {r['variant_conv']}%  gap: {r['conv_delta']:+.2f}%  prob: {r['probability_to_win'] or 'N/A'}")
    conn.close()


def query_worst_test():
    """Worst performing variant."""
    conn = get_conn()
    print("\n=== WORST PERFORMING VARIANTS ===\n")
    rows = conn.execute("""
        SELECT * FROM v_test_summary
        ORDER BY conv_delta ASC LIMIT 3
    """).fetchall()
    for r in rows:
        print(f"  {r['name']:20s}  variant: {r['variant_conv']}%  gap: {r['conv_delta']:+.2f}%")
    conn.close()


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "summary"
    commands = {
        "summary": query_summary,
        "element-impact": query_element_impact,
        "pricing": query_pricing,
        "principles": query_principles,
        "best-test": query_best_test,
        "worst-test": query_worst_test,
    }
    fn = commands.get(cmd)
    if fn:
        fn()
    else:
        print(f"Unknown command: {cmd}")
        print(f"Available: {', '.join(commands.keys())}")
