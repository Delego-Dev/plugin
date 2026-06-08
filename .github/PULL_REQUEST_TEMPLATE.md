<!-- Fork the repo and open this PR from a branch in your fork. See CONTRIBUTING.md. -->

## What & why

<!-- What does this skill/agent do (or what does it change), and why? -->

## AI assistance disclosure (required)

- [ ] No AI assistance.
- [ ] AI-assisted. Tool(s) and how used: ______
- [ ] AI-generated, human-reviewed. I have read every line and am accountable for it.

## Checklist

- [ ] Forked the repo; this PR comes from a branch in my fork.
- [ ] `python scripts/validate.py` passes (manifests + skill/agent frontmatter).
- [ ] Frontmatter is valid and the `description` is **precise** — it fires on the
  right requests only, and won't hijack unrelated ones.
- [ ] Instructions are **safe** (nothing destructive, credential-leaking, or that
  bypasses delego) and **delego-accurate** (fail-closed, the invariants,
  honest caveats — no overselling the audit).
- [ ] I did **not** change the plugin/marketplace manifest or the MCP config
  (or a maintainer has signed off — these affect every install).
