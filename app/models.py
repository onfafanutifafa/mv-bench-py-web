"""Domain models for the shop app."""

from dataclasses import dataclass, field


@dataclass
class User:
    id: int
    username: str
    email: str
    role: str = "customer"  # "customer" | "admin"
    balance_cents: int = 0


@dataclass
class Order:
    id: int
    user_id: int
    items: list[dict] = field(default_factory=list)
    total_cents: int = 0
    status: str = "cart"  # cart | paid | shipped


@dataclass
class Coupon:
    code: str
    percent_off: int
    used: bool = False
