# Touch and other client-triggered interactions

## Touch rewards

Treat `Touched` as a notification to consider an action, not proof of legitimate contact. Executor interactions can manipulate the client-controlled physics/event surface; production code only uses official Studio APIs.

1. Resolve the touching part to the player's current character using the project's supported character structure. Verify current membership, required alive state, and the intended target.
2. Check the server's reward eligibility, objective sequence, and target active state. For sequential checkpoints, completing the last checkpoint is not sufficient.
3. Use server-side spatial plausibility where appropriate, with game-specific tolerances. Proximity alone is insufficient when the character or target can be teleported by client-owned physics.
4. For critical static pickups/checkpoints, inspect ownership and anchoring. Anchor or manage ownership only for the relevant target if compatible with gameplay; do not anchor every object or take over all player physics.
5. Deduplicate according to the mechanic: once per pickup, per player, per round, or a real cooldown. Multiple body-part touches are ordinary behavior. Reserve the reward before yielding, and avoid double granting from different handlers.
6. Verify normal contact still works. Touch failure or missing events are not cheating evidence; use another authoritative gameplay signal only if the requested feature needs it.

Distance evidence from client-owned positions cannot by itself prove that a legal journey occurred. If rewards depend on a journey, validate prerequisites or an approved movement policy rather than quietly adding movement restrictions.

## Prompts, clicks, and drags

Consult the current client-server-boundary documentation for the exact event. As researched on 2026-10-03:

- Only `ProximityPrompt.Triggered` has the documented server-side distance check; hold/begin/end events do not inherit that guarantee.
- Prompt properties changed on the client do not establish server authorization. Validate server-enabled state, permission, distance, timing if required, and rate.
- ClickDetector events have no documented server range checks to rely on.
- Drag events check some properties, not every gameplay requirement; inherited click events differ from drag events.

Avoid treating every event as equally secured. A built-in check does not replace your game's permission, ownership, state, or replay checks. Unanchored interaction targets can be moved near the character by a network owner.

## Consequences and tests

Reject impossible/unauthorized interaction attempts without rewards. An out-of-range event can also indicate latency, a stale handler, legitimate multiple contacts, or a project bug; do not kick automatically from that alone.

Test legal touch, repeated body-part events, two players on one pickup, instant repeated requests, respawn, removed target, unauthorized reward, moved unanchored target, and remote/interaction paths granting the same reward. Test that the server commits at most the intended reward count and preserves ordinary interaction timing.
