# User stories & acceptance criteria

Use these to design test cases (TestRail), traceability, and automated scripts.

**US-1 Registration & login**
- A new user can register with a valid email and a password of 6+ characters; duplicate emails are rejected.
- Login returns a token (API) / sets a session (UI). Wrong credentials are rejected without revealing which field was wrong.
- Requests with a missing, malformed, tampered, or **expired** token are rejected with 401.

**US-2 Browse & search**
- Products can be listed, searched by name, and filtered by category (UI and API).
- Stock is shown; out-of-stock products cannot be added to the cart.

**US-3 Cart**
- A logged-in user can add items (quantity 1–20), see per-line and subtotal prices, and remove items.
- A user cannot add more units than are in stock.

**US-4 Pricing & checkout**
- Order of operations: subtotal → tier discount → coupon discount → tax on the discounted amount → shipping.
- Tax is rounded half-up, once, on the whole order. Discounts never push the taxable amount below zero.
- `FREESHIP` waives shipping when the subtotal **meets or exceeds** its minimum.
- `FLAT5` and the minimum-subtotal rules apply only when the subtotal qualifies. `ONCE` can be used by only one order.
- The checkout page's "Update totals" preview must match what the order is finally charged.

**US-3/4 Payment & order lifecycle**
- Placing an order creates it as `PENDING`, reserves stock, and clears the cart. The payment result arrives
  asynchronously: success → `PAID` (confirmation email), decline → `PAYMENT_FAILED` (stock returned, email).
- An order must **always** end in its correct final state.
- `PENDING` or `PAID` orders can be cancelled → `CANCELLED`, stock returned. Only `PAID` orders can be refunded → `REFUNDED`.
- Cancel/refund must be reflected everywhere: API response, database, order page, order history.

**US-5 Inventory integrity**
- Stock is never negative. When several customers try to buy the last unit at the same moment, exactly one succeeds.

**US-6 Order history**
- Users see only their own orders. Totals, status and line items match the order detail and the API.

**US-7 Quality gate (your delivery)**
- Every story above maps to test cases and automated scripts; the pipeline publishes a report and a clear go/no-go.
