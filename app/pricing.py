"""Pricing rules. All money is integer cents."""
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

TAX_RATES = {"IN": Decimal("0.18"), "US": Decimal("0.08"), "EU": Decimal("0.20")}
SHIPPING_CENTS = {"standard": 500, "express": 1500}
TIER_DISCOUNT_PERCENT = {"standard": 0, "gold": 5}


def _round(value: Decimal) -> int:
    return int(value.quantize(Decimal("1"), rounding=ROUND_HALF_UP))


def coupon_discount(coupon: Optional[dict], subtotal: int) -> int:
    if not coupon:
        return 0
    if subtotal < coupon["min_subtotal_cents"]:
        return 0
    if coupon["kind"] == "percent":
        return _round(Decimal(subtotal) * coupon["value"] / 100)
    if coupon["kind"] == "flat":
        return min(coupon["value"], subtotal)
    return 0


def shipping_for(method: str, coupon: Optional[dict], subtotal: int) -> int:
    base = SHIPPING_CENTS[method]
    if coupon and coupon["kind"] == "freeship" and subtotal >= coupon["min_subtotal_cents"]:
        return 0
    return base


def price_order(lines, region: str, method: str, tier: str, coupon: Optional[dict]) -> dict:
    """lines: iterable of (unit_price_cents, qty).

    Order of operations: subtotal -> tier discount -> coupon discount -> tax on the
    discounted amount (rounded half-up, once, on the whole order) -> shipping.
    """
    subtotal = sum(price * qty for price, qty in lines)
    tier_discount = _round(Decimal(subtotal) * TIER_DISCOUNT_PERCENT[tier] / 100)
    coupon_off = coupon_discount(coupon, subtotal)
    discount = min(subtotal, tier_discount + coupon_off)
    taxable = subtotal - discount
    tax = _round(Decimal(taxable) * TAX_RATES[region])
    shipping = shipping_for(method, coupon, subtotal)
    return {
        "subtotal_cents": subtotal,
        "discount_cents": discount,
        "tax_cents": tax,
        "shipping_cents": shipping,
        "total_cents": taxable + tax + shipping,
    }
