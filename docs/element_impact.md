# Design Element Impact Analysis

## How This Was Calculated

Each element's impact is derived by comparing variant performance against its concurrent control group. When multiple tests use the same element, the impacts are averaged.

## Impact Matrix

### Layout Direction

| Value | Avg Conv Impact | Avg Sub Impact | Tests |
|-------|-----------------|----------------|-------|
| Horizontal (control) | BASELINE | BASELINE | All controls |
| Vertical stacked | -1.8% | -8% | All 7 variants |

**Insight:** Every single variant used vertical layouts. This is the most universally tested (and universally failing) element. Horizontal cards allow faster visual scanning and comparison.

### Subscription Toggle

| Value | Avg Conv Impact | Avg Sub Impact | Tests |
|-------|-----------------|----------------|-------|
| Checkbox (pre-selected) | BASELINE | BASELINE | Control + Resilia V1 |
| Side-by-side buttons | -2.2% | -25% | Omre V1, Omre V2 |
| No toggle (sub only) | -1.7% | +17% | Ryze V1, Ryze V2 |
| OTP as separate card | -1.4% | -15% | Ankhway V1, Ankhway V2 |

**Insight:** The checkbox toggle is the single most important element. Giving OTP equal visual weight (side-by-side buttons) is the most damaging pattern tested. It reduces both conversion AND subscription rate.

### OTP Visibility

| Value | Avg Conv Impact | Avg Sub Impact | Tests |
|-------|-----------------|----------------|-------|
| Behind toggle | BASELINE | BASELINE | Control, Resilia |
| Separate card | -1.4% | -15% | Ankhway V1/V2 |
| Equal weight | -2.0% | -20% | Omre V1/V2 |
| Not available | -1.0% | +17% | Ryze V1/V2 |

**Insight:** OTP should exist (removing it hurts conversion) but should NOT be prominent. The control's approach - hiding OTP behind a toggle that defaults to subscription - is optimal.

### Bundle Naming

| Value | Avg Conv Impact | Avg Sub Impact | Tests |
|-------|-----------------|----------------|-------|
| Pack-based | BASELINE | BASELINE | Control |
| Time-based | -0.5% | -3% | Ankhway, Omre |
| Creative names | -0.4% | Neutral | Ryze V1/V2 |
| BOGO | -1.7% | -5% | Resilia V1 |

**Insight:** Simple, concrete pack naming performs best. "30-day supply" implies time commitment. "Buy 2 Get 1 Free" implies a bigger deal than customers want.

### Number of Options

| Value | Avg Conv Impact | Tests |
|-------|-----------------|-------|
| 3 options | BASELINE | Control, Ryze, Resilia |
| 2 options | -0.5% | Ankhway, Omre |

**Insight:** Three options (1/2/3 packs) provides a good decoy effect. The 2-pack middle option makes the 3-pack look like better value.

### Neutral Elements (No Measurable Impact)

- **Product images on cards** - Tested in Resilia V1, Ryze V2. No conversion lift.
- **Rounded pricing** - Tested in Omre V2, Ankhway V2. Negligible impact.
- **Savings badges** - Tested across multiple variants. Slight negative (-0.3%).
- **CTA copy changes** - "BUY NOW" and "GET STARTED" vs "ADD TO CART". Minimal difference.

## Interaction Effects

Some elements are confounded because they always appear together:
- Vertical layout + time-based naming (in Ankhway, Omre)
- Subscription-only + creative naming (in Ryze)
- BOGO naming + product images (in Resilia)

Future tests should isolate these elements on the horizontal control layout.
