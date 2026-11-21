# Contributing

Thanks for helping. This guide is only useful if it's accurate, so a few rules.

## Ground rules

- **Link to the source.** Every table name, connector name, licence statement and date needs a link to Microsoft Learn, the Azure-Sentinel GitHub repo, or another official Microsoft source. Community blogs are fine as extra reading, not as the only source.
- **Verify before you mark verified.** Set the "Last verified" date only when you've checked every table name and link in the guide yourself.
- **Use the template.** Start from [TEMPLATE.md](TEMPLATE.md) and keep the section order so readers can jump around.
- **Mark assumptions.** In KQL, put `// ASSUMPTION:` on any line that depends on something you couldn't confirm.
- **No secrets or customer data.** Scrub tenant IDs, workspace IDs, UPNs and IP addresses from screenshots and sample output.

## Writing style

- Plain Australian English. Short sentences, contractions are fine.
- No em dashes, emojis or marketing language.
- Use Microsoft's current product names (for example Microsoft Entra ID, not Azure AD) and mention the old name once if it helps.
- Use exact table names in backticks, for example `SigninLogs`.

## Diagrams

Use Mermaid `flowchart LR` so diagrams render on GitHub and stay editable. Keep node labels short.

## How to contribute

1. Pick an issue, or open one using the **Product guide** or **Correction** template.
2. Comment on the issue so others know you're on it.
3. Fork, branch, and open a pull request that references the issue.
4. A maintainer reviews for accuracy, links and style.

## Labels

- `product:*` one per product guide
- `area:*` the folder group (identity, endpoint, azure and so on)
- `type:guide`, `type:diagram`, `type:detections`, `type:docs`, `type:tooling`, `type:correction`
- `priority:p1`, `priority:p2`, `priority:p3`
- `good first issue` for well-scoped starter work
