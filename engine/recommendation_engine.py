"""
Recommendation Engine
Generates prioritized test recommendations based on data gaps
and historical patterns.
"""


class RecommendationEngine:
    """Generates next-test recommendations based on analysis."""

    def __init__(self, analyzer, scorer):
        self.analyzer = analyzer
        self.scorer = scorer

    def get_untested_combinations(self):
        """Identify element combinations that haven't been tested yet."""
        tested = set()
        for test in self.analyzer.get_all_tests():
            design = test["design"]
            combo = (
                design.get("layout", ""),
                design.get("toggle_type", ""),
                design.get("naming", ""),
            )
            tested.add(combo)

        # Key untested combinations
        all_layouts = ["horizontal", "vertical"]
        all_toggles = ["checkbox", "side_by_side", "none", "separate_card"]
        all_namings = ["pack_based", "time_based", "creative", "bogo"]

        untested = []
        for layout in all_layouts:
            for toggle in all_toggles:
                for naming in all_namings:
                    combo = (layout, toggle, naming)
                    if combo not in tested:
                        # Score the hypothetical
                        config = {
                            "layout": layout,
                            "toggle_type": toggle,
                            "naming": naming,
                            "num_options": 3,
                            "otp_visibility": "behind_toggle" if toggle == "checkbox" else "equal_weight",
                            "pricing_display": "standard",
                            "savings_display": "none",
                            "product_images": False,
                            "cta_copy": "add_to_cart",
                        }
                        score = self.scorer.score_offer(config)
                        untested.append({
                            "layout": layout,
                            "toggle": toggle,
                            "naming": naming,
                            "predicted_conv": score["predicted_conversion_rate"],
                            "risk": score["risk_level"],
                        })

        return sorted(untested, key=lambda x: x["predicted_conv"], reverse=True)

    def generate_recommendations(self):
        """Generate prioritized test recommendations."""
        recommendations = []

        # Priority 1: Single-element changes on control
        recommendations.append({
            "priority": 1,
            "title": "Test individual elements on the winning control",
            "description": (
                "All 7 variants changed 5+ elements simultaneously. "
                "Change ONE element at a time on the control to isolate "
                "what actually drives performance."
            ),
            "specific_tests": [
                {
                    "change": "CTA: 'ADD TO CART' -> 'GET STARTED'",
                    "elements_changed": 1,
                    "predicted_impact": "-0.1%",
                    "risk": "very low",
                },
                {
                    "change": "Add 'Save $X' badges to pack cards",
                    "elements_changed": 1,
                    "predicted_impact": "-0.3%",
                    "risk": "low",
                },
                {
                    "change": "Add per-day price display ($0.66/day)",
                    "elements_changed": 1,
                    "predicted_impact": "Unknown - untested in isolation",
                    "risk": "low",
                },
                {
                    "change": "Add 'Most Popular' badge to 3-pack",
                    "elements_changed": 1,
                    "predicted_impact": "Unknown - untested in isolation",
                    "risk": "very low",
                },
            ],
        })

        # Priority 2: Pricing micro-tests
        recommendations.append({
            "priority": 2,
            "title": "Test pricing micro-adjustments on control",
            "description": (
                "The control pricing hasn't been A/B tested in isolation. "
                "Small pricing changes can have outsized revenue impact."
            ),
            "specific_tests": [
                {
                    "change": "3-pack sub: $58.99 -> $54.99 (keep everything else)",
                    "rationale": "Under $55 psychological threshold",
                    "risk": "low",
                },
                {
                    "change": "1-pack OTP: $40.99 -> $44.99 (widen sub/OTP gap)",
                    "rationale": "Push more buyers toward subscription",
                    "risk": "low",
                },
                {
                    "change": "Compare-at: $57.99 -> $64.99 (increase perceived savings)",
                    "rationale": "Stronger anchor price may increase urgency",
                    "risk": "medium",
                },
            ],
        })

        # Priority 3: Urgency & social proof
        recommendations.append({
            "priority": 3,
            "title": "Test urgency and social proof placement",
            "description": (
                "Control has countdown in header only. Moving urgency "
                "closer to the CTA may increase conversion."
            ),
            "specific_tests": [
                {
                    "change": "Move countdown timer into offer module (above CTA)",
                    "rationale": "Proximity to decision point increases urgency",
                    "risk": "low",
                },
                {
                    "change": "Add '11,847 reviews' badge near offer section",
                    "rationale": "Social proof at decision point",
                    "risk": "very low",
                },
                {
                    "change": "Add 'X people viewing this' live counter",
                    "rationale": "FOMO trigger",
                    "risk": "medium",
                },
            ],
        })

        # Priority 4: Churn reduction (not A/B test, but highest ROI)
        recommendations.append({
            "priority": 4,
            "title": "Fix accidental subscription issue (highest ROI opportunity)",
            "description": (
                "33.2% of cancellations cite 'I subscribed by accident'. "
                "This is 12,191 lost subscribers. Fixing the checkout flow "
                "is worth more than any A/B test on the offer module."
            ),
            "specific_actions": [
                "Add subscription confirmation step before checkout",
                "Make subscription terms more visible in cart",
                "Add 'You are subscribing to...' confirmation modal",
                "Test subscription checkbox copy for clarity",
            ],
            "estimated_impact": (
                "Reducing accidental subs by 50% would retain ~6,000 "
                "additional subscribers = ~$117k/month additional MRR"
            ),
        })

        return recommendations

    def generate_anti_patterns(self):
        """Elements that should NOT be used based on data."""
        return [
            {
                "pattern": "Vertical stacked cards",
                "tested_in": "7/7 variants",
                "avg_conv_drop": "-1.8%",
                "verdict": "NEVER use - consistently underperforms horizontal",
            },
            {
                "pattern": "Side-by-side Sub/OTP toggle",
                "tested_in": "Omre V1, Omre V2",
                "avg_conv_drop": "-2.2%",
                "avg_sub_drop": "-25%",
                "verdict": "NEVER use - destroys subscription rate",
            },
            {
                "pattern": "OTP as visible third card",
                "tested_in": "Ankhway V1, Ankhway V2",
                "avg_conv_drop": "-1.4%",
                "avg_sub_drop": "-21%",
                "verdict": "AVOID - makes OTP too accessible",
            },
            {
                "pattern": "Subscription-only (no OTP option)",
                "tested_in": "Ryze V1, Ryze V2",
                "avg_conv_drop": "-1.7%",
                "verdict": "AVOID - eliminates OTP but loses conversion",
            },
            {
                "pattern": "BOGO naming",
                "tested_in": "Resilia V1",
                "avg_conv_drop": "-1.7%",
                "verdict": "AVOID - creates commitment perception that deters buyers",
            },
        ]
