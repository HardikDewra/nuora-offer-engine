"""
Nuora Brand Configuration
Colors, typography, and product catalog for the offer engine.
"""

BRAND = {
    "name": "Nuora",
    "domain": "mynuora.com",
    "industry": "Women's Health / Dietary Supplements",
    "target_demo": "Women 25-50, US, mobile-first",
    "business_model": "Subscription-first DTC",
}

# Design preferences (Nikita)
DESIGN_PREFERENCES = {
    "mode": "light_only",           # NO dark mode anywhere
    "border_radius": "1px",         # Maximum 1px on all elements
    "shadows": False,               # NO box-shadow, text-shadow, or glow
    "glow_effects": False,          # No glow or radiance
    "liquid_glass": False,          # Does NOT like iOS 26 liquid glass
    "frosty_glass": True,           # Likes subtle frosted glass (backdrop-filter blur)
    "heading_font": "Americana BT Bold",
    "body_font": "Montserrat",
    "design_tool": "Paper Design (MCP server)",
}

COLORS = {
    "yellow": {
        25: "#FEFDF0",
        50: "#FEFBE8",
        100: "#FEF7C3",
        200: "#FDE272",
        400: "#FAC515",
        500: "#EAAA08",
        600: "#CA8504",
    },
    "brown": {
        800: "#854A0E",
        900: "#713B12",
        950: "#542C0D",
    },
    "rose": {
        "primary": "#9B083E",
        "dark": "#4A0420",
        "pdp": "#7B1C3A",
    },
    "medical_blue": {
        "primary": "#1565c0",
        "light": "#e3f2fd",
    },
}

TYPOGRAPHY = {
    "heading": {
        "family": "Americana BT",
        "fallback": "Georgia, 'Times New Roman', serif",
        "weight": 700,
    },
    "body": {
        "family": "Montserrat",
        "fallback": "-apple-system, 'Helvetica Neue', Arial, sans-serif",
        "weights": [400, 500, 600, 700],
    },
}

PRODUCTS = {
    "vaginal_probiotic_gummies": {
        "name": "Nuora Vaginal Probiotic",
        "handle": "feminine-balance-gummies-1",
        "url": "https://mynuora.com/products/feminine-balance-gummies-1",
        "type": "gummies",
        "servings_per_pack": 30,
        "gummies_per_pack": 60,
        "flavor": "Pineapple",
        "color_scheme": "yellow",  # uses yellow/brown brand colors
        "pricing": {
            "one_time": {
                "1_pack": {"price": 40.99, "compare": 57.99},
                "2_pack": {"price": 57.99, "compare": 115.98},
                "3_pack": {"price": 68.99, "compare": 173.97},
            },
            "subscription": {
                "1_pack": {"price": 34.99, "frequency": "monthly"},
                "2_pack": {"price": 49.99, "frequency": "every 2 months"},
                "3_pack": {"price": 58.99, "frequency": "every 3 months"},
            },
        },
        "reviews": {"count": 11847, "rating": 4.57},
        "subscribers": 65212,
    },
    "gut_ritual": {
        "name": "Nuora Gut Ritual",
        "handle": "gut-capsule",
        "url": "https://mynuora.com/products/gut-capsule",
        "type": "capsules",
        "color_scheme": "rose",  # uses rose/pink brand colors
        "pricing": {
            "one_time": {
                "1_bottle": {"price": 59.00},
                "2_bottles": {"price": 69.00},
                "3_bottles": {"price": 79.00},
            },
        },
        "reviews": {"count": 11847, "rating": 4.57},
    },
}

# Testing configuration
TESTING = {
    "platform": "Elevate A/B (elevateab.app)",
    "split_ratio": "50/50",
    "device_targeting": "Mobile only",
    "country_targeting": "United States only",
    "visitor_type": "All Visitors",
    "min_visitors": 2000,
    "min_duration_hours": 12,
    "primary_metrics": [
        "conversion_rate",
        "revenue",
        "revenue_per_visitor",
        "orders",
        "aov",
    ],
    "secondary_metrics": [
        "add_to_cart_rate",
        "reached_checkout_rate",
        "subscription_rate",
        "session_duration",
    ],
    "traffic_sources": {
        "facebook": 0.67,
        "instagram": 0.14,
        "direct": 0.10,
        "google": 0.08,
        "other": 0.01,
    },
}

# Subscription business metrics
SUBSCRIPTION = {
    "active_subscribers": 65212,
    "mrr": 1785570.83,
    "annualized_revenue": 21426849.91,
    "cadence_distribution": {
        "monthly_1pack": {"pct": 34.8, "subscribers": 22690, "avg_order": 39.33},
        "bimonthly_2pack": {"pct": 20.0, "subscribers": 13048, "avg_order": 50.06},
        "quarterly_3pack": {"pct": 45.2, "subscribers": 29474, "avg_order": 58.64},
    },
    "churn": {
        "overall": 35.2,
        "30_day": {
            "monthly": 19.6,
            "bimonthly": 20.7,
            "quarterly": 17.0,
        },
    },
    "cancel_reasons": {
        "subscribed_by_accident": 33.2,
        "unknown": 27.9,
        "too_much_product": 16.6,
        "too_expensive": 13.3,
        "product_issue": 4.1,
        "shipping_issue": 3.2,
    },
}
