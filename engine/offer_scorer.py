"""
Offer Scorer
Predicts performance of new offer configurations based on historical patterns.
"""

from config.settings import CONVERSION_WEIGHTS, SUBSCRIPTION_WEIGHTS, CONTROL_BASELINE


class OfferScorer:
    """Scores hypothetical offer configurations against historical data."""

    def __init__(self):
        self.conv_weights = CONVERSION_WEIGHTS
        self.sub_weights = SUBSCRIPTION_WEIGHTS
        self.baseline = CONTROL_BASELINE

    def score_offer(self, config):
        """
        Score an offer configuration.

        Args:
            config: dict with keys matching CONVERSION_WEIGHTS categories.
                Example:
                {
                    "layout": "horizontal",
                    "toggle_type": "checkbox",
                    "otp_visibility": "behind_toggle",
                    "naming": "pack_based",
                    "num_options": 3,
                    "pricing_display": "standard",
                    "savings_display": "none",
                    "product_images": False,
                    "cta_copy": "add_to_cart",
                }

        Returns:
            dict with predicted metrics and risk assessment.
        """
        conv_delta = 0.0
        sub_delta = 0.0
        breakdown = []

        for element, value in config.items():
            # Conversion impact
            conv_impact = self.conv_weights.get(element, {}).get(value, 0)
            sub_impact = self.sub_weights.get(element, {}).get(value, 0)

            conv_delta += conv_impact
            sub_delta += sub_impact

            if conv_impact != 0 or sub_impact != 0:
                breakdown.append({
                    "element": element,
                    "value": value,
                    "conv_impact": conv_impact,
                    "sub_impact": sub_impact,
                })

        predicted_conv = max(0, self.baseline["conversion_rate"] + conv_delta)
        predicted_sub = max(0, min(100, self.baseline["subscription_rate"] + sub_delta))

        # Risk assessment
        if conv_delta >= -0.5:
            risk = "low"
            risk_desc = "Close to proven control pattern"
        elif conv_delta >= -2.0:
            risk = "medium"
            risk_desc = "Some historically negative elements present"
        else:
            risk = "high"
            risk_desc = "Multiple elements that have hurt conversion in past tests"

        return {
            "predicted_conversion_rate": round(predicted_conv, 2),
            "predicted_subscription_rate": round(predicted_sub, 1),
            "conversion_delta_from_control": round(conv_delta, 2),
            "subscription_delta_from_control": round(sub_delta, 1),
            "risk_level": risk,
            "risk_description": risk_desc,
            "breakdown": breakdown,
            "confidence": self._compute_confidence(config),
        }

    def _compute_confidence(self, config):
        """
        Compute confidence level based on how similar this config
        is to previously tested configurations.
        """
        # Count how many elements match tested patterns
        tested_combos = 0
        total_elements = len(config)

        for element, value in config.items():
            if element in self.conv_weights:
                if value in self.conv_weights[element]:
                    tested_combos += 1

        ratio = tested_combos / total_elements if total_elements > 0 else 0

        if ratio >= 0.8:
            return {"level": "high", "pct": round(ratio * 100), "note": "Most elements have been tested"}
        elif ratio >= 0.5:
            return {"level": "medium", "pct": round(ratio * 100), "note": "Some elements are untested"}
        else:
            return {"level": "low", "pct": round(ratio * 100), "note": "Many untested elements - prediction unreliable"}

    def score_control(self):
        """Score the control configuration as a reference."""
        return self.score_offer({
            "layout": "horizontal",
            "toggle_type": "checkbox",
            "otp_visibility": "behind_toggle",
            "naming": "pack_based",
            "num_options": 3,
            "pricing_display": "standard",
            "savings_display": "none",
            "product_images": False,
            "cta_copy": "add_to_cart",
        })

    def compare_offers(self, config_a, config_b, name_a="Offer A", name_b="Offer B"):
        """Compare two offer configurations side by side."""
        score_a = self.score_offer(config_a)
        score_b = self.score_offer(config_b)

        return {
            name_a: score_a,
            name_b: score_b,
            "recommendation": name_a if score_a["predicted_conversion_rate"] >= score_b["predicted_conversion_rate"] else name_b,
            "conv_difference": round(
                score_a["predicted_conversion_rate"] - score_b["predicted_conversion_rate"], 2
            ),
        }

    def generate_optimal_config(self):
        """Generate the theoretically optimal configuration based on data."""
        optimal = {}
        for element, values in self.conv_weights.items():
            best_value = max(values.keys(), key=lambda v: values[v])
            optimal[element] = best_value

        return {
            "config": optimal,
            "score": self.score_offer(optimal),
            "note": "This is the control configuration - it's already the optimal based on available data.",
        }
