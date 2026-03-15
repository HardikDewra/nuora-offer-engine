# Paper Design Context for Nuora Offers

This file provides context for designing new Nuora PDP offers using the Paper Design MCP server.

## Current Winning Design (Control)

The control offer has won all 7 A/B tests. Any new design should start from this foundation.

### Layout
- **Direction:** Horizontal cards with radio buttons for pack selection
- **Options:** 3 pack choices (1 Pack, 2 Packs, 3 Packs)
- **Default:** 3 Packs with Subscription pre-selected
- **Section header:** "FINAL SUPERSAVINGS"

### Subscription Module
- Dashed border checkbox with circular radio
- Pre-selected state: filled orange circle, cream/yellow background
- Unselected: empty circle, white background with dashed border
- Copy: "Save More With Automatic Refills"
- Sub-copy: "Zero Commitment | Cancel Anytime"

### CTA
- Text: "ADD TO CART" (static, no price in button)
- Style: Full-width button

### Pricing (Current Live)
| Pack | Subscription | One-Time | Compare-At |
|------|-------------|----------|------------|
| 1 Pack | $34.99 | $40.99 | $57.99 |
| 2 Packs | $49.99 | $57.99 | $115.98 |
| 3 Packs | $58.99 | $68.99 | $173.97 |

## Design Rules for Paper

When creating new offer designs in Paper:

1. **Start from control layout.** Never rebuild from scratch.
2. **Change ONE element at a time.** If testing CTA copy, keep everything else identical.
3. **Use brand fonts only.** Americana BT Bold for headings, Montserrat for body.
4. **1px border-radius maximum.** On all elements.
5. **No shadows, no glow.** Use frosty glass (backdrop-filter blur) for depth.
6. **Light backgrounds only.** Use Yellow-25 (#FEFDF0) or white.
7. **Keep subscription as default.** Always pre-select subscription option.
8. **Keep OTP behind toggle.** Never make OTP a separate visible card.
9. **3 pack options.** Always offer 1/2/3 pack choices.
10. **Pack-based naming.** Use "1 Pack / 2 Packs / 3 Packs", not time-based or creative names.

## Elements That Can Be Safely Tested

Based on data, these individual changes are low-risk to test:
- CTA copy: "ADD TO CART" vs "GET STARTED" vs "BUY NOW"
- Adding "Save $X" or "X% OFF" badges to pack cards
- Adding per-day price display (e.g., "$0.66/day")
- Adding "Most Popular" badge on 3-pack
- Moving countdown timer closer to CTA
- Adding review count badge near offer section
- Dynamic CTA showing selected price ("ADD TO CART - $58.99")

## Elements That Should NEVER Be Used

- Vertical card layouts
- Side-by-side Subscribe/One-Time toggle buttons
- OTP as a separate selectable card
- "Buy X Get Y Free" naming
- Removing the OTP option entirely
- Reducing to 2 pack options
- Dark backgrounds or sections

## Product Assets

When designing, reference:
- Product photos in `data/products/`
- Brand guidelines in `docs/brand_preferences.md`
- Color palette in `config/brand.py`
