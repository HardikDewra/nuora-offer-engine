/**
 * Nuora Offer Scoring API
 *
 * REST API that scores offer configurations against historical A/B test data.
 * Used by the CRO team to quickly evaluate new offer ideas before testing.
 *
 * Endpoints:
 *   POST /score           - Score a single offer configuration
 *   POST /compare         - Compare two offer configurations
 *   GET  /control         - Get the control (winning) configuration and score
 *   GET  /tests           - List all historical test results
 *   GET  /sweet-spots     - Get pricing sweet spot analysis
 *   GET  /health          - Health check
 *
 * Usage:
 *   cd tools && npm install && node offer_api.js
 *   Server runs on http://localhost:3000
 */

const express = require("express");
const fs = require("fs");
const path = require("path");

const app = express();
app.use(express.json());

// CORS for browser access
app.use((req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header("Access-Control-Allow-Headers", "Content-Type");
  res.header("Access-Control-Allow-Methods", "GET, POST, OPTIONS");
  if (req.method === "OPTIONS") return res.sendStatus(200);
  next();
});

// =====================================================
// SCORING WEIGHTS (derived from 7 A/B tests)
// =====================================================

const CONV_WEIGHTS = {
  layout: { horizontal: 0, vertical: -1.8 },
  toggle_type: { checkbox: 0, side_by_side: -2.2, none: -1.7, separate_card: -1.4 },
  otp_visibility: { behind_toggle: 0, separate_card: -1.4, equal_weight: -2.0, not_available: -1.0 },
  naming: { pack_based: 0, time_based: -0.5, creative: -0.4, bogo: -1.7 },
  num_options: { 3: 0, 2: -0.5 },
  pricing_display: { standard: 0, rounded: -0.1 },
  savings_display: { none: 0, dollar: -0.3, percent: -0.3 },
  product_images: { false: 0, true: 0 },
  cta_copy: { add_to_cart: 0, buy_now: -0.1, get_started: -0.1 },
};

const SUB_WEIGHTS = {
  layout: { horizontal: 0, vertical: -8 },
  toggle_type: { checkbox: 0, side_by_side: -25, none: 5, separate_card: -15 },
  otp_visibility: { behind_toggle: 0, separate_card: -15, equal_weight: -20, not_available: 17 },
  naming: { pack_based: 0, time_based: -3, creative: 0, bogo: -5 },
  num_options: { 3: 0, 2: -2 },
  pricing_display: { standard: 0, rounded: 0 },
  savings_display: { none: 0, dollar: 0, percent: 0 },
  product_images: { false: 0, true: 0 },
  cta_copy: { add_to_cart: 0, buy_now: 0, get_started: 0 },
};

const BASELINE = {
  conversion_rate: 7.65,
  subscription_rate: 83,
  aov: 53.38,
};

// =====================================================
// SCORING FUNCTION
// =====================================================

function scoreOffer(config) {
  let convDelta = 0;
  let subDelta = 0;
  const breakdown = [];

  for (const [element, value] of Object.entries(config)) {
    const convImpact = CONV_WEIGHTS[element]?.[String(value)] ?? 0;
    const subImpact = SUB_WEIGHTS[element]?.[String(value)] ?? 0;
    convDelta += convImpact;
    subDelta += subImpact;
    if (convImpact !== 0 || subImpact !== 0) {
      breakdown.push({ element, value: String(value), conv_impact: convImpact, sub_impact: subImpact });
    }
  }

  const predictedConv = Math.max(0, BASELINE.conversion_rate + convDelta);
  const predictedSub = Math.max(0, Math.min(100, BASELINE.subscription_rate + subDelta));

  let risk, riskDesc;
  if (convDelta >= -0.5) {
    risk = "low";
    riskDesc = "Close to proven control pattern";
  } else if (convDelta >= -2.0) {
    risk = "medium";
    riskDesc = "Some historically negative elements present";
  } else {
    risk = "high";
    riskDesc = "Multiple elements that hurt conversion in past tests";
  }

  return {
    predicted_conversion_rate: +predictedConv.toFixed(2),
    predicted_subscription_rate: +predictedSub.toFixed(1),
    conversion_delta: +convDelta.toFixed(2),
    subscription_delta: +subDelta.toFixed(1),
    risk_level: risk,
    risk_description: riskDesc,
    breakdown,
    baseline: BASELINE,
  };
}

