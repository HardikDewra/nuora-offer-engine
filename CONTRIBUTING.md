# Contributing to Nuora Offer Engine

This guide is for the Nuora CRO team. Follow these steps to add new test data, run analysis, and contribute improvements.

## Getting Started

```bash
# Clone the repo
git clone https://github.com/HardikDewra/nuora-offer-engine.git
cd nuora-offer-engine

# Install Python dependencies (only needed for scraper)
pip install -r requirements.txt

# Run the analysis
python run_analysis.py

# Run with live product data scrape
python run_analysis.py --scrape
```

## Adding New Test Results

When you run a new A/B test, add the results as a JSON file:

1. Copy an existing test file from `data/test_results/` as a template
2. Create a new file named `{style}_v{version}.json` (e.g., `ankhway_v3.json`)
3. Fill in all metrics from Elevate A/B
4. Add key learnings from the test

### Required Fields

```json
{
  "name": "Style VX",
  "style": "Style Name",
  "version": "VX",
  "url": "test URL",
  "test_date": "YYYY-MM-DD",
  "duration_hours": 12,
  "result": "control_wins or variant_wins",
  "design": {
    "layout": "horizontal or vertical",
    "toggle_type": "checkbox, side_by_side, none, or separate_card",
    "otp_visibility": "behind_toggle, separate_card, equal_weight, or not_available",
    "naming": "pack_based, time_based, creative, or bogo",
    "num_options": 2 or 3,
    "pricing_display": "standard or rounded",
    "savings_display": "none, dollar, or percent",
    "product_images": true or false,
    "cta_copy": "add_to_cart, buy_now, or get_started"
  },
  "metrics": {
    "control": { ... },
    "variant": { ... }
  },
  "key_learnings": ["..."]
}
```

### After Adding Data

```bash
# Run analysis to verify data loads correctly
python run_analysis.py

# Commit and push
git add data/test_results/your_new_test.json
git commit -m "Add [test name] results"
git push
```

## Viewing the Dashboard

Open `dashboard/index.html` in any browser. If using GitHub Pages:
https://hardikdewra.github.io/nuora-offer-engine/dashboard/

## Node.js Offer Scoring API

For quick offer scoring without Python:

```bash
cd tools
npm install
node offer_api.js
# API runs on http://localhost:3000
```

Then score an offer:
```bash
curl http://localhost:3000/score -X POST -H "Content-Type: application/json" -d '{
  "layout": "horizontal",
  "toggle_type": "checkbox",
  "otp_visibility": "behind_toggle",
  "naming": "pack_based",
  "num_options": 3,
  "pricing_display": "standard",
  "savings_display": "none",
  "product_images": false,
  "cta_copy": "add_to_cart"
}'
```

## Design Guidelines

Before creating any new offer design, read:
- `docs/brand_preferences.md` - Nikita's design preferences
- `docs/paper_design_context.md` - Context for Paper Design tool
- `docs/element_impact.md` - What design elements affect performance

## Branch Naming

- `test/style-name-vX` for new test data
- `feature/description` for new features
- `fix/description` for bug fixes

## Code Review

All changes should be submitted as pull requests for review. The analysis engine re-runs automatically via GitHub Actions on every push.
