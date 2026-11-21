# Cost estimation

> Status: stub. Tracked in the "Cost estimation query pack" issue.

Starter query, GB per table over 30 days:

```kql
Usage
| where TimeGenerated > ago(30d)
| where IsBillable == true
| summarize GB = round(sum(Quantity) / 1024, 2) by DataType
| order by GB desc
```
