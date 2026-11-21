# Defender XDR vs Sentinel: avoiding duplication

> Status: stub. Tracked in the "Defender XDR vs Sentinel duplication guidance" issue.

To do. Cover:

- What Defender XDR keeps by itself (advanced hunting, 30 days) and what that costs (nothing extra).
- When to stream raw Defender tables into Sentinel (custom rules joining non-Microsoft data, retention beyond 30 days, data lake hunting).
- Alert and incident duplication: use the Defender XDR connector for incidents, and turn off standalone alert connectors for the same products.
- Custom detections in Defender XDR vs analytic rules in Sentinel, now that many Content Hub solutions ship both formats.
