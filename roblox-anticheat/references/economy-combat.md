# Economy, purchases, and combat

## Economy and duplicate rewards

1. Find the existing inventory/currency authority and persistence/session ownership mechanism. Do not create a second source of truth.
2. Resolve item IDs, prices, quantities, ownership, and reward amounts from server catalogs. Client input must not determine a final price or granted amount.
3. Validate finite positive bounded quantities and current eligibility before applying changes. Preserve intended exceptions such as legitimate free items using explicit catalog rules.
4. Serialize operations that touch the same balance/inventory through the existing service. Recheck inside that boundary; an initial check before a yield is insufficient.
5. Give grant/retry operations server-controlled idempotency where required. Define what happens when players leave, persistence fails, or the request retries. Cooldown alone is not a transaction.
6. Test concurrent buys/trades, replayed rewards, leave/rejoin, service failures, and save retries before claiming dupe prevention.

Roblox DataStore updates are not a general atomic transaction across two players' keys. Do not promise that independent `UpdateAsync` calls make trading atomic. Reuse an established protocol or explicitly scope the additional recovery/session-lock/idempotency design required. A local rollback cannot magically undo an already durable grant in another session.

Validate serializable data before mutating economic state. Bound strings/tables and reject non-finite numbers and invalid UTF-8 where applicable. Saving every rejected request would turn anti-cheat into a budget-exhaustion vector.

## Purchases

Verify the current MarketplaceService flow for the actual product type. Developer products use the server `ProcessReceipt` callback; client purchase-finished signals do not prove a receipt. Receipt processing needs durable duplicate handling and correct retry acknowledgement. Pass ownership checks have a different API; do not use a developer-product flow for all monetization.

Only add or change purchase handling when in scope. Missing persistence proof must be reported rather than claiming exact-once across servers.

## Combat

Keep existing combat feel unless a change is authorized. The server uses its weapon configuration, ownership, ammo, cooldown/reload state, team, and alive-state rules. A client-reported target or damage amount is not authoritative.

Verify origin/hit plausibility and obstruction checks with latency-aware rules appropriate to the game. The official example recommends static-geometry obstruction checks to avoid rejecting shots because other objects moved during latency. Do not invent full lag compensation or replace the weapon controller unless requested.

Do not punish solely for high accuracy, a wall-hit report, fast input cadence, or a single rejected shot. Accessibility tools, desync, and exceptional skill are legitimate near-misses. Block an unauthorized damage outcome and follow the agreed evidence policy separately.
