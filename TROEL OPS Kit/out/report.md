# TROEL OPS Kit Report

_Generated on 2026-04-10_

## Summary
- SKUs with stock: **200**
- SKUs in sales: **200**
- Alerts: **6**

---

## Top low coverage (risk of stockout)

| SKU | On hand | Avg daily demand | Coverage (days) |
|---|---:|---:|---:|
| SKU-0001 | 1 | 0.29 | 3.5 |
| SKU-0157 | 3 | 0.68 | 4.4 |
| SKU-0003 | 1 | 0.21 | 4.7 |
| SKU-0002 | 1 | 0.21 | 4.7 |
| SKU-0137 | 2 | 0.43 | 4.7 |
| SKU-0029 | 5 | 0.68 | 7.4 |
| SKU-0125 | 5 | 0.68 | 7.4 |
| SKU-0195 | 3 | 0.36 | 8.4 |
| SKU-0021 | 3 | 0.21 | 14.0 |
| SKU-0064 | 10 | 0.68 | 14.7 |


---

## Top "A" items (ABC)

| SKU | Total qty | Unit cost | Consumption value | ABC |
|---|---:|---:|---:|---|
| SKU-0120 | 111 | 91.48 | 10154.3 | A |
| SKU-0099 | 104 | 93.48 | 9721.9 | A |
| SKU-0160 | 116 | 80.71 | 9362.4 | A |
| SKU-0080 | 91 | 99.27 | 9033.6 | A |
| SKU-0128 | 71 | 118.56 | 8417.8 | A |
| SKU-0034 | 73 | 107.26 | 7830.0 | A |
| SKU-0189 | 78 | 99.65 | 7772.7 | A |
| SKU-0114 | 87 | 86.88 | 7558.6 | A |
| SKU-0137 | 81 | 92.52 | 7494.1 | A |
| SKU-0017 | 71 | 103.67 | 7360.6 | A |


---

## Alerts (sample)

| Severity | Code | SKU | Message | Metric |
|---|---|---|---|---:|
| warning | DEAD_SKU | SKU-0005 | Aucune vente sur 60j avec stock>0 | 184.0 |
| warning | LOW_COVERAGE | SKU-0001 | Couverture faible (3.5 jours) | 3.5 |
| warning | LOW_COVERAGE | SKU-0157 | Couverture faible (4.4 jours) | 4.421052631578947 |
| warning | LOW_COVERAGE | SKU-0003 | Couverture faible (4.7 jours) | 4.666666666666667 |
| warning | LOW_COVERAGE | SKU-0002 | Couverture faible (4.7 jours) | 4.666666666666667 |
| warning | LOW_COVERAGE | SKU-0137 | Couverture faible (4.7 jours) | 4.666666666666667 |
