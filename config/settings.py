"""
Engine settings and configuration.
"""

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
TEST_RESULTS_DIR = os.path.join(DATA_DIR, "test_results")
PRODUCTS_DIR = os.path.join(DATA_DIR, "products")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

# Scoring model weights - derived from 8 A/B tests
# Each weight represents the avg conversion rate impact when that element is used
CONVERSION_WEIGHTS = {
    "layout": {
        "horizontal": 0.0,       # Control baseline
        "vertical": -1.8,        # Avg -1.8% across vertical layouts
    },
    "toggle_type": {
        "checkbox": 0.0,          # Control baseline - pre-selected subscription
        "side_by_side": -2.2,     # Equal weight buttons - Omre style
        "none": -1.7,             # No toggle, subscription only - Ryze style
        "separate_card": -1.4,    # OTP as separate card - Ankhway style
    },
    "otp_visibility": {
        "behind_toggle": 0.0,     # Control - hidden behind checkbox
        "separate_card": -1.4,    # Visible as third card
        "equal_weight": -2.0,     # Side-by-side with subscription
        "not_available": -1.0,    # No OTP option at all
    },
    "naming": {
        "pack_based": 0.0,        # "1 Pack / 2 Packs / 3 Packs"
        "time_based": -0.5,       # "30-day / 90-day supply"
        "creative": -0.4,         # "Starter Kit / Ritual Set"
        "bogo": -1.7,             # "Buy 2, Get 1 FREE"
    },
    "num_options": {
        3: 0.0,                   # Three pack choices
        2: -0.5,                  # Two pack choices only
    },
    "pricing_display": {
        "standard": 0.0,          # $X.99 format
        "rounded": -0.1,          # Clean round numbers
    },
    "savings_display": {
        "none": 0.0,              # No savings shown on cards
        "dollar": -0.3,           # "Save $X"
        "percent": -0.3,          # "Save X%"
    },
    "product_images": {
        False: 0.0,
        True: 0.0,                # No measurable impact
    },
    "cta_copy": {
        "add_to_cart": 0.0,
        "buy_now": -0.1,
        "get_started": -0.1,
    },
}

# Subscription rate weights - how elements affect subscription capture
SUBSCRIPTION_WEIGHTS = {
    "layout": {
        "horizontal": 0,
        "vertical": -8,
    },
    "toggle_type": {
        "checkbox": 0,
        "side_by_side": -25,
        "none": 5,
        "separate_card": -15,
    },
    "otp_visibility": {
        "behind_toggle": 0,
        "separate_card": -15,
        "equal_weight": -20,
        "not_available": 17,
    },
    "naming": {
        "pack_based": 0,
        "time_based": -3,
        "creative": 0,
        "bogo": -5,
    },
    "num_options": {
        3: 0,
        2: -2,
    },
    "pricing_display": {
        "standard": 0,
        "rounded": 0,
    },
    "savings_display": {
        "none": 0,
        "dollar": 0,
        "percent": 0,
    },
    "product_images": {
        False: 0,
        True: 0,
    },
    "cta_copy": {
        "add_to_cart": 0,
        "buy_now": 0,
        "get_started": 0,
    },
}

# Control baseline metrics (averaged across all 8 tests)
CONTROL_BASELINE = {
    "conversion_rate": 7.65,
    "subscription_rate": 83,
    "aov": 53.38,
    "revenue_per_visitor": 4.02,
    "add_to_cart_rate": 15.0,
    "session_duration_sec": 43,
}
