from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path

from . import services as svc
from .pricing import SHIPPING_CENTS, TAX_RATES
from .security import create_token, verify_token

templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))
router = APIRouter()


def money(cents: int) -> str:
    return f"${cents / 100:,.2f}"


templates.env.filters["money"] = money


def _user(request: Request) -> Optional[dict]:
    token = request.cookies.get("token")
    uid = verify_token(token) if token else None
    return svc.get_user(uid) if uid else None


def render(request: Request, name: str, status_code: int = 200, **ctx):
    return templates.TemplateResponse(request, name, {"user": _user(request), **ctx}, status_code=status_code)


def _login_redirect():
    return RedirectResponse("/login", status_code=303)


@router.get("/", response_class=HTMLResponse)
def home(request: Request, category: Optional[str] = None, q: Optional[str] = None):
    products = svc.list_products(category or None, q or None)
    categories = sorted({p["category"] for p in svc.list_products()})
    return render(request, "products.html", products=products, categories=categories, category=category, q=q or "")


@router.get("/products/{product_id}", response_class=HTMLResponse)
def product_page(request: Request, product_id: int):
    try:
        return render(request, "product.html", product=svc.get_product(product_id), error=None)
    except svc.ApiError as e:
        return render(request, "error.html", status_code=e.status, message=e.message)


@router.get("/register", response_class=HTMLResponse)
def register_form(request: Request):
    return render(request, "register.html", error=None)


@router.post("/register")
def register_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        svc.register_user(email, password)
    except svc.ApiError as e:
        return render(request, "register.html", status_code=e.status, error=e.message)
    return RedirectResponse("/login?registered=1", status_code=303)


@router.get("/login", response_class=HTMLResponse)
def login_form(request: Request, registered: Optional[str] = None):
    return render(request, "login.html", error=None, registered=bool(registered))


@router.post("/login")
def login_submit(request: Request, email: str = Form(...), password: str = Form(...)):
    try:
        user = svc.authenticate(email, password)
    except svc.ApiError as e:
        return render(request, "login.html", status_code=e.status, error=e.message, registered=False)
    resp = RedirectResponse("/", status_code=303)
    resp.set_cookie("token", create_token(user["id"]), httponly=True, samesite="lax")
    return resp


@router.post("/logout")
def logout():
    resp = RedirectResponse("/", status_code=303)
    resp.delete_cookie("token")
    return resp


@router.post("/cart/add")
def cart_add(request: Request, product_id: int = Form(...), qty: int = Form(1)):
    user = _user(request)
    if not user:
        return _login_redirect()
    try:
        svc.add_to_cart(user["id"], product_id, qty)
    except svc.ApiError as e:
        return render(request, "product.html", status_code=e.status, product=svc.get_product(product_id), error=e.message)
    return RedirectResponse("/cart", status_code=303)


@router.get("/cart", response_class=HTMLResponse)
def cart_page(request: Request):
    user = _user(request)
    if not user:
        return _login_redirect()
    lines = svc.cart_lines(user["id"])
    return render(request, "cart.html", lines=lines, subtotal=sum(l["price_cents"] * l["qty"] for l in lines))


@router.post("/cart/remove")
def cart_remove(request: Request, product_id: int = Form(...)):
    user = _user(request)
    if not user:
        return _login_redirect()
    svc.remove_from_cart(user["id"], product_id)
    return RedirectResponse("/cart", status_code=303)


def _checkout_ctx(user, region="IN", shipping="standard", coupon="", error=None, quote=None):
    return dict(regions=sorted(TAX_RATES), methods=sorted(SHIPPING_CENTS), region=region, shipping=shipping,
                coupon=coupon, error=error, quote=quote)


@router.get("/checkout", response_class=HTMLResponse)
def checkout_page(request: Request):
    user = _user(request)
    if not user:
        return _login_redirect()
    return render(request, "checkout.html", **_checkout_ctx(user), lines=svc.cart_lines(user["id"]))


@router.post("/checkout")
def checkout_submit(request: Request, region: str = Form("IN"), shipping_method: str = Form("standard"),
                    coupon_code: str = Form(""), card_number: str = Form(""), action: str = Form("pay")):
    user = _user(request)
    if not user:
        return _login_redirect()
    lines = svc.cart_lines(user["id"])
    try:
        if action == "quote":
            quote = svc.quote(user["id"], region, shipping_method, coupon_code or None)
            return render(request, "checkout.html", lines=lines,
                          **_checkout_ctx(user, region, shipping_method, coupon_code, None, quote))
        order = svc.checkout(user["id"], region, shipping_method, coupon_code or None, card_number)
    except svc.ApiError as e:
        return render(request, "checkout.html", status_code=e.status, lines=lines,
                      **_checkout_ctx(user, region, shipping_method, coupon_code, e.message))
    return RedirectResponse(f"/orders/{order['id']}", status_code=303)


@router.get("/orders", response_class=HTMLResponse)
def orders_page(request: Request):
    user = _user(request)
    if not user:
        return _login_redirect()
    return render(request, "orders.html", orders=svc.list_orders(user["id"]))


@router.get("/orders/{order_id}", response_class=HTMLResponse)
def order_page(request: Request, order_id: int):
    user = _user(request)
    if not user:
        return _login_redirect()
    try:
        return render(request, "order.html", order=svc.get_order(order_id, user["id"]), message=None)
    except svc.ApiError as e:
        return render(request, "error.html", status_code=e.status, message=e.message)


@router.post("/orders/{order_id}/cancel")
def order_cancel(request: Request, order_id: int):
    user = _user(request)
    if not user:
        return _login_redirect()
    try:
        svc.cancel_order(order_id, user["id"])
    except svc.ApiError as e:
        return render(request, "order.html", status_code=e.status, order=svc.get_order(order_id, user["id"]), message=e.message)
    return RedirectResponse(f"/orders/{order_id}", status_code=303)
