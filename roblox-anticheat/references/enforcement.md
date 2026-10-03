# Evidence and enforcement

## Default policy

**Kick confirmed cheaters from the server by default.** Do not silently turn that preference into "never kick." At the same time, rejecting a request and proving cheating are distinct decisions. Bans, position correction, and client-side anti-tamper punishments are not default behaviors.

Before coding new punitive rules, ask for the unresolved choices in SKILL.md, show proposed evidence and exclusions, and obtain acceptance. Keep detection, impact prevention, and consequence execution separately testable within the existing project; they need not be separate modules.

## Evidence classes

| Evidence | Meaning | Default action |
|---|---|---|
| Bad type, expired/stale interaction, missing permission, rate burst | Request invalid; buggy or desynced legitimate clients remain possible | Drop, bounded log |
| One position jump, fast completion, regular cadence, client anti-tamper alert | Weak/context-dependent signal | Observe; deny only an independently invalid protected action |
| Repeated correlated heuristics | Increased suspicion, not automatic proof | Review/corroborate against allowed mechanics; no automatic escalation by count alone |
| Approved server-observed protocol violation with no legitimate route in the supported build | High-confidence evidence after integration checks | **Server kick** |
| Explicitly approved ban rule and sufficiently reliable evidence | Authorized escalation | Chosen temporary/permanent ban |

An example of the fourth class is a client firing a truly server-to-client-only remote or an existing never-used-by-legitimate-clients honeypot. First audit all callers and builds, test directionality, exclude legacy/debug paths, and verify the rule actually cannot be reached normally. Names alone do not establish direction. Do not create decoys just to manufacture a kick rule without approval.

If no proposed rule meets the high-confidence bar, state that clearly: implement protective rejection and retain the agreed kick policy for later confirmed rules, rather than weakening the evidence threshold to ensure kicks happen.

## Consequence implementation

- Execute `Player:Kick` only on the server after the approved evidence predicate. Verify its current API before using it. Ensure the target is the originating player, not an ID supplied by a different client.
- Exercise the actual kick path with a controlled Studio test account. Test legal near-misses that must not call it.
- Keep client alerts as supplementary telemetry at most; missing/tampered heartbeats can also be disconnects or disabled code, not proof.
- For bans, verify the current Ban API, configuration, universe/place scope, duration, alternate-account options, public/private reason fields, failure behavior, and unban procedure. Do not enable a broad scope or alternate-account ban by accident.
- Handle a failed sanction API call explicitly. A successful `pcall` alone does not prove every protected action or persistent consequence completed; use the API's documented completion/error contract and observable result where available.
- Make repeated processing idempotent and bounded. Do not spawn sanctions or logs indefinitely.

## Logging and rollout

Record only what is needed: server player identity, rule/version, server time, evidence and relevant allowed-mechanic context, consequence, and result. Bound memory, write volume, and retention. Do not persist every movement sample or disclose internal evidence details in a client-facing kick message.

New heuristics start in observation mode, calibrated against legitimate play. Approved confirmed rules can activate kicks after controlled proof; observation-only rollout is not an excuse to omit the agreed kick implementation. Track rejection/kick rates and review unexpected increases after releases.

Expose a narrow server-side disable/configuration switch consistent with the project. Keep protective validation active if a punitive rule is disabled. Document how to reverse a mistaken ban and investigate its evidence. Never claim that tuning eliminates every possible false positive.
