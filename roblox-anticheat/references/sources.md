# Official research map

Research date: **2026-10-03**. These are source pointers and synthesis caveats, not a frozen API contract. Re-fetch the relevant pages when implementing. Index/page `last_updated` values observed in initial research were 2026-10-02; site export timestamps do not prove when an engine feature shipped.

| Source | Use |
|---|---|
| https://create.roblox.com/docs/llms.txt | Concept index and documented search interface |
| https://create.roblox.com/docs/reference/engine/llms.txt | Engine API discovery |
| https://create.roblox.com/docs/reference/engine/deprecated.md | Deprecated API inventory |
| https://create.roblox.com/docs/en-us/scripting/security/security-tactics.md | Client control and fundamental trust model |
| https://create.roblox.com/docs/en-us/scripting/security/defensive-design.md | Prevent harmful outcomes through design |
| https://create.roblox.com/docs/en-us/scripting/security/client-server-boundary.md | Validation, rate limits, interactions, economy and purchases |
| https://create.roblox.com/docs/en-us/scripting/security/network-ownership.md | Physics authority and movement-validation limits |
| https://create.roblox.com/docs/en-us/scripting/security/server-side-detection.md | Evidence, heuristics, honeypots, consequences |
| https://create.roblox.com/docs/en-us/scripting/security/access-control.md | Replication, confidentiality, secure place access |
| https://create.roblox.com/docs/en-us/scripting/security/third-party-vulnerabilities.md | Asset backdoors and sandboxing |
| https://create.roblox.com/docs/en-us/projects/server-authority.md | Engine prediction/rollback model and requirements |
| https://create.roblox.com/docs/en-us/physics/network-ownership.md | Ownership API and performance tradeoffs |
| https://create.roblox.com/docs/en-us/scripting/capabilities.md | Current script-capability/sandbox restrictions |

## Retrieval

Roblox documents `/docs/api/search/<percent-encoded question>` returning JSON with Markdown URLs. A response containing `error` is not an empty successful search. The helper validates that returned URLs stay on the official host. If the endpoint changes, use indexes or available documentation tools rather than guessed URL patterns.

Never load the monolithic `llms-full.txt`. Fetch only selected pages. Engine APIs used inside an experience and external Open Cloud HTTP APIs are different systems.

## Caveats that change implementation decisions

- Server-side remote validation is essential regardless of whether Engine Server Authority is enabled. They are different concepts.
- The security movement page labels Server Authority beta; the dedicated guide describes concrete setup. Confirm project/runtime support before recommending it, and do not migrate incidentally.
- The client-server-boundary page contains a relay example that checks NaN only in Vector3.X and uses older-style time examples. This is not complete production vector validation. Check all relevant components and current clock semantics.
- The same page recommends `math.isfinite`; verify the target Luau API rather than replacing it based on older memory.
- The detection guide describes cadence heuristics. This skill treats cadence as weak evidence, not proof warranting a kick or ban, to preserve legitimate/accessibility-assisted play.
- Third-party sandbox/capability features have rollout caveats. Inspect assets even when sandboxing is available; popularity is not a security guarantee.

## Skill creation tooling

Vercel Skills CLI: https://github.com/vercel-labs/skills

The initial template is created with `npx skills init roblox-anticheat`. Discover the local source with `npx skills add ./roblox-anticheat --list`. Installation/publishing is separate from creation and requires user approval for its destination.

The retrieval and verification approach was informed by `luau-script-hub`. This skill's instructions and Python helper are independent; no executor tooling or files from that skill are required or copied.
