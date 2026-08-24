import importlib.util
import json
from datetime import date
from pathlib import Path

MODULE_PATH = Path(__file__).parents[1] / "collector.py"
spec = importlib.util.spec_from_file_location("l3_004_collector", MODULE_PATH)
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)


class Response:
    def __init__(self, payload): self.content = json.dumps(payload, separators=(",", ":")).encode()
    def raise_for_status(self): pass


class Session:
    def __init__(self, payloads): self.payloads = iter(payloads); self.urls = []
    def get(self, url): self.urls.append(url); return Response(next(self.payloads))


def test_fetch_cme_preserves_actual_trade_date():
    payload = {"empty":False,"tradeDate":"08/21/2026","settlements":[],"reportType":"Final"}
    content, returned, actual, url = module.fetch_cme(date(2026,8,21),Session([payload]))
    assert json.loads(content) == payload and returned == payload
    assert actual == date(2026,8,21) and "08/21/2026" in url


def test_fetch_cme_falls_back_without_synthetic_date():
    empty={"empty":True,"tradeDate":"08/23/2026","settlements":[]}
    actual={"empty":False,"tradeDate":"08/21/2026","settlements":[]}
    session=Session([empty,actual]); _,_,trade_date,_=module.fetch_cme(date(2026,8,23),session)
    assert trade_date == date(2026,8,21) and "08/21/2026" in session.urls[-1]
