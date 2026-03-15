# Brand & Design Preferences

This documents the design preferences for all Nuora CRO assets. These apply to any offer, PDP, landing page, or tool built for the Nuora brand.

## Design Lead Preferences (Nikita)

### General
- **Light mode ONLY.** No dark mode, no dark backgrounds, no dark headers.
- **No shadows.** No `box-shadow`, no `text-shadow`, no drop shadows on any element.
- **No glow effects.** No glow, no radiance, no luminous effects of any kind.
- **No liquid glass.** Does NOT like the Apple iOS 26 / macOS Tahoe "liquid glass" look.
- **Frosty glass is OK.** Subtle frosted glass (backdrop-filter blur with semi-transparent white) is acceptable and preferred for card elements.
- **1px border-radius maximum.** No rounded corners beyond 1px. Applies to cards, buttons, inputs, tags, charts, badges - everything.
- **Minimal borders.** 1px solid borders only. Use subtle colors like `rgba(113, 59, 18, 0.08)` for glass borders.

### Typography
- **Headings:** Americana BT Bold (weight 700). Fallback: Georgia, Times New Roman, serif.
- **Body text:** Montserrat (weights 400-800). Available via Google Fonts.
- **No other fonts.** Only these two fonts should be used across all Nuora assets.

### Colors

#### Yellow Brand Palette (Gummies - Primary)
Used for the Vaginal Probiotic Gummies product and general brand identity.
```
#FEFDF0  Yellow-25   (Lightest background)
#FEFBE8  Yellow-50   (Light background)
#FEF7C3  Yellow-100  (Soft highlight)
#FDE272  Yellow-200  (Light accent)
#FAC515  Yellow-400  (Primary brand yellow)
#EAAA08  Yellow-500  (Hover state)
#CA8504  Yellow-600  (Dark accent)
```

#### Brown Palette (Text, Headings)
```
#854A0E  Brown-800   (Body text)
#713B12  Brown-900   (Headings, emphasis)
#542C0D  Brown-950   (Darkest - high contrast)
```

#### Rose Palette (Gut Ritual Product)
Used for the Gut Ritual capsules product line.
```
#FDF0F4  Rose-light  (Background)
#9B083E  Rose-primary (Main rose)
#7B1C3A  Rose-PDP    (PDP elements)
#4A0420  Rose-dark   (Darkest)
```

#### Blue Palette (Medical Gummies)
Used for medical-branded version of gummies (same SKU, different avatar).
```
#E3F2FD  Blue-light  (Background)
#1565C0  Blue-primary (Main blue)
```

### Do NOT Use
- Pure black (#000000) - use Brown-950 instead
- Gradients of any kind (`linear-gradient`, `radial-gradient`)
- Box shadows (`box-shadow`)
- Text shadows (`text-shadow`)
- Glow effects
- Border-radius greater than 1px
- Dark backgrounds for headers or sections
- Neon or saturated colors outside the approved palette

## Product Color Mapping

| Product | Primary Color | Use Case |
|---------|--------------|----------|
| Vaginal Probiotic Gummies | Yellow (#FAC515) | Main PDP, landing pages, offers |
| Gut Ritual Capsules | Rose (#9B083E) | Gut product PDP and pages |
| Medical Gummies | Blue (#1565C0) | Medical-branded avatar PDP |

All three products share the same Brown palette for text and the Yellow-25 background.

## Design Tool

Future designs are created using **Paper Design** (MCP server integration). Paper replaces Figma for new design work. All designers should use Paper for creating new offer layouts, PDP sections, and landing page components.

When using Paper, reference these guidelines and the existing control offer design as the baseline.
