import os
import re
from typing import Dict, Optional

import requests

class SupportedChainId:
    MAINNET = 1
    OPTIMISM = 10
    ARBITRUM_ONE = 42161
    POLYGON = 137
    BASE = 8453


SUBGRAPH_ENDPOINT_BY_CHAIN_ID: Dict[int, str] = {
    SupportedChainId.MAINNET: "https://api.thegraph.com/subgraphs/name/cowprotocol/cow",
    SupportedChainId.ARBITRUM_ONE: "https://api.thegraph.com/subgraphs/name/cowprotocol/cow-arbitrum",
    SupportedChainId.BASE: "https://api.thegraph.com/subgraphs/name/cowprotocol/cow-base",
    SupportedChainId.OPTIMISM: "https://api.thegraph.com/subgraphs/name/cowprotocol/cow-optimism",
    SupportedChainId.POLYGON: "https://api.thegraph.com/subgraphs/name/cowprotocol/cow-polygon",
}

CHAIN_NAME_TO_ID: Dict[str, int] = {
    "ethereum": SupportedChainId.MAINNET,
    "mainnet": SupportedChainId.MAINNET,
    "arbitrum": SupportedChainId.ARBITRUM_ONE,
    "arbitrum_one": SupportedChainId.ARBITRUM_ONE,
    "optimism": SupportedChainId.OPTIMISM,
    "polygon": SupportedChainId.POLYGON,
    "base": SupportedChainId.BASE,
}

_ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_LOG_FILE = os.path.join(_ROOT_DIR, "error_log.log")
_SESSION: Optional[requests.Session] = None


def _log_line(msg: str) -> None:
    try:
        with open(_LOG_FILE, "a", encoding="utf-8") as f:
            f.write(msg + "\n")
    except Exception:
        pass


def _session() -> requests.Session:
    global _SESSION
    if _SESSION is not None:
        return _SESSION
    s = requests.Session()
    s.headers.update({
        "User-Agent": "XChainDataGen/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json",
    })
    _SESSION = s
    return s


class SubgraphApi:
    """Lightweight Subgraph client with a run_query method.

    Example usage:
        api = SubgraphApi({ 'chainId': SupportedChainId.ARBITRUM_ONE })
        result = api.run_query('{ trades(first: 5) { id } }')
    """

    def __init__(self, config: Dict[str, int]):
        chain_id = config.get("chainId") if isinstance(config, dict) else None
        if not isinstance(chain_id, int):
            raise ValueError("SubgraphApi requires config with integer 'chainId'")
        endpoint = SUBGRAPH_ENDPOINT_BY_CHAIN_ID.get(chain_id)
        if not endpoint:
            raise ValueError(f"Unsupported chain id: {chain_id}")
        self.chain_id = chain_id
        self.endpoint = endpoint

    def run_query(self, query: str, variables: Optional[dict] = None, timeout: int = 30) -> dict:
        try:
            resp = _session().post(self.endpoint, json={"query": query, "variables": variables or {}}, timeout=timeout)
            if resp.status_code != 200:
                _log_line(f"COW_SUBGRAPH non200 chainId={self.chain_id} status={resp.status_code}")
                return {}
            data = resp.json()
            return data or {}
        except Exception as e:
            _log_line(f"COW_SUBGRAPH exception chainId={self.chain_id} err={type(e).__name__}:{e}")
            return {}


def extract_cid(value: Optional[str]) -> Optional[str]:
    """Extract a probable IPFS CID from appData if it's an IPFS URL or a bare CID."""
    if not value or not isinstance(value, str):
        return None
    v = value.strip()
    if v.lower().startswith("ipfs://"):
        v = v[7:]
        if v.lower().startswith("ipfs/"):
            v = v[5:]
    m = re.search(r"/ipfs/([A-Za-z0-9]+)", v)
    if m:
        v = m.group(1)
    if (v.startswith("Qm") and len(v) >= 46) or (v.startswith("baf") and len(v) >= 46):
        return v
    return None


def get_order(blockchain: str, uid: str) -> Optional[dict]:
    """Subgraph-only order fetch. Returns {'appData', 'appDataCid'} or None."""
    try:
        chain_id = CHAIN_NAME_TO_ID.get((blockchain or "").lower())
        if not chain_id or not uid:
            return None
        api = SubgraphApi({"chainId": chain_id})
        query = "query ($id: ID!) { order(id: $id) { id appData } }"
        out = api.run_query(query, variables={"id": uid.lower()})
        order = (out or {}).get("data", {}).get("order")
        if not order:
            return None
        app_data = order.get("appData")
        return {
            "appData": app_data,
            "appDataCid": extract_cid(app_data) if app_data else None,
        }
    except Exception as e:
        _log_line(f"COW_SUBGRAPH get_order exception chain={blockchain} uid={uid} err={type(e).__name__}:{e}")
        return None

