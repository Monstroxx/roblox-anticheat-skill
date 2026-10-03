# Optional movement and teleport checks

## Start with mechanics, not thresholds

Use only when the user requests movement protection or a protected outcome actually depends on travel. Inventory the game's server-approved teleport, dash, sprint, flight, vehicle, moving-platform, knockback, death, respawn, and administrative behaviors. Default to observing, not correcting positions or punishing.

Roblox documents no universal movement validator. With ordinary client network ownership, character physics can be manipulated; checking the server-visible `WalkSpeed` is not proof of actual travel speed.

## Minimal observation design

1. Reuse the game's existing authoritative ability/teleport service. Authorized exemptions must be created by the server, bounded in time/displacement/context, and not requested freely by the client.
2. Maintain a bounded per-current-character baseline. Reset on character replacement and verified server teleport; reject stale samples. Do not carry a dead character's location into the new character.
3. Validate finite positions and time deltas before arithmetic. Skip initialization, unusable timing, or known server-stall samples rather than dividing by zero or interpreting them as guilt.
4. Measure over windows that tolerate irregular replication. Ground games may need XZ travel checks distinct from vertical motion. Vehicles and special abilities need their own accepted movement envelope or an explicit exclusion.
5. Combine a suspected displacement with actual server-authorized mechanics and ownership context. A simple distance/time threshold is a weak signal, not confirmed cheating.
6. Keep observation and enforcement separate. A failed reward prerequisite may deny that reward without a kick. Rubber-banding, collision changes, forced ownership, or kick activation require agreement and legitimate-play testing.

Choose sampling/tolerance from measured game behavior, not invented "safe" constants. Never grant unlimited exemption because a client claims high ping. Conversely, do not interpret delayed/bunched updates as precise evidence of a teleport. Log rule version and the relevant server context, with bounded sampling.

## Ownership and physics

Inspect critical unanchored assemblies, not just the character. A client owning an object can move it, manipulate velocities, or affect others' physics. `SetNetworkOwner(nil)` or anchoring can be appropriate for a specific server-critical object, but may harm gameplay and performance; check the API and project requirements first.

A touched pickup now near the player may have moved rather than been reached legitimately. Ownership decisions and reward eligibility are separate defenses.

## Server Authority is not ordinary server validation

Roblox's Engine Server Authority model involves prediction, rollback/resimulation, simulation-access APIs, fixed simulation, and specific Workspace settings. Ordinary server-side remote validation does not mean that this physics feature is enabled.

The official security guide researched on 2026-10-03 labels Server Authority beta, while the dedicated page describes setup APIs. Verify actual availability and settings in the target Studio version. Do not enable it or replace the game's input/movement architecture as an incidental anti-cheat patch.

If explicitly implementing this model, read its current full guide. Re-simulated side effects must not duplicate rewards or persistent writes; use the documented simulation clock (`time()` in the researched guide), not arbitrary wall/CPU clocks. Client misprediction is normal and not cheating evidence.

## Acceptance matrix

Ordinary movement, high/variable latency, bunched updates, server stalls, spawn/death/respawn, every allowed teleport, repeated authorized teleport, dash, knockback, falling, moving platforms, vehicles, streaming transitions, and a synthetic impossible-position case. Report absent game mechanics as not applicable, not tested. No kick/correction should occur solely from one jump or a weak accumulated movement signal.
