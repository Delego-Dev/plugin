# delego — Claude Code plugin

The one-command way to get [delego](https://github.com/Delego-Dev/delego) — the
policy & audit firewall for agent actions — into a Claude Code project: its
**skills**, **review agents**, and the **MCP server**, all in a single plugin.
This repo is both the plugin and its own marketplace.

## Install

In Claude Code:

```
/plugin marketplace add Delego-Dev/plugin
/plugin install delego@delego
```

That's it — Claude Code places the skills, agents, and MCP server in the right
spots (no manual cloning into `.claude/`). Then:

```
/delego:init
```

`/delego:init` installs the `delego` Python package (`pip install "delego[mcp]"`),
creates the project firewall home at `.claude/.delego`, drafts/validates a policy,
and verifies. The plugin's MCP server reads `DELEGO_HOME = <project>/.claude/.delego`
and activates once the package is installed and the home exists.

> **Prerequisite:** the MCP server runs the `delego-mcp` command, which comes from
> `pip install "delego[mcp]"` (done by `/delego:init`). Until it's installed,
> Claude Code's `/plugin` Errors tab will show `delego-mcp not found` — expected;
> it clears after init + a reload.

## What's inside

**Skills** (`/delego:<name>`)
| Skill | Use it to… |
|---|---|
| `init` | Install delego, create the firewall home, verify. |
| `policy-drafter` | Draft/harden a fail-closed `policy.yaml`. |
| `approval-triage` | Review pending approvals and approve/deny. |
| `audit-explainer` | Verify the signed chain and explain what the agent did. |

**Agents** (`@delego:<name>`)
| Agent | Use it to… |
|---|---|
| `policy-reviewer` | Adversarially review a policy.yaml (footguns, over-broad rules, fail-open gaps). |
| `broker-reviewer` | Review a custom `BrokerAdapter` against the invariants. |
| `audit-investigator` | Verify the ledger, reconstruct authority paths, flag anomalies. |

**MCP server** — `delego_propose_action`, `delego_resolve_action`,
`delego_audit_tail`, `delego_show_policy` (the agent's interface to the firewall).

## Typical flow

1. `/plugin install delego@delego` → `/delego:init` (sets everything up).
2. `/delego:policy-drafter` to write the policy → `@delego:policy-reviewer` to
   harden it.
3. At runtime the agent proposes actions through the MCP server; decide parked
   ones with `/delego:approval-triage`, read the trail with `/delego:audit-explainer`,
   investigate incidents with `@delego:audit-investigator`.

## Repo layout

```
.claude-plugin/marketplace.json    # this repo is its own marketplace
delego/
  .claude-plugin/plugin.json       # the plugin manifest
  .mcp.json                        # the delego MCP server
  skills/<name>/SKILL.md           # invoked as /delego:<name>
  agents/<cluster>/<name>.md       # invoked as @delego:<name>
```

`python scripts/validate.py` (run in CI) checks the manifests and every
skill/agent's frontmatter.

## Standalone alternative

Prefer not to use a plugin? The same skills and agents are available as plain
repos to clone into `.claude/`: [skills](https://github.com/Delego-Dev/skills)
and [agents](https://github.com/Delego-Dev/agents).

## License

Apache-2.0. Built for [delego](https://github.com/Delego-Dev/delego); see the
[wire specification](https://github.com/Delego-Dev/specification).
