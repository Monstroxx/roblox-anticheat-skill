# Roblox Anticheat Skill

An agent skill for auditing and hardening Roblox experiences with minimal gameplay changes. Prevent unauthorized outcomes on the server instead of trusting client-side checks or replacing legitimate movement mechanics.

This is guidance for a coding agent, **not a drop-in anti-cheat script**.

## Protection and enforcement

- Secure remotes and functions with server-owned rules, input validation, permissions, bounded rate limits, and safe state changes.
- Validate touch, prompt, and click interactions without treating an event alone as proof of eligibility.
- Add optional, game-specific teleport observation while accounting for lag, respawn, dash, vehicles, knockback, and authorized teleports.
- Preserve existing architecture and normal movement.
- **Kick by default for confirmed server-side cheating under an agreed evidence rule.** Invalid requests or weak movement signals alone do not justify a kick.
- Require explicit user approval for bans, movement correction, and stronger enforcement.

Client functions and remotes cannot be made reliably unhookable. The skill focuses on making client manipulation ineffective. It does not promise zero false positives or universal movement detection.

## Install

Install for OpenCode using [Vercel's Skills CLI](https://github.com/vercel-labs/skills):

```powershell
npx skills add Monstroxx/roblox-anticheat-skill --skill roblox-anticheat --agent opencode
```

For another supported agent, replace `opencode` with its documented CLI identifier. The CLI may collect anonymous telemetry; set `DISABLE_TELEMETRY=1` to disable it according to Vercel's documentation.

To inspect or install a local checkout instead:

```powershell
npx skills add ./roblox-anticheat --list
npx skills add ./roblox-anticheat --agent opencode --copy
```

## Usage

Ask your coding agent:

> Audit my Roblox remotes and touch rewards for security issues. Preserve normal movement. Kick confirmed cheaters, but do not ban players or punish weak signals such as lag.

The skill first reads the project, resolves unanswered protection and enforcement choices, checks current official documentation, and implements the smallest relevant change. It then tests valid behavior as well as rejected requests and reports any unavailable verification layers.

## Contents

| Path | Purpose |
|---|---|
| `roblox-anticheat/SKILL.md` | Workflow and protection/enforcement decision table |
| `roblox-anticheat/references/` | Remotes, interactions, movement, economy/combat, enforcement, and official sources |
| `roblox-anticheat/scripts/roblox_docs.py` | Targeted official documentation retrieval using Python 3, with no third-party packages |
| `roblox-anticheat/evals/evals.json` | Three tasks for comparing responses with and without the skill |
| `roblox-anticheat/evals/fixtures/` | Deliberately vulnerable inputs for evaluation |

**Do not copy the vulnerable fixtures into a live game.** Generated evaluation solutions are not verified production modules either.

The skill is self-contained. Its research and verification approach was informed by `luau-script-hub`, but that skill and executor tooling are not required.

## Documentation helper

From a local checkout, use an available Python 3 interpreter:

```powershell
python roblox-anticheat/scripts/roblox_docs.py --selftest
python roblox-anticheat/scripts/roblox_docs.py search "securing client server boundary"
```

The helper follows Roblox's official `llms.txt`/Markdown retrieval surface and refuses the monolithic `llms-full.txt`. If Python is unavailable, use the official links through your agent's web tools instead.

## Verification limits

The initial evaluation compared three tasks with and without the skill using German-language prompts. Structure, documentation retrieval, and Luau syntax checks were performed; **Roblox Studio runtime tests were not**. The published prompts are English translations, not separately rerun evaluations.

Passing response/design checks does not prove correct replication, real kick behavior, or safe false-positive rates. Test changes in Studio with the actual game's mechanics, multiple clients, and relevant latency conditions before deployment.

Local evaluation outputs and the review viewer are kept in `roblox-anticheat-workspace/` and excluded from Git. They are not part of the published skill.
