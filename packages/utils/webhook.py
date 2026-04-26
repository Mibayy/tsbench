import hashlib
import hmac
import json

import requests


def send_webhook(url: str, payload: dict, *, secret: str, timeout: float = 5.0) -> dict:
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    signature = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    headers = {
        "Content-Type": "application/json",
        "X-Signature": f"sha256={signature}",
    }
    try:
        response = requests.post(url, data=body, headers=headers, timeout=timeout)
        return {"status": response.status_code, "body": response.text, "error": None}
    except requests.RequestException as e:
        return {"status": 0, "body": "", "error": str(e)}
