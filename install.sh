#!/usr/bin/env bash
# À la carte install — use this only if you don't want the plugin. The plugin is
# easier (one command, auto-updates, namespaced):
#
#   /plugin marketplace add Delego-Dev/plugin
#   /plugin install delego@delego
#
# This copies delego's skills + agents into a project's .claude/ with a `delego-`
# name prefix. (The plugin namespaces them as `delego:`; outside a plugin we add
# the prefix so they don't collide with your own skills/agents.)
#
# Usage — run from your project root:
#   /path/to/plugin/install.sh                # into ./.claude
#   /path/to/plugin/install.sh /my/project    # into /my/project/.claude
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${1:-$PWD}/.claude"

# portable in-place sed that prefixes a `name:` frontmatter value with `delego-`
_prefix_name() {
  sed -i.bak -E "s/^name: ([a-z0-9]+(-[a-z0-9]+)*)$/name: delego-\1/" "$1" && rm -f "$1.bak"
}

mkdir -p "$DEST/skills"
for s in "$HERE"/delego/skills/*/; do
  name="$(basename "$s")"
  out="$DEST/skills/delego-$name"
  rm -rf "$out"; cp -R "$s" "$out"
  _prefix_name "$out/SKILL.md"
  echo "  skill  /delego-$name"
done

rm -rf "$DEST/agents/delego"; mkdir -p "$DEST/agents/delego"
cp -R "$HERE"/delego/agents/. "$DEST/agents/delego/"
while IFS= read -r f; do _prefix_name "$f"; done < <(find "$DEST/agents/delego" -name '*.md')
echo "  agents @agent-delego-* -> $DEST/agents/delego/"

echo "Done -> $DEST. Skills hot-load; restart Claude Code for the agents."
