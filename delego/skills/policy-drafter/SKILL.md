---
name: policy-drafter
description: Draft or harden a delego policy.yaml from a description of what an agent should and shouldn't be allowed to do. Knows the delego policy schema, the fail-closed evaluation order, and the common footguns. Use when the user wants to write, change, review, or tighten a delego policy, or asks "what should my delego policy be?".
---

# policy-drafter

Turn "here's what my agent should and shouldn't do" into a correct, fail-closed
delego `policy.yaml`.

## The model you're writing for
Evaluation order is **fixed**: `forbidden` (hard deny) → `rules` (first match
wins) → `default`. A matched rule whose constraints fail becomes a **deny**
(fail-closed). `default` MUST be `deny`. No LLM is in this decision — the policy
is the entire security surface, so precision matters.

## Schema
```yaml
version: 1
default: deny
forbidden:
  - name: <slug>
    description: <why>
    match: { method: <str|list>, host: <str>, path: <glob>, path_contains: <substr> }
rules:
  - name: <slug>
    description: <why>
    decision: allow | needs_approval
    match: { ... }                      # same fields as forbidden
    constraints:
      amount:     { field: <param>, max: <number>, currency: <str> }
      allow_list: { field: <param>, in: [<allowed>, ...] }
      rate_limit: { max: <int>, per: minute | hour | day }
```
`match`: `method` (string or list), `host` (exact, case-insensitive), `path`
(glob), `path_contains` (substring). Constraints read the decision-relevant
fields the agent declares in the action's `params`.

## Elicit — ask, don't assume
1. **What must the agent do unattended?** → `allow` rules (usually reads). Scope
   tightly by method + host + path.
2. **What's sensitive — money, outbound messages, state changes — that a human
   must approve every time?** → `needs_approval` rules + constraints (an amount
   cap with currency, an `allow_list` for recipients/destinations).
3. **What must NEVER happen?** → `forbidden` (permission/ACL changes, deletes,
   withdrawals, secret ops). Checked first; always deny.
4. Hosts, path shapes, amount caps + currency, and per-window rate limits.

## Footguns — get these right
- **`default: deny`.** Never `allow`.
- **`forbidden` is a hard stop** before any rule — put irreversible/destructive
  operations here, not in a rule that might be shadowed.
- **`path_contains` is a plain substring** — `/permissions` also matches
  `/permissions-export`. Prefer an exact `path` glob where you can.
- **Globs are coarse:** `**` and `*` both span `/` (they collapse). Don't rely on
  per-segment precision.
- **Cap every `amount`** and set its `currency` (a cap with no currency caps any
  currency; no cap means unlimited). The engine already denies non-finite and
  negative amounts.
- **Rate-limit `allow` rules** that hit external services.
- **Keep decision-relevant data in `params`, not the URL query** — the query
  string is not part of the action fingerprint yet (it lands in protocol 0.3), so
  a policy can't see it and an approval won't bind it. If safety depends on a
  query value, that policy is unsound today.
- **First-match-wins:** order rules narrow→broad; a broad `allow` placed first can
  shadow a `needs_approval` you intended.
- Approvals are **single-use and bound to the action fingerprint + intent** — a
  `needs_approval` rule means exactly one human-approved execution per request;
  you don't design that, just rely on it.

## Produce
1. Write `policy.yaml` (project root, or the delego home being used).
2. **Validate it:** `delego --home <home> policy` loads it; a malformed policy
   fails closed with an error. Fix whatever it rejects.
3. Walk the user through each rule in plain language, mapping it to their intent.
4. Recommend an adversarial pass with the **policy-reviewer** agent (`@delego:policy-reviewer`).
