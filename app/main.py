"""Shop API — FastAPI entry point.

Routes are thin: they pull the request inputs and hand them to the service
layer. The interesting behaviour (and the bugs) live in app/services and
app/utils; this file is the trust boundary where untrusted input enters.
"""

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from . import auth
from .models import User
from .services import files, net, orders, users
from .utils import crypto, serialize

app = FastAPI(title="mv-bench shop")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/users/search")
def users_search(q: str, me: User = Depends(auth.current_user)):
    return {"results": users.search_users(q)}


@app.get("/orders/{order_id}")
def read_order(order_id: int, me: User = Depends(auth.current_user)):
    order = orders.get_order(order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="not found")
    return order


@app.post("/orders/checkout")
def checkout(payload: dict, me: User = Depends(auth.current_user)):
    order = orders.checkout(me, payload.get("items", []), payload.get("discount_cents", 0))
    return {"order": order, "balance_cents": me.balance_cents}


@app.post("/coupons/apply")
def coupons_apply(payload: dict, me: User = Depends(auth.current_user)):
    new_total = orders.apply_coupon(me, payload["code"], payload["subtotal_cents"])
    return {"subtotal_cents": new_total}


@app.patch("/profile")
def patch_profile(payload: dict, me: User = Depends(auth.current_user)):
    users.update_profile(me.id, payload)
    return {"ok": True}


@app.get("/admin/stats")
def admin_stats():
    return {
        "users": users.search_users(""),
        "revenue_cents": sum(o["total_cents"] for o in orders._ORDERS.values()),
    }


@app.get("/files/download")
def download(path: str, me: User = Depends(auth.current_user)):
    return {"bytes": len(files.read_user_file(path))}


@app.post("/files/convert")
def convert(payload: dict, me: User = Depends(auth.current_user)):
    code = files.convert_to_pdf(payload["name"])
    return {"exit_code": code}


@app.get("/fetch")
def fetch(url: str, me: User = Depends(auth.current_user)):
    return net.fetch_metadata(url)


@app.get("/go")
def go(next: str):
    return RedirectResponse(net.build_redirect_target(next))


@app.post("/session/restore")
def restore(payload: dict, me: User = Depends(auth.current_user)):
    state = serialize.load_session(payload["blob"])
    return {"restored": str(state)[:200]}


@app.post("/auth/reset-token")
def reset_token(payload: dict):
    return {"token": crypto.generate_reset_token()}
