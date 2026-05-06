# Security Policy

Fleet Scorecard Spec is a documentation and schema repository. The primary
security concern is accidental exposure of sensitive run evidence.

## Reporting a vulnerability

Please report security issues privately through GitHub's security advisory flow
or by opening a minimal issue that does not include secrets, credentials, or
private logs.

## Implementation guidance

Fleet Scorecard implementations should:

- redact token-like strings from log excerpts
- keep generated `.fleet-scorecards/` overlays out of source commits by default
- avoid publishing raw command output without review
- preserve partial and failed statuses instead of converting them to success
- avoid treating heartbeats or preflights as final success evidence

## Sensitive evidence

Evidence indexes should point to source artifacts, but public scorecards should
summarize sensitive logs instead of copying them verbatim.
