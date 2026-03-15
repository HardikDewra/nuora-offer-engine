# Nuora Offer Intelligence Engine

🔴 **Live Dashboard:** https://hardikdewra.github.io/nuora-offer-engine/dashboard/

⚫ **Repository:** https://github.com/HardikDewra/nuora-offer-engine

A data-driven offer optimization system for Nuora's PDP (Product Detail Page). Analyzes historical A/B test data to identify winning patterns, predict new offer performance, find pricing sweet spots, and generate recommendations for the next round of tests.

## What This Does

- **Analyzes 7 A/B tests** across 4 offer styles (Ankhway, Ryze, Omre, Resilia) with V1/V2 iterations
- **Scores new offer configurations** against historical patterns to predict conversion rate and subscription capture
- **Finds pricing sweet spots** based on how different price points correlate with conversion, AOV, and LTV
- **Generates next-test recommendations** prioritized by expected impact and risk
- **Calculates LTV projections** across subscription cadences (monthly, bimonthly, quarterly)
- **Scrapes live product data** from mynuora.com for real-time pricing analysis

## Quick Start

```bash
# Install dependencies (only needed for scraper)
pip install -r requirements.txt

# Run the full analysis
python run_analysis.py

# Run with live product data scrape
python run_analysis.py --scrape
```

The analysis outputs to terminal and generates a report at `reports/analysis_report.md`.

## Project Structure

```
nuora-offer-engine/
├── run_analysis.py          # Main entry point - runs full analysis pipeline
├── requirements.txt         # Python dependencies
│
├── engine/                  # Core analysis modules
│   ├── analyzer.py          # Cross-test pattern analysis
│   ├── pricing_optimizer.py # Pricing sweet spot finder
│   ├── offer_scorer.py      # Offer configuration scoring algorithm
│   ├── recommendation_engine.py  # Next-test recommendation generator
│   └── ltv_calculator.py    # LTV/AOV projection calculator
│
├── scrapers/
│   └── nuora_scraper.py     # Live product data scraper (mynuora.com)
│
├── config/
│   ├── brand.py             # Brand colors, typography, product catalog
│   └── settings.py          # Scoring weights, control baseline metrics
│
├── data/
│   ├── test_results/        # Structured A/B test result files (JSON)
│   │   ├── control.json     # Current winning control offer
│   │   ├── resilia_v1.json  # Resilia-style test (Jan 9)
│   │   ├── ankhway_v1.json  # Ankhway-style test (Jan 17)
│   │   ├── ankhway_v2.json  # Ankhway V2 - rounded pricing (Jan 30)
│   │   ├── ryze_v1.json     # Ryze-style test (Jan 21)
│   │   ├── ryze_v2.json     # Ryze V2 - added product images (Jan 30)
│   │   ├── omre_v1.json     # Omre-style test (Jan 21)
│   │   └── omre_v2.json     # Omre V2 - rounded pricing (Jan 30)
│   └── products/            # Product data (scraped + reference)
│       ├── vaginal_probiotic.json
│       └── gut_ritual.json
│
├── dashboard/
│   └── index.html           # Interactive visual dashboard (Chart.js)
│
├── docs/
│   ├── methodology.md       # A/B testing methodology and standards
│   ├── testing_guidelines.md # What to test next and how
│   └── element_impact.md    # Design element impact analysis
│
└── reports/                 # Auto-generated analysis reports
    └── analysis_report.md   # Full analysis output
```

## Key Findings (from 7 tests, 16,335 visitors)

### Control Always Wins
The current control offer has won all 7 A/B tests. It uses:
- Horizontal card layout with radio buttons
- Checkbox toggle (pre-selected subscription)
- Pack-based naming (1 Pack / 2 Packs / 3 Packs)
- OTP hidden behind toggle
- Standard $X.99 pricing

