# Offer Testing Guidelines

## Lessons from 7 A/B Tests

### What We Know Works (Control Pattern)
- Horizontal card layout with radio selection
- Pack-based naming: "1 Pack / 2 Packs / 3 Packs"
- Checkbox toggle for subscription (pre-selected, dashed border)
- OTP hidden behind toggle (less prominent)
- 3 quantity options
- Standard $X.99 pricing
- No savings badges on cards
- Static "ADD TO CART" CTA
- 3-pack subscription as default selection

### What We Know Fails

1. **Vertical stacked cards** - Tested in 7/7 variants, avg -1.8% conversion
2. **Side-by-side Sub/OTP toggle** - avg -2.2% conversion, -25% subscription rate
3. **OTP as separate visible card** - avg -1.4% conversion, -21% subscription rate
4. **Subscription-only model** - avg -1.7% conversion despite 100% sub rate
5. **BOGO naming** - eliminates OTP entirely, -1.7% conversion

### What Hasn't Been Tested Yet

These are individual elements that should be tested on the control:

1. CTA copy variations ("GET STARTED", "BUY NOW", "SUBSCRIBE NOW")
2. Savings badges on cards ("Save $X")
3. Per-day pricing display ("$0.66/day")
4. "Most Popular" badge on 3-pack
5. Countdown timer placement (in offer module vs header)
6. Dynamic CTA showing price ("ADD TO CART - $58.99")
7. Review count near offer section
8. Pricing micro-adjustments ($54.99 vs $58.99 for 3-pack)
9. OTP price increase ($44.99 vs $40.99 for 1-pack)

## Test Prioritization Framework

### Priority 1: Single-element tests on control
Lowest risk, clearest learnings. Change ONE thing at a time.

### Priority 2: Pricing micro-tests
Small pricing changes can have outsized impact on AOV and LTV.

### Priority 3: Urgency and social proof
Placement of urgency elements and social proof near the offer module.

### Priority 4: Checkout/cart optimization
Fixing accidental subscription issue (33.2% of cancels).

## Testing Checklist

Before launching any test:
- [ ] Only ONE element changed from control
- [ ] Test URL created and verified on mobile
- [ ] Elevate A/B configured (50/50, mobile, US only)
- [ ] Control URL confirmed as live PDP
- [ ] Minimum 2,000 visitor target planned
- [ ] Subscription vs OTP tracking enabled
- [ ] Session duration tracking enabled
