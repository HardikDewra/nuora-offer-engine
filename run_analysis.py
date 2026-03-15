#!/usr/bin/env python3
"""
Nuora Offer Intelligence Engine - Main Entry Point

Run this script to:
1. Load and analyze all A/B test data
2. Compute pricing sweet spots
3. Score the current control offer
4. Generate recommendations for next tests
5. Calculate LTV projections
6. Output a full analysis report

Usage:
    python run_analysis.py
    python run_analysis.py --scrape    # Also scrape live product data
"""

import sys
import os
import json
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.analyzer import OfferAnalyzer
from engine.pricing_optimizer import PricingOptimizer
from engine.offer_scorer import OfferScorer
from engine.recommendation_engine import RecommendationEngine
from engine.ltv_calculator import LTVCalculator
from config.settings import REPORTS_DIR


def print_header(title):
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def print_section(title):
    print(f"\n--- {title} ---\n")


def run_analysis():
    """Run the full analysis pipeline."""
    print_header("NUORA OFFER INTELLIGENCE ENGINE v1.0")
    print(f"Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"Data Source: 7 A/B tests, Jan 2026")

    # Optional: scrape live data
    if "--scrape" in sys.argv:
        print_section("SCRAPING LIVE PRODUCT DATA")
        from scrapers.nuora_scraper import NuoraScraper
        scraper = NuoraScraper()
        scraper.run()

    # 1. Initialize analyzers
    print_section("LOADING TEST DATA")
    analyzer = OfferAnalyzer()
    print(f"Loaded {len(analyzer.get_all_tests())} test results + control reference")

    # 2. Summary Stats
    print_section("SUMMARY STATISTICS")
    stats = analyzer.compute_summary_stats()
    print(f"  Total tests run:          {stats['total_tests']}")
    print(f"  Total visitors tested:    {stats['total_visitors']:,}")
    print(f"  Control wins:             {stats['control_wins']}/{stats['total_tests']}")
    print(f"  Avg control conversion:   {stats['avg_control_conv']}%")
    print(f"  Avg variant conversion:   {stats['avg_variant_conv']}%")
    print(f"  Conversion gap:           -{stats['conv_gap']}%")
    print(f"  Avg control sub rate:     {stats['avg_control_sub_rate']}%")
    print(f"  Avg variant sub rate:     {stats['avg_variant_sub_rate']}%")
    print(f"  Avg control AOV:          ${stats['avg_control_aov']}")
    print(f"  Avg variant AOV:          ${stats['avg_variant_aov']}")

    # 3. Element Impact
    print_section("ELEMENT IMPACT ANALYSIS")
    impacts = analyzer.compute_element_impact()
    for element, values in impacts.items():
        print(f"\n  {element.upper()}:")
        for value, data in values.items():
            print(f"    {value:20s}  conv: {data['avg_conv_impact']:+.2f}%  "
                  f"sub: {data['avg_sub_impact']:+.1f}%  "
                  f"(n={data['sample_size']})")

    # 4. Winning & Losing Patterns
    print_section("WINNING PATTERNS (Control)")
    winning = analyzer.identify_winning_patterns()
    for key, value in winning.items():
        print(f"  {key:20s}: {value}")

    print_section("LOSING PATTERNS (Avoid)")
    losing = analyzer.identify_losing_patterns()
    for item in losing:
        print(f"  [{item['severity'].upper():8s}] {item['pattern']}")
        print(f"              Impact: {item['avg_impact']}")
        print(f"              Tested: {item['tested_in']}")

    # 5. Pricing Analysis
    print_section("PRICING SWEET SPOTS")
    optimizer = PricingOptimizer(analyzer)
    sweet_spots = optimizer.find_sweet_spots()

    entry = sweet_spots["subscription_entry_point"]
    print(f"  Subscription entry point:")
    print(f"    Current (control): ${entry['current_control']}")
    print(f"    Tested range:      ${entry['range_tested']['min']} - ${entry['range_tested']['max']}")
    print(f"    Sweet spot:        ${entry['sweet_spot']['low']} - ${entry['sweet_spot']['high']}")
    print(f"    Why: {entry['sweet_spot']['reasoning'][:100]}...")

    bundle = sweet_spots["subscription_max_bundle"]
    print(f"\n  Max bundle price:")
    print(f"    Current (control): ${bundle['current_control']}")
    print(f"    Sweet spot:        ${bundle['sweet_spot']['low']} - ${bundle['sweet_spot']['high']}")

    pp = sweet_spots["per_pack_analysis"]
    print(f"\n  Per-pack subscription pricing:")
    for pack, data in pp["subscription"].items():
        print(f"    {pack}: ${data['price']}/pack (${data['per_day']}/day)")

    # 6. Pricing Recommendations
    print_section("PRICING RECOMMENDATIONS")
    pricing_recs = optimizer.generate_pricing_recommendations()
    print("  KEEP (proven working):")
    for item in pricing_recs["keep"]:
        print(f"    + {item}")
    print("\n  TEST (potentially better):")
    for item in pricing_recs["test"]:
        print(f"    ? {item['change']}")
        print(f"      Risk: {item['risk']} | Expected: {item['expected_impact']}")
    print("\n  AVOID (data says no):")
    for item in pricing_recs["avoid"]:
        print(f"    x {item}")

    # 7. Offer Scoring
    print_section("OFFER SCORING")
    scorer = OfferScorer()

    # Score control
    ctrl_score = scorer.score_control()
    print(f"  Control score:       {ctrl_score['predicted_conversion_rate']}%")
    print(f"  Control sub rate:    {ctrl_score['predicted_subscription_rate']}%")
    print(f"  Risk level:          {ctrl_score['risk_level']}")

    # Score a hypothetical: control + savings badges
    hypo = scorer.score_offer({
        "layout": "horizontal",
        "toggle_type": "checkbox",
        "otp_visibility": "behind_toggle",
        "naming": "pack_based",
        "num_options": 3,
        "pricing_display": "standard",
        "savings_display": "dollar",
        "product_images": False,
        "cta_copy": "add_to_cart",
    })
    print(f"\n  Hypothetical (Control + Save $X badges):")
    print(f"    Predicted conv:    {hypo['predicted_conversion_rate']}%")
    print(f"    Predicted sub:     {hypo['predicted_subscription_rate']}%")
    print(f"    Risk:              {hypo['risk_level']}")
    for b in hypo["breakdown"]:
        print(f"    {b['element']:20s} -> {b['value']:20s}  conv: {b['conv_impact']:+.1f}%")

    # 8. LTV Projections
    print_section("LTV PROJECTIONS")
    ltv_calc = LTVCalculator()
    current_ltv = ltv_calc.compute_current_ltv()
    for cadence, data in current_ltv.items():
        print(f"  {cadence}:")
        print(f"    AOV: ${data['avg_order_value']}  |  "
              f"Churn: {data['monthly_churn_rate']}%/mo  |  "
              f"LTV: ${data['projected_ltv']}  |  "
              f"Lifetime: {data['expected_lifetime_months']} months")

    # 9. LTV Improvement Scenarios
    print_section("LTV IMPROVEMENT SCENARIOS")
    scenarios = ltv_calc.compute_ltv_improvement_scenarios()
    for s in scenarios:
        print(f"  {s['name']}:")
        print(f"    {s['description']}")
        if "annual_impact" in s:
            print(f"    Annual impact: ${s['annual_impact']:,.2f}")
        if "total_ltv_gain" in s:
            print(f"    Total LTV gain: ${s['total_ltv_gain']:,.2f}")
        print()

    # 10. Next Test Recommendations
    print_section("RECOMMENDED NEXT TESTS")
    rec_engine = RecommendationEngine(analyzer, scorer)
    recs = rec_engine.generate_recommendations()
    for rec in recs:
        print(f"  Priority {rec['priority']}: {rec['title']}")
        print(f"  {rec['description'][:120]}...")
        if "specific_tests" in rec:
            for t in rec["specific_tests"][:3]:
                print(f"    -> {t['change']} (risk: {t['risk']})")
        if "specific_actions" in rec:
            for a in rec["specific_actions"][:3]:
                print(f"    -> {a}")
        print()

    # 11. Anti-patterns
    print_section("ANTI-PATTERNS (DO NOT USE)")
    anti = rec_engine.generate_anti_patterns()
    for a in anti:
        print(f"  {a['pattern']}")
        print(f"    Verdict: {a['verdict']}")
        print()

    # 12. Generate report file
    print_section("GENERATING REPORT")
    generate_report(stats, sweet_spots, pricing_recs, current_ltv, scenarios, recs, anti)

    print_header("ANALYSIS COMPLETE")
    print(f"Full report saved to: {REPORTS_DIR}/analysis_report.md")
    print(f"Dashboard available at: dashboard/index.html")


def generate_report(stats, sweet_spots, pricing_recs, ltv, scenarios, recs, anti):
    """Generate markdown report."""
    os.makedirs(REPORTS_DIR, exist_ok=True)

    report = f"""# Nuora Offer Intelligence Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}
**Data Source:** {stats['total_tests']} A/B tests, {stats['total_visitors']:,} visitors, Jan 2026
**Product:** Nuora Vaginal Probiotic Gummies

---

## Executive Summary

- **Control has won all {stats['total_tests']} tests** with avg {stats['avg_control_conv']}% conversion
- Variants average {stats['avg_variant_conv']}% conversion (gap: -{stats['conv_gap']}%)
- Control maintains {stats['avg_control_sub_rate']}% subscription rate vs variant avg {stats['avg_variant_sub_rate']}%
- The current control offer is well-optimized; future gains come from micro-testing individual elements

---

## Pricing Sweet Spots

### Subscription Entry Point
- **Current:** ${sweet_spots['subscription_entry_point']['current_control']}
- **Sweet spot:** ${sweet_spots['subscription_entry_point']['sweet_spot']['low']} - ${sweet_spots['subscription_entry_point']['sweet_spot']['high']}
- {sweet_spots['subscription_entry_point']['sweet_spot']['reasoning']}

### Max Bundle Price
- **Current:** ${sweet_spots['subscription_max_bundle']['current_control']}
- **Sweet spot:** ${sweet_spots['subscription_max_bundle']['sweet_spot']['low']} - ${sweet_spots['subscription_max_bundle']['sweet_spot']['high']}

### Per-Pack Analysis
| Pack | Sub Price | Per Day | OTP Price | Sub/OTP Gap |
|------|-----------|---------|-----------|-------------|
| 1 Pack | $34.99 | $1.17 | $40.99 | 14.6% |
| 2 Pack | $25.00/pk | $0.83 | $29.00/pk | 13.8% |
| 3 Pack | $19.66/pk | $0.66 | $23.00/pk | 14.5% |

---

## Pricing Recommendations

### Keep (Proven Working)
"""
    for item in pricing_recs["keep"]:
        report += f"- {item}\n"

    report += "\n### Test (Potentially Better)\n"
    for item in pricing_recs["test"]:
        report += f"- **{item['change']}** - {item['rationale']} (Risk: {item['risk']})\n"

    report += "\n### Avoid\n"
    for item in pricing_recs["avoid"]:
        report += f"- {item}\n"

    report += "\n---\n\n## LTV by Cadence\n\n"
    report += "| Cadence | AOV | Churn/mo | LTV | Lifetime | Subscribers |\n"
    report += "|---------|-----|----------|-----|----------|-------------|\n"
    for name, data in ltv.items():
        report += (
            f"| {name} | ${data['avg_order_value']} | "
            f"{data['monthly_churn_rate']}% | ${data['projected_ltv']} | "
            f"{data['expected_lifetime_months']}mo | "
            f"{data['active_subscribers']:,} |\n"
        )

    report += "\n---\n\n## LTV Improvement Opportunities\n\n"
    for s in scenarios:
        report += f"### {s['name']}\n"
        report += f"{s['description']}\n"
        if "annual_impact" in s:
            report += f"- **Annual impact:** ${s['annual_impact']:,.2f}\n"
        if "total_ltv_gain" in s:
            report += f"- **Total LTV gain:** ${s['total_ltv_gain']:,.2f}\n"
        report += "\n"

    report += "---\n\n## Recommended Next Tests\n\n"
    for rec in recs:
        report += f"### Priority {rec['priority']}: {rec['title']}\n"
        report += f"{rec['description']}\n\n"
        if "specific_tests" in rec:
            for t in rec["specific_tests"]:
                report += f"- {t['change']} (Risk: {t['risk']})\n"
        if "specific_actions" in rec:
            for a in rec["specific_actions"]:
                report += f"- {a}\n"
        report += "\n"

    report += "---\n\n## Anti-Patterns\n\n"
    report += "These design patterns should NOT be used based on test data:\n\n"
    for a in anti:
        report += f"### {a['pattern']}\n"
        report += f"- Tested in: {a['tested_in']}\n"
        report += f"- Impact: {a['avg_conv_drop']}\n"
        report += f"- **{a['verdict']}**\n\n"

    report += f"""---

*Generated by Nuora Offer Intelligence Engine v1.0*
*Data: {stats['total_tests']} A/B tests, {stats['total_visitors']:,} total visitors*
"""

    report_path = os.path.join(REPORTS_DIR, "analysis_report.md")
    with open(report_path, "w") as f:
        f.write(report)

    print(f"  Report saved: {report_path}")


if __name__ == "__main__":
    run_analysis()