### What Kills Conversion
| Pattern | Avg Impact | Tested In |
|---------|-----------|-----------|
| Side-by-side Sub/OTP toggle | -2.2% conv, -25% sub rate | Omre V1/V2 |
| Vertical stacked cards | -1.8% conversion | All 7 variants |
| BOGO naming | -1.7% conv, eliminates OTP | Resilia V1 |
| Subscription-only | -1.7% conversion | Ryze V1/V2 |
| OTP as visible card | -1.4% conv, -21% sub rate | Ankhway V1/V2 |

### Pricing Sweet Spots
- **Subscription entry:** $34-40 range (control's $34.99 is proven)
- **Max bundle:** Keep under $60 (control's $58.99 for 3-pack)
- **OTP gap:** 14-15% above subscription price
- **Per-day anchor:** 3-pack at $0.66/day is strong

### Biggest Revenue Opportunity
33.2% of subscription cancellations cite "I subscribed by accident". Fixing checkout UX could retain ~6,000 additional subscribers = ~$117k/month in recovered MRR. This is higher ROI than any offer test.

## Scoring Algorithm

The offer scorer uses element-level weights derived from test data:

```
Predicted Conversion = Control Baseline (7.65%) + Sum of Element Impacts
```

Each design element (layout, toggle type, naming, etc.) has a weight based on its observed impact. The scorer also predicts subscription rate and provides a risk assessment.

Example:
```python
from engine.offer_scorer import OfferScorer

scorer = OfferScorer()
result = scorer.score_offer({
    "layout": "horizontal",
    "toggle_type": "checkbox",
    "otp_visibility": "behind_toggle",
    "naming": "pack_based",
    "num_options": 3,
    "pricing_display": "standard",
    "savings_display": "dollar",   # Adding savings badges
    "product_images": False,
    "cta_copy": "add_to_cart",
})
# result: predicted_conversion_rate: 7.35%, risk: low
```

## Dashboard

Open `dashboard/index.html` in a browser for an interactive visual dashboard with:
- Conversion rate comparison charts
- Revenue per visitor analysis
- Subscription rate breakdown
- Element impact matrix
- Interactive offer configurator with live scoring

**Live dashboard:** https://hardikdewra.github.io/nuora-offer-engine/dashboard/

## Node.js Offer Scoring API

For quick scoring without Python, use the Express API:

```bash
cd tools && npm install && node offer_api.js
```

Endpoints:
- `POST /score` - Score a single offer configuration
- `POST /compare` - Compare two offers side by side
- `GET /control` - Get winning control config and score
- `GET /tests` - List all historical test results
- `GET /sweet-spots` - Pricing sweet spot analysis

## CI/CD

GitHub Actions automatically re-runs analysis and updates the report when new test data is pushed to `data/test_results/`.

## Related Nuora Repositories

| Repository | Description |
|-----------|-------------|
| [nuora-offer-engine](https://github.com/HardikDewra/nuora-offer-engine) | This repo - offer optimization engine |
| [nuora-subscription-analysis](https://github.com/HardikDewra/nuora-subscription-analysis) | Subscription revenue & retention analysis |
| [Nuora-New-Offer-Testing](https://github.com/HardikDewra/Nuora-New-Offer-Testing) | Offer testing methodology and A/B test reports |
| [Nuora-Cursor-Project](https://github.com/HardikDewra/Nuora-Cursor-Project) | Landing pages, listicles, and PDP builds |
| [nuora-quiz-funnels](https://github.com/HardikDewra/nuora-quiz-funnels) | Quiz funnel implementation |

## Design Preferences

See `docs/brand_preferences.md` for Nikita's design guidelines:
- Light mode only, no dark mode
- Americana BT Bold headings, Montserrat body
- 1px border-radius, no shadows, no glow
- Frosty glass OK, liquid glass NOT OK
- Brand colors: Yellow (gummies), Rose (gut ritual), Blue (medical)

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for how to add new test data and use the tools.

---

Built for Nuora CRO optimization. Data from Elevate A/B tests, Jan 2026.
