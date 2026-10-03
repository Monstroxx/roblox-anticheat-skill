---
name: roblox-anticheat
description: Build, audit, and harden Roblox experience anti-cheat in Luau with minimal gameplay changes. Use whenever Roblox requests involve exploit prevention, insecure remotes, spoofed touch or prompt interactions, teleport checks, item duplication, server validation, anti-cheat false positives, or kick/ban policies. Preserve legitimate movement; use server-side evidence and ask for enforcement policy, with kicks as the default for confirmed cheating.
---

# Roblox anti-cheat

Prevent unauthorized outcomes at the server boundary before adding detectors. Harden the existing game, not an imagined replacement. A rejected request is not automatically proof of cheating; a confirmed violation can justify a server-side kick under the chosen policy.

## 1. Establish the project and verification surface

Read project instructions and existing scripts before proposing files. Locate client-triggered entry points, the authoritative state they mutate, existing limiters, transaction services, movement abilities, and player lifecycle cleanup. Reuse responsible modules; do not mandate a framework or file split.

Check which Luau tools and Roblox Studio/MCP integrations are actually available. Inspect the attached tool list; a shell cannot discover your MCP connections. Never require an executor to secure a Studio game. Syntax, pure logic, and Studio multi-client tests are different evidence layers.

If the game is unavailable, provide an explicitly labeled design or bounded example. Do not invent its movement rules, rewards, threshold measurements, or a successful runtime test.

## 2. Resolve policy before implementing consequences

Ask only for unanswered decisions. Show the following table in the user's language and record the choices in the change report. A user can accept the defaults together. A previous explicit kick preference resolves the confirmed-cheating row, but does not authorize bans or movement correction.

| Decision | Options | Default |
|---|---|---|
| Protection scope | Remotes/interactions; add teleport checks; game-specific extensions | Remotes/interactions |
| Invalid request without confirmed cheating | Drop; drop and bounded log | Drop and bounded log |
| Weak movement signal | Observe; deny a sensitive follow-up action when its own prerequisites fail | Observe |
| Position correction | Off; explicitly approved targeted correction | Off |
| Confirmed server-side cheating | Kick; temporary ban; permanent ban | **Kick** |
| Ban authorization | Off; explicit evidence rules, duration, and scope | Off |

Use [references/enforcement.md](references/enforcement.md) to define what counts as confirmed. Show concrete evidence rules and their exclusions before coding punitive behavior. Weak indicators do not become certainty merely by accumulating many copies of the same indicator. Zero false positives cannot be promised.

While awaiting an unresolved punitive decision, an explicitly requested non-punitive validation fix may proceed; leave new kicks/bans disabled rather than guessing. Do not implement an unrequested behavioral change.

## 3. Look up the APIs and select the relevant reference

Fetch current official documentation for APIs and platform behavior used in the change. Start from the official `llms.txt` indexes or search, follow discovered Markdown URLs, and check beta/deprecation status. Do not download `llms-full.txt`. Treat documentation examples as explanations, not audited production modules.

Optional cross-platform helper, requiring Python 3:

```text
python scripts/roblox_docs.py search "securing client server boundary"
python scripts/roblox_docs.py page /docs/en-us/scripting/security/client-server-boundary.md
python scripts/roblox_docs.py index engine
```

Run these paths relative to this skill directory or use their absolute paths. A web-fetch tool can replace the helper; the skill has no dependency on another installed skill.

| Work | Read |
|---|---|
| Remote validation, hooks, input budgets | [references/remote-security.md](references/remote-security.md) |
| Touch, prompts, click/drag, movable targets | [references/interactions.md](references/interactions.md) |
| Teleports, movement, ownership, server authority | [references/movement-physics.md](references/movement-physics.md) |
| Inventory, trading, purchases, combat | [references/economy-combat.md](references/economy-combat.md) |
| Evidence, kicks, bans, rollout | [references/enforcement.md](references/enforcement.md) |
| Official source map and research caveats | [references/sources.md](references/sources.md) |

## 4. Make the smallest responsible change

List the protected outcomes and who is allowed to determine them. Clients request actions; the server determines rewards, prices, inventory ownership, damage, and permissions. Client functions and remotes cannot be made reliably unhookable. Make manipulation ineffective instead of depending on obfuscation, hidden names, passwords shipped to clients, or client heartbeats.

Validate at the existing entry point before state mutation or broadcasting. Use server-derived identity, bounded payloads, finite numbers, expected instance ancestry/class, permissions, timing, and authoritative state. Rate-limit before expensive work; distinguish resource protection from legitimate ability cooldowns.

Keep server-only rules and secrets out of replicated modules. Shared prediction modules may expose simulation rules, but not secrets or server-only authorization. Never put executor APIs such as `firetouchinterest`, `hookfunction`, `getgenv`, or `getgc` in production anti-cheat code.

Do not bolt on client anti-tamper punishments, force server-owned characters, replace movement systems, create honeypots, or add telemetry services unless relevant and agreed. Existing protections should not be removed merely to shorten the diff.

## 5. Verify both rejection and legitimate acceptance

Identify expected results before running tests, then exercise the actual changed functions:

- Legal action still succeeds exactly as intended, including ordinary bursts and player lifecycle transitions.
- Wrong type, non-finite values, forged target, unauthorized action, spam, and repeat requests cannot produce the protected outcome.
- Economy and inventory tests cover concurrent requests, failures, retries, and idempotent rewards where relevant.
- Movement tests cover the game's allowed teleports, respawn, lag/server stalls, knockback, vehicles, and abilities; none is evidence for an automatic kick by itself.
- Enforcement tests demonstrate the default server kick for an approved, confirmed rule, and no ban without explicit authorization. Test the rule's legitimate near-misses too.

Use a genuine Luau parser/type checker if available. A Lua 5.1 fallback is not equivalent. Pure tests do not prove replication, engine event behavior, or latency tolerance. In Studio, test a server with multiple clients and relevant latency conditions. If unavailable, mark those checks **not run** and supply a reproducible Studio procedure.

## 6. Deliver and stop

Report: changed paths; protected outcomes; agreed scope and punishment table; proof for each test layer; unrun Studio cases; remaining tuning/rollout risks; disable/rollback instructions. Clearly separate verified behavior from proposed behavior.

For movement heuristics, start in observation mode and calibrate against legitimate play before punitive activation. For confirmed protocol violations, exercise the kick path in a controlled test before deployment. Keep logs and per-player state bounded and clean them on player removal/character replacement as appropriate.

Stop when the agreed outcomes are protected and verified at the available layers. Do not expand into a universal anti-cheat framework, publish, install globally, or alter unrelated gameplay without authorization.
