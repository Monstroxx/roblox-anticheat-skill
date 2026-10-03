# Secure client-server entry points

## Implementation sequence

1. Find the existing handler and the authoritative state it changes. Trace every caller and legitimate payload before tightening the contract.
2. Identify the player from `OnServerEvent`/`OnServerInvoke`, not an asserted user ID in the payload. Other event families have their own contracts; verify those rather than assuming the same argument order.
3. Apply a cheap per-player/per-action ingress budget before expensive validation. Bound tracked keys, logs, concurrent jobs, and queued work. Do not create a limiter per arbitrary client-supplied string.
4. Validate exact types, allowed fields, sizes, and values. Reject unexpected structures without an unbounded recursive traversal. Check all relevant components of vectors/transforms, not just X.
5. Validate expected instance class and location, action permission, live character where required, server inventory, phase, range, and cooldown. Replicated physical positions can still be influenced by network owners.
6. Revalidate mutable prerequisites inside the existing transaction/serialization boundary, then commit exactly once. Yielding between check and mutation can invalidate a previously true condition.
7. Broadcast only a server-approved, bounded result. An effects relay is also a security boundary.
8. Clean per-player state on removal and reject stale character references after respawn. Test legal requests alongside malformed and repeated ones.

## Numeric and structural pitfalls

Type `number` includes NaN and infinities. Current documentation recommends `math.isfinite`; verify availability in the target runtime. For an older documented runtime, use an explicit finite predicate after a type check: `x == x and x > -math.huge and x < math.huge`. The equality rejects NaN; strict bounds reject infinities. Check integer and domain bounds separately.

Check every component before magnitude/distance comparisons. A NaN distance can make `distance > limit` false. Validate strings by byte budget and UTF-8 validity if persisted or processed as text. Set limits on table entries/depth if the protocol accepts tables; prefer a small known schema.

An instance-like table is not an Instance. A real Instance is not necessarily an authorized target. Prefer a stable allowed identifier resolved through a server-owned catalog when it fits the existing protocol; do not migrate a working protocol unnecessarily.

## Two different timing protections

- An ingress token bucket limits computational work and tolerates expected bursts.
- A gameplay cooldown/sequence check enforces the action's rules. Reserve/debit before yielding or launching work so parallel requests cannot all pass the same check.

Choose values from intended mechanics and measured legitimate usage. Documentation example values are not universal ceilings. Use the target's documented monotonic server time for ordinary elapsed checks; simulation-bound rollback logic has a different clock contract (see movement reference).

## Hooks and client trust

Assume an attacker can replace any client function, bypass a LocalScript check, inspect replicated code, or send arbitrary remote arguments. Do not implement client hook detection as a prerequisite for rewards or a reason to kick.

Remote-name randomization, encrypted payloads, client-shipped tokens, and obfuscation do not replace authorization. A protocol nonce may prevent accidental replay when correctly tracked server-side; possession of it does not prove the client is honest.

Avoid remotes that accept arbitrary code/module IDs, paths to modify/delete, or unchecked assets. Avoid waiting for `InvokeClient` as a security check: the client can refuse, disconnect, or lie. Verify the current API's failure/yield behavior before choosing callbacks.

## Acceptance cases

Legal request, normal burst, wrong type, NaN/±Infinity in every numeric component, oversized payload, forged/foreign instance, missing permission, stale character, repeated request, concurrent request, and spam. Rejection must not mutate protected state, relay effects, schedule unbounded work, or itself automatically punish an innocent malformed caller.
