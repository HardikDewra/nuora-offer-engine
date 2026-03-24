# Nuora Offer Intelligence Report

**Generated:** 2026-03-24 16:31
**Data Source:** 8 A/B tests, 26,723 visitors, Jan 2026
**Product:** Nuora Vaginal Probiotic Gummies

---

## Executive Summary

- **Control has won all 8 tests** with avg 7.38% conversion
- Variants average 5.38% conversion (gap: -2.0%)
- Control maintains 78.5% subscription rate vs variant avg 77.7%
- The current control offer is well-optimized; future gains come from micro-testing individual elements

---

## Pricing Sweet Spots

### Subscription Entry Point
- **Current:** $34.99
- **Sweet spot:** $34.0 - $40.0
- Control's $34.99 entry consistently wins. Variants at $29.99-$34.19 (Resilia, Ryze) didn't convert better despite lower prices. Variants at $37.99-$40.00 (Ankhway, Omre) came closest to control performance. The $34-40 range appears optimal for subscription entry.

### Max Bundle Price
- **Current:** $58.99
- **Sweet spot:** $53.0 - $60.0

### Per-Pack Analysis
| Pack | Sub Price | Per Day | OTP Price | Sub/OTP Gap |
|------|-----------|---------|-----------|-------------|
| 1 Pack | $34.99 | $1.17 | $40.99 | 14.6% |
| 2 Pack | $25.00/pk | $0.83 | $29.00/pk | 13.8% |
| 3 Pack | $19.66/pk | $0.66 | $23.00/pk | 14.5% |

---

## Pricing Recommendations

### Keep (Proven Working)
- 3-pack default selection at $58.99 subscription
- $34.99 entry point for 1-pack subscription
- 14-15% OTP-to-subscription price gap across all packs
- Compare-at pricing ($57.99 anchor for 1-pack)

### Test (Potentially Better)
- **Increase 1-pack OTP from $40.99 to $44.99** - Wider gap between OTP and sub may push more toward subscription without hurting overall CVR (Risk: low)
- **Add per-day cost display ($0.66/day for 3-pack)** - Makes the 3-pack value concrete. $0.66/day feels very affordable for a health supplement (Risk: low)
- **Test $54.99 for 3-pack subscription (from $58.99)** - Keeping it under $55 is a psychological threshold. Still above cost basis with healthy margin (Risk: medium)

### Avoid
- Dropping entry below $30 (Resilia's $29.99 didn't help)
- Round number pricing in isolation (Omre V2 showed negligible impact)
- BOGO framing with inflated compare-at prices (Resilia's $299.95 compare felt fake)
- Identical Sub and OTP pricing for 1-pack (removes subscription incentive)

---

## LTV by Cadence

| Cadence | AOV | Churn/mo | LTV | Lifetime | Subscribers |
|---------|-----|----------|-----|----------|-------------|
| monthly_1pack | $39.33 | 19.6% | $200.66 | 5.1mo | 22,690 |
| bimonthly_2pack | $50.06 | 20.7% | $241.84 | 4.8mo | 13,048 |
| quarterly_3pack | $58.64 | 17.0% | $114.98 | 5.9mo | 29,474 |

---

## LTV Improvement Opportunities

### Fix accidental subscription checkout UX
Reduce 'subscribed by accident' cancels by 50%
- **Annual impact:** $3,556,857.09

### Shift 10% of monthly subs to quarterly
Push more customers toward 3-pack quarterly subscription
- **Total LTV gain:** $-194,407.92

### Increase AOV by $5 through bundle upsell
Add complementary product suggestion at checkout
- **Annual impact:** $1,304,240.00

---

## Recommended Next Tests

### Priority 1: Test individual elements on the winning control
All 7 variants changed 5+ elements simultaneously. Change ONE element at a time on the control to isolate what actually drives performance.

- CTA: 'ADD TO CART' -> 'GET STARTED' (Risk: very low)
- Add 'Save $X' badges to pack cards (Risk: low)
- Add per-day price display ($0.66/day) (Risk: low)
- Add 'Most Popular' badge to 3-pack (Risk: very low)

### Priority 2: Test pricing micro-adjustments on control
The control pricing hasn't been A/B tested in isolation. Small pricing changes can have outsized revenue impact.

- 3-pack sub: $58.99 -> $54.99 (keep everything else) (Risk: low)
- 1-pack OTP: $40.99 -> $44.99 (widen sub/OTP gap) (Risk: low)
- Compare-at: $57.99 -> $64.99 (increase perceived savings) (Risk: medium)

### Priority 3: Test urgency and social proof placement
Control has countdown in header only. Moving urgency closer to the CTA may increase conversion.

- Move countdown timer into offer module (above CTA) (Risk: low)
- Add '11,847 reviews' badge near offer section (Risk: very low)
- Add 'X people viewing this' live counter (Risk: medium)

### Priority 4: Fix accidental subscription issue (highest ROI opportunity)
33.2% of cancellations cite 'I subscribed by accident'. This is 12,191 lost subscribers. Fixing the checkout flow is worth more than any A/B test on the offer module.

- Add subscription confirmation step before checkout
- Make subscription terms more visible in cart
- Add 'You are subscribing to...' confirmation modal
- Test subscription checkbox copy for clarity

---

## Anti-Patterns

These design patterns should NOT be used based on test data:

### Vertical stacked cards
- Tested in: 7/7 variants
- Impact: -1.8%
- **NEVER use - consistently underperforms horizontal**

### Side-by-side Sub/OTP toggle
- Tested in: Omre V1, Omre V2
- Impact: -2.2%
- **NEVER use - destroys subscription rate**

### OTP as visible third card
- Tested in: Ankhway V1, Ankhway V2
- Impact: -1.4%
- **AVOID - makes OTP too accessible**

### Subscription-only (no OTP option)
- Tested in: Ryze V1, Ryze V2
- Impact: -1.7%
- **AVOID - eliminates OTP but loses conversion**

### BOGO naming
- Tested in: Resilia V1
- Impact: -1.7%
- **AVOID - creates commitment perception that deters buyers**

---

*Generated by Nuora Offer Intelligence Engine v1.0*
*Data: 8 A/B tests, 26,723 total visitors*
