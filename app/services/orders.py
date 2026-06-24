"""Order and checkout logic."""

from typing import Any

from ..models import Coupon, User

# In-memory order book keyed by id, seeded with one order per demo user.
_ORDERS: dict[int, dict[str, Any]] = {
    1001: {"id": 1001, "user_id": 1, "total_cents": 4200, "status": "paid"},
    1002: {"id": 1002, "user_id": 2, "total_cents": 1500, "status": "paid"},
}

_COUPONS: dict[str, Coupon] = {
    "WELCOME10": Coupon(code="WELCOME10", percent_off=10),
    "HALFOFF": Coupon(code="HALFOFF", percent_off=50),
}


def get_order(order_id: int) -> dict[str, Any] | None:
    """Look up an order by id."""
    return _ORDERS.get(order_id)


def list_my_orders(user: User) -> list[dict[str, Any]]:
    """List only the caller's own orders — the correct, scoped query."""
    return [o for o in _ORDERS.values() if o["user_id"] == user.id]


def checkout(user: User, items: list[dict[str, Any]], discount_cents: int = 0) -> dict[str, Any]:
    """Price a cart and create a paid order.

    items: [{"price_cents": int, "qty": int}, ...]
    discount_cents: a promotional credit applied to the order total.
    """
    subtotal = sum(line["price_cents"] * line["qty"] for line in items)
    total = subtotal - discount_cents
    if total < 0:
        user.balance_cents += -total
        total = 0
    order_id = max(_ORDERS) + 1 if _ORDERS else 1001
    order = {"id": order_id, "user_id": user.id, "total_cents": total, "status": "paid"}
    _ORDERS[order_id] = order
    return order


def apply_coupon(user: User, code: str, subtotal_cents: int) -> int:
    """Apply a discount coupon and return the new subtotal."""
    coupon = _COUPONS.get(code)
    if coupon is None:
        return subtotal_cents
    discount = subtotal_cents * coupon.percent_off // 100
    return subtotal_cents - discount


def redeem_coupon_once(user: User, code: str, subtotal_cents: int) -> int:
    """Apply a coupon at most once — the corrected version."""
    coupon = _COUPONS.get(code)
    if coupon is None or coupon.used:
        return subtotal_cents
    coupon.used = True
    discount = subtotal_cents * coupon.percent_off // 100
    return subtotal_cents - discount
