---
name: init
description: Initialize delego — intent-bound action authorization for AI agents — in the current project. Installs the package, creates a project-scoped delego home with signing keys and a starter policy, and verifies it. The delego MCP server is provided by this plugin, so this does NOT touch .mcp.json. Use when the user wants to "set up delego", "add delego to this project", or "initialize delego".
---

# init

Stand up [delego](https://github.com/Delego-Dev/delego) in this project so an
agent's actions are authorised against a deterministic policy, sensitive ones are
parked for human approval, and every decision lands in a signed audit trail —
all *before* any credential is used.

> This plugin already ships the delego **MCP server** (it reads
> `DELEGO_HOME = <project>/.claude/.delego`). So you do **not** edit `.mcp.json`
> here — you only install the package and create that home.

## Say this first
delego authorises an agent's **declared** action; it is only a real control when
the credential is reachable **solely** through a broker the agent can't bypass.
If the agent also has raw network/shell access, delego is advisory. Make sure the
user understands that.

Require Python ≥ 3.10.

## Steps

1. **Install delego with the MCP extra** (the plugin's MCP server runs
   `delego-mcp`, which this provides):
   ```bash
   python3 -m venv .venv 2>/dev/null || true
   .venv/bin/pip install -U "delego[mcp]"
   ```
   Use the project's existing venv / uv / poetry env if it has one. Ensure
   `delego-mcp` is on the PATH Claude Code launches the MCP server with (activate
   the venv, or install into the environment Claude Code uses).

2. **Create the delego home** the plugin's MCP server points at:
   ```bash
   .venv/bin/delego --home .claude/.delego init
   ```
   This creates the Ed25519 signing key, an example policy, and a `.gitignore`
   keeping the key, ledger, approvals, and `*.lock` out of git. Idempotent.

3. **Draft a real policy.** Offer to run the **policy-drafter** skill
   (`/delego:policy-drafter`) to write a policy for this project's agent. Never
   leave `default` as anything but `deny`. Keep the example only as a placeholder.

4. **Verify:**
   ```bash
   .venv/bin/delego --home .claude/.delego policy   # show the loaded policy
   .venv/bin/delego --home .claude/.delego verify   # check the audit chain
   ```
   Report both.

5. **Activate the MCP server.** It starts automatically once `delego-mcp` is
   installed and the home exists. If the `/plugin` Errors tab showed a
   `delego-mcp not found` error on first load (before step 1), reload the plugin
   or restart Claude Code. After that the agent can call `delego_propose_action` /
   `delego_resolve_action`; the human decides with the **approval-triage** skill
   (`/delego:approval-triage`) or `delego --home .claude/.delego approve <id>`.

## Guardrails
- Never commit `.claude/.delego/signing_key.pem`, the ledger, or `*.lock`.
- Re-running this skill is safe.