// =====================================================
// LOAD TEST DATA
// =====================================================

function loadTests() {
  const dir = path.join(__dirname, "..", "data", "test_results");
  const tests = [];
  for (const file of fs.readdirSync(dir).sort()) {
    if (!file.endsWith(".json") || file === "control.json") continue;
    tests.push(JSON.parse(fs.readFileSync(path.join(dir, file), "utf-8")));
  }
  return tests;
}

function loadControl() {
  const fp = path.join(__dirname, "..", "data", "test_results", "control.json");
  return JSON.parse(fs.readFileSync(fp, "utf-8"));
}

// =====================================================
// ROUTES
// =====================================================

// Health check
app.get("/health", (req, res) => {
  res.json({ status: "ok", engine: "nuora-offer-scorer", version: "1.0.0" });
});

// Score an offer
app.post("/score", (req, res) => {
  const config = req.body;
  if (!config || Object.keys(config).length === 0) {
    return res.status(400).json({ error: "Request body must contain offer configuration" });
  }
  const result = scoreOffer(config);
  res.json(result);
});

// Compare two offers
app.post("/compare", (req, res) => {
  const { offer_a, offer_b } = req.body;
  if (!offer_a || !offer_b) {
    return res.status(400).json({ error: "Body must contain offer_a and offer_b" });
  }
  const scoreA = scoreOffer(offer_a);
  const scoreB = scoreOffer(offer_b);
  res.json({
    offer_a: scoreA,
    offer_b: scoreB,
    winner: scoreA.predicted_conversion_rate >= scoreB.predicted_conversion_rate ? "offer_a" : "offer_b",
    conv_difference: +(scoreA.predicted_conversion_rate - scoreB.predicted_conversion_rate).toFixed(2),
  });
});

// Get control config and score
app.get("/control", (req, res) => {
  const control = loadControl();
  const controlConfig = {
    layout: "horizontal",
    toggle_type: "checkbox",
    otp_visibility: "behind_toggle",
    naming: "pack_based",
    num_options: 3,
    pricing_display: "standard",
    savings_display: "none",
    product_images: false,
    cta_copy: "add_to_cart",
  };
  res.json({
    config: controlConfig,
    score: scoreOffer(controlConfig),
    pricing: control.pricing,
    performance: control.avg_performance,
  });
});

// List all tests
app.get("/tests", (req, res) => {
  const tests = loadTests();
  const summary = tests.map((t) => ({
    name: t.name,
    style: t.style,
    version: t.version,
    date: t.test_date,
    result: t.result,
    variant_conv: t.metrics.variant.conversion_rate,
    control_conv: t.metrics.control.conversion_rate,
    variant_sub_rate: t.metrics.variant.subscription_rate,
    variant_aov: t.metrics.variant.aov,
    total_visitors: t.metrics.control.visitors + t.metrics.variant.visitors,
  }));
  res.json({ count: summary.length, tests: summary });
});

// Pricing sweet spots
app.get("/sweet-spots", (req, res) => {
  res.json({
    subscription_entry_point: {
      current: 34.99,
      sweet_spot: { low: 34.0, high: 40.0 },
      note: "Control's $34.99 consistently wins. Don't go below $30.",
    },
    subscription_max_bundle: {
      current: 58.99,
      sweet_spot: { low: 53.0, high: 60.0 },
      note: "Keep 3-pack under $60 for maximum conversion.",
    },
    otp_gap: {
      current_pct: "14-15%",
      note: "OTP should be 14-15% higher than subscription to nudge toward sub.",
    },
    per_pack_pricing: {
      "1_pack_sub": { price: 34.99, per_day: 1.17 },
      "2_pack_sub": { price: 25.0, per_day: 0.83 },
      "3_pack_sub": { price: 19.66, per_day: 0.66 },
    },
  });
});

// =====================================================
// START
// =====================================================

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Nuora Offer Scoring API running on http://localhost:${PORT}`);
  console.log(`Endpoints:`);
  console.log(`  POST /score       - Score an offer configuration`);
  console.log(`  POST /compare     - Compare two offers`);
  console.log(`  GET  /control     - Get winning control config`);
  console.log(`  GET  /tests       - List all test results`);
  console.log(`  GET  /sweet-spots - Pricing analysis`);
  console.log(`  GET  /health      - Health check`);
});
