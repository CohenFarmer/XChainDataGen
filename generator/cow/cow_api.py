import hashlib
import requests

COW_API_BASE = {
    "ethereum": ["https://api.cow.fi/mainnet"],
    "arbitrum": ["https://api.cow.fi/arbitrum", "https://api.cow.fi/arb1", "https://api.cow.fi/arbitrum_one"],
    "base": ["https://api.cow.fi/base"],
    "optimism": ["https://api.cow.fi/optimism"],
    "polygon": ["https://api.cow.fi/polygon"],
}

def _normalize_uid(uid: str) -> str:
    if not uid:
        return uid
    u = uid.lower()
    return u if u.startswith("0x") else f"0x{u}"

def get_order(blockchain: str, uid: str) -> dict | None:
    bases = COW_API_BASE.get(blockchain) or []
    if isinstance(bases, str):
        bases = [bases]
    uid = _normalize_uid(uid)

    last_status = None
    for base in bases:
        try:
            url = f"{base}/api/v1/orders/{uid}"
            r = requests.get(url, timeout=10, headers={"User-Agent": "XChainDataGen/1.0"})
            last_status = r.status_code
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None

def fetch_appdata_json(cid: str) -> dict | None:
    if not cid:
        return None
    for base in ("https://gateway.cow.fi/ipfs", "https://ipfs.io/ipfs"):
        try:
            r = requests.get(f"{base}/{cid}", timeout=10, headers={"User-Agent": "XChainDataGen/1.0"})
            if r.status_code == 200:
                return r.json()
        except Exception:
            pass
    return None

def derive_cross_chain_key(order_json: dict, appdata_json: dict | None) -> str | None:
    if not order_json:
        return None
    fields = []
    if appdata_json:
        fields.extend([
            appdata_json.get("intentId"),
            (appdata_json.get("xchain") or {}).get("intentId") if isinstance(appdata_json.get("xchain"), dict) else None,
            (appdata_json.get("metadata") or {}).get("intentId") if isinstance(appdata_json.get("metadata"), dict) else None,
            (appdata_json.get("metadata") or {}).get("quoteId") if isinstance(appdata_json.get("metadata"), dict) else None,
        ])
    fields.extend([order_json.get("appDataCid"), order_json.get("appData")])
    for f in fields:
        if f:
            return str(f)
    return None

def derive_fallback_key(owner: str, sell_token: str, buy_token: str, sell_amount: str | int, buy_amount: str | int, valid_to: int) -> str:
    # Deterministic composite; hash to keep it compact
    parts = [
        (owner or "").lower(),
        (sell_token or "").lower(),
        (buy_token or "").lower(),
        str(sell_amount),
        str(buy_amount),
        str(valid_to or 0),
    ]
    raw = "|".join(parts).encode("utf-8")
    return "fallback:" + hashlib.sha256(raw).hexdigest()