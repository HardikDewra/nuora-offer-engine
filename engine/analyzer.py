"""
Core A/B Test Analyzer
Loads all test results and computes cross-test patterns and insights.
"""

import json
import os
from config.settings import TEST_RESULTS_DIR, CONTROL_BASELINE


class OfferAnalyzer:
    """Analyzes all historical A/B test data to extract patterns."""

    def __init__(self):
        self.tests = []
        self.control = None
        self._load_data()

    def _load_data(self):
        """Load all test result JSON files."""
        for filename in sorted(os.listdir(TEST_RESULTS_DIR)):
            if not filename.endswith(".json"):
                continue
            filepath = os.path.join(TEST_RESULTS_DIR, filename)
            with open(filepath) as f:
                data = json.load(f)
            if filename == "control.json":
                self.control = data
            else:
                self.tests.append(data)

    def get_all_tests(self):
        """Return all variant tests (excluding control reference)."""
        return self.tests

    def compute_summary_stats(self):
        """Compute aggregate stats across all tests."""
        total_visitors = 0
        control_conv_rates = []
        variant_conv_rates = []
        control_sub_rates = []
        variant_sub_rates = []
        control_aovs = []
        variant_aovs = []

        for test in self.tests:
            m_ctrl = test["metrics"]["control"]
            m_var = test["metrics"]["variant"]

            total_visitors += m_ctrl["visitors"] + m_var["visitors"]
            control_conv_rates.append(m_ctrl["conversion_rate"])
            variant_conv_rates.append(m_var["conversion_rate"])
            control_sub_rates.append(m_ctrl["subscription_rate"])
            variant_sub_rates.append(m_var["subscription_rate"])
            control_aovs.append(m_ctrl["aov"])
            variant_aovs.append(m_var["aov"])

        n = len(self.tests)
        avg = lambda lst: sum(lst) / len(lst) if lst else 0

        return {
            "total_tests": n,
            "total_visitors": total_visitors,
            "control_wins": n,  # control won all 7 tests
            "avg_control_conv": round(avg(control_conv_rates), 2),
            "avg_variant_conv": round(avg(variant_conv_rates), 2),
            "conv_gap": round(avg(control_conv_rates) - avg(variant_conv_rates), 2),
            "avg_control_sub_rate": round(avg(control_sub_rates), 1),
            "avg_variant_sub_rate": round(avg(variant_sub_rates), 1),
            "avg_control_aov": round(avg(control_aovs), 2),
            "avg_variant_aov": round(avg(variant_aovs), 2),
            "control_conv_range": {
                "min": min(control_conv_rates),
                "max": max(control_conv_rates),
            },
            "variant_conv_range": {
                "min": min(variant_conv_rates),
                "max": max(variant_conv_rates),
            },
        }

    def compute_element_impact(self):
        """
        Analyze which design elements correlate with conversion changes.
        Returns a dict mapping element -> value -> avg impact.
        """
        element_impacts = {}

        for test in self.tests:
            design = test["design"]
            conv_delta = (
                test["metrics"]["variant"]["conversion_rate"]
                - test["metrics"]["control"]["conversion_rate"]
            )
            sub_delta = (
                test["metrics"]["variant"]["subscription_rate"]
                - test["metrics"]["control"]["subscription_rate"]
            )

            for element, value in design.items():
                if element in (
                    "bundle_names", "badges", "dynamic_pricing",
                    "subscription_info_location", "dynamic_cta", "urgency",
                ):
                    continue  # skip non-comparable elements

                key = element
                val = str(value)

                if key not in element_impacts:
                    element_impacts[key] = {}
                if val not in element_impacts[key]:
                    element_impacts[key][val] = {
                        "conv_deltas": [],
                        "sub_deltas": [],
                        "tests": [],
                    }

                element_impacts[key][val]["conv_deltas"].append(conv_delta)
                element_impacts[key][val]["sub_deltas"].append(sub_delta)
                element_impacts[key][val]["tests"].append(test["name"])

        # Compute averages
        results = {}
        for element, values in element_impacts.items():
            results[element] = {}
            for value, data in values.items():
                n = len(data["conv_deltas"])
                results[element][value] = {
                    "avg_conv_impact": round(
                        sum(data["conv_deltas"]) / n, 2
                    ),
                    "avg_sub_impact": round(
                        sum(data["sub_deltas"]) / n, 1
                    ),
                    "sample_size": n,
                    "tests": data["tests"],
                }

        return results

    def compute_pricing_analysis(self):
        """Analyze pricing patterns across all tests and control."""
        pricing_data = []

        # Control pricing
        if self.control:
            ctrl_pricing = self.control["pricing"]
            for pack_type in ["one_time", "subscription"]:
                for pack_size, details in ctrl_pricing.get(pack_type, {}).items():
                    pricing_data.append({
                        "source": "control",
                        "type": pack_type,
                        "pack": pack_size,
                        "price": details["price"],
                        "per_pack": details.get("per_pack", details["price"]),
                    })

        # Variant pricing
        for test in self.tests:
            for pack_type in ["subscription", "one_time"]:
                for pack_name, details in test.get("pricing", {}).get(pack_type, {}).items():
                    pricing_data.append({
                        "source": test["name"],
                        "type": pack_type,
                        "pack": pack_name,
                        "price": details["price"],
                        "per_pack": details.get("per_pack", details["price"]),
                    })

        return pricing_data

    def compute_funnel_analysis(self):
        """Analyze conversion funnel across all tests."""
        funnels = {"control": [], "variant": []}

        for test in self.tests:
            for group in ["control", "variant"]:
                m = test["metrics"][group]
                funnels[group].append({
                    "test": test["name"],
                    "atc": m.get("add_to_cart_rate", 0),
                    "checkout": m.get("reached_checkout_rate", 0),
                    "purchase": m["conversion_rate"],
                    "session_sec": m.get("session_duration_sec", 0),
                })

        # Averages
        avg_funnel = {}
        for group in ["control", "variant"]:
            data = funnels[group]
            n = len(data)
            avg_funnel[group] = {
                "avg_atc": round(sum(d["atc"] for d in data) / n, 1),
                "avg_checkout": round(sum(d["checkout"] for d in data) / n, 1),
                "avg_purchase": round(sum(d["purchase"] for d in data) / n, 2),
                "avg_session": round(sum(d["session_sec"] for d in data) / n, 0),
            }

        return {"per_test": funnels, "averages": avg_funnel}

    def identify_winning_patterns(self):
        """Identify which specific patterns the control uses that keep winning."""
        return {
            "layout": "horizontal",
            "toggle": "checkbox (dashed border, pre-selected subscription)",
            "otp_handling": "Behind toggle - less prominent, not a separate card",
            "naming": "Pack-based (1 Pack / 2 Packs / 3 Packs)",
            "options": "3 quantity choices",
            "pricing": "Standard $X.99 format",
            "savings": "No savings badges on cards",
            "images": "No product images on offer cards",
            "cta": "ADD TO CART (static text)",
            "default": "3-pack subscription pre-selected",
            "subscription_copy": "Save More With Automatic Refills",
        }

    def identify_losing_patterns(self):
        """Patterns that consistently hurt performance."""
        return [
            {
                "pattern": "Vertical stacked cards",
                "avg_impact": "-1.8% conversion",
                "tested_in": "All 7 variants",
                "severity": "high",
            },
            {
                "pattern": "Side-by-side Sub/OTP toggle",
                "avg_impact": "-2.2% conversion, -25% subscription rate",
                "tested_in": "Omre V1, Omre V2",
                "severity": "critical",
            },
            {
                "pattern": "OTP as visible separate card",
                "avg_impact": "-1.4% conversion, -21% subscription rate",
                "tested_in": "Ankhway V1, Ankhway V2",
                "severity": "high",
            },
            {
                "pattern": "Subscription-only model (no OTP)",
                "avg_impact": "-1.7% conversion (eliminates OTP entirely)",
                "tested_in": "Ryze V1, Ryze V2",
                "severity": "medium",
            },
            {
                "pattern": "BOGO naming (Buy X Get Y Free)",
                "avg_impact": "-1.7% conversion, eliminates OTP orders entirely",
                "tested_in": "Resilia V1",
                "severity": "high",
            },
            {
                "pattern": "Time-based naming (30-day/90-day supply)",
                "avg_impact": "-0.5% conversion",
                "tested_in": "Ankhway V1/V2, Omre V1/V2",
                "severity": "low",
            },
        ]
