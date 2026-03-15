"""
LTV Calculator
Projects customer lifetime value based on subscription cadence,
churn rates, and AOV data.
"""

from config.brand import SUBSCRIPTION, PRODUCTS


class LTVCalculator:
    """Calculates and projects LTV across different subscription scenarios."""

    def __init__(self):
        self.sub_data = SUBSCRIPTION
        self.product_data = PRODUCTS["vaginal_probiotic_gummies"]

    def compute_current_ltv(self):
        """Calculate current LTV by subscription cadence."""
        churn = self.sub_data["churn"]["30_day"]
        cadences = self.sub_data["cadence_distribution"]

        results = {}
        for name, data in cadences.items():
            churn_key = name.split("_")[0]
            monthly_churn = churn.get(churn_key, 20.0) / 100
            avg_order = data["avg_order"]

            # Determine billing frequency
            if "monthly" in name:
                months_between_bills = 1
            elif "bimonthly" in name:
                months_between_bills = 2
            else:
                months_between_bills = 3

            # Expected lifetime in months (1 / monthly churn rate)
            expected_lifetime_months = 1 / monthly_churn if monthly_churn > 0 else 12

            # Number of billing cycles in that lifetime
            billing_cycles = expected_lifetime_months / months_between_bills

            # LTV = avg order * billing cycles
            ltv = avg_order * billing_cycles

            # Monthly revenue per subscriber
            mrr_per_sub = avg_order / months_between_bills

            results[name] = {
                "avg_order_value": avg_order,
                "months_between_bills": months_between_bills,
                "monthly_churn_rate": round(monthly_churn * 100, 1),
                "expected_lifetime_months": round(expected_lifetime_months, 1),
                "expected_billing_cycles": round(billing_cycles, 1),
                "projected_ltv": round(ltv, 2),
                "mrr_per_subscriber": round(mrr_per_sub, 2),
                "active_subscribers": data["subscribers"],
                "total_projected_revenue": round(ltv * data["subscribers"], 2),
            }

        return results

    def compute_ltv_improvement_scenarios(self):
        """Model how different improvements would affect LTV."""
        current = self.compute_current_ltv()
        base_mrr = self.sub_data["mrr"]

        scenarios = []

        # Scenario 1: Reduce churn by fixing accidental subscription
        accidental_pct = self.sub_data["cancel_reasons"]["subscribed_by_accident"] / 100
        if_fixed = base_mrr * (1 + accidental_pct * 0.5)  # recover 50% of accidental cancels
        scenarios.append({
            "name": "Fix accidental subscription checkout UX",
            "description": "Reduce 'subscribed by accident' cancels by 50%",
            "current_mrr": round(base_mrr, 2),
            "projected_mrr": round(if_fixed, 2),
            "mrr_increase": round(if_fixed - base_mrr, 2),
            "mrr_increase_pct": round((if_fixed - base_mrr) / base_mrr * 100, 1),
            "annual_impact": round((if_fixed - base_mrr) * 12, 2),
        })

        # Scenario 2: Shift more customers to quarterly billing
        # If we move 10% of monthly subs to quarterly
        monthly_subs = current["monthly_1pack"]["active_subscribers"]
        quarterly_ltv = current["quarterly_3pack"]["projected_ltv"]
        monthly_ltv = current["monthly_1pack"]["projected_ltv"]
        shifted = monthly_subs * 0.10
        ltv_gain_per_sub = quarterly_ltv - monthly_ltv
        scenarios.append({
            "name": "Shift 10% of monthly subs to quarterly",
            "description": "Push more customers toward 3-pack quarterly subscription",
            "subscribers_shifted": round(shifted),
            "ltv_gain_per_subscriber": round(ltv_gain_per_sub, 2),
            "total_ltv_gain": round(shifted * ltv_gain_per_sub, 2),
        })

        # Scenario 3: Increase AOV by $5 through upsell
        total_subs = self.sub_data["active_subscribers"]
        scenarios.append({
            "name": "Increase AOV by $5 through bundle upsell",
            "description": "Add complementary product suggestion at checkout",
            "current_avg_aov": round(
                sum(c["avg_order"] for c in self.sub_data["cadence_distribution"].values()) / 3, 2
            ),
            "target_aov_increase": 5.00,
            "monthly_revenue_increase": round(total_subs * 5 / 3, 2),
            "annual_impact": round(total_subs * 5 / 3 * 12, 2),
        })

        return scenarios

    def compute_revenue_projection(self, months=6):
        """Project revenue for next N months from existing subscriber base."""
        current = self.compute_current_ltv()
        projection = []

        for month in range(1, months + 1):
            month_revenue = 0
            month_detail = {}

            for cadence_name, data in current.items():
                churn_rate = data["monthly_churn_rate"] / 100
                survivors = data["active_subscribers"] * ((1 - churn_rate) ** month)
                billing_freq = data["months_between_bills"]

                # Only bills on billing months
                if month % billing_freq == 0:
                    revenue = survivors * data["avg_order_value"]
                else:
                    revenue = 0

                # Monthly cadence bills every month
                if billing_freq == 1:
                    revenue = survivors * data["avg_order_value"]

                month_detail[cadence_name] = {
                    "surviving_subscribers": round(survivors),
                    "revenue": round(revenue, 2),
                }
                month_revenue += revenue

            projection.append({
                "month": month,
                "total_revenue": round(month_revenue, 2),
                "detail": month_detail,
            })

        return projection
