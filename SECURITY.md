# Security Policy

This repository packages delego for Claude Code — bundling its **skills**,
**review agents**, and the **MCP server**. Installing the plugin places an MCP
server and tooling into a developer's environment, so we take issues here
seriously.

## Reporting a vulnerability

**Please do not open a public issue for security vulnerabilities.**

Report privately via GitHub's
[private vulnerability reporting](https://github.com/Delego-Dev/plugin/security/advisories/new),
or email **koishore@gmail.com**. Include the affected component (skill, agent, or
the MCP server) and reproduction steps. We aim to acknowledge within 72 hours.

## In scope

- The bundled **MCP server** (`delego-mcp`) exposing an operation that authorizes,
  approves, or mutates the audit ledger in a way the policy should prevent.
- A **skill or agent** that can be steered into running an unintended command,
  leaking the policy or ledger, or weakening the firewall it is meant to manage.
- The plugin / marketplace manifests resolving to unexpected code on install.

## Out of scope

- The **authorization and audit guarantees themselves** live in the delego
  package — report those upstream at
  [delego](https://github.com/Delego-Dev/delego/security).
- Misconfiguration in a user's own policy.

## Supported versions

Pre-1.0; only the latest released plugin version receives security fixes.
