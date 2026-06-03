---
name: audit-explainer
description: Read, verify, and explain a delego audit trail — verify the signed hash chain, summarize what the agent did, reconstruct why an action was allowed or denied and which instruction authorised it, and flag anomalies (denials, confused-deputy / substituted-action refusals, single-use replays, rate-limit hits). Use when the user asks "what did my agent do?", "verify the audit log", or "why was X allowed/denied?".
---

# audit-explainer

Make delego's signed receipt chain legible.

## Get the data
- `delego --home <home> verify` — checks content hashes, linkage, and signatures.
- `delego --home <home> log -n <N>` — recent receipts (or the MCP
  `delego_audit_tail` tool).

Find the home from `DELEGO_HOME`, the `.mcp.json` `delego` server env, or the
project's `./.claude/.delego`.

## Read a receipt
Each receipt records `phase` (`decision` | `execution`), `outcome`
(`allow` | `deny` | `needs_approval`), the matched `rule`, the human-readable
`reasons`, and the `intent_hash` → `action_fingerprint` pair that ties an
executed action back to the instruction that authorised it.

## What to surface
- A plain-language summary: what was allowed, parked for approval, or denied.
- For a specific action: reconstruct its authority path — instruction → decision
  → approval → execution — from the receipts sharing its `approval_id` /
  `action_fingerprint`.
- **Anomalies to flag:**
  - `execution`/`deny` reading "approval/action mismatch" or "intent mismatch" — a
    confused-deputy / substituted-action attempt.
  - "approval already used" — a single-use replay attempt.
  - Clusters of `deny`, forbidden-rule hits, repeated `rate_limit` denials.

## Be honest about the guarantees
`verify` catches edits, reordering, and middle deletions — but **not** truncation
of the most recent receipts (a truncated prefix verifies clean), and the local
signing key gives no protection after a host compromise. For rollback detection
the head must be anchored externally (`verify(expected_head=…)`). State this; do
not oversell the audit.
