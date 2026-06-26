from __future__ import annotations

import json
import os
import time
from typing import Any
from urllib import request, error

DEFAULT_RPC_URL = "http://127.0.0.1:51234/rpc"

class RpcError(RuntimeError):
    pass

class GameKitRpcClient:
    def __init__(self, base_url: str | None = None, token: str | None = None, timeout: float = 30.0) -> None:
        self.base_url = base_url or os.environ.get("NEXUS_RPC_URL") or DEFAULT_RPC_URL
        self.token = token if token is not None else os.environ.get("NEXUS_TOKEN")
        self.timeout = timeout
        self._next_id = 1

    def call(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        rpc_id = self._next_id
        self._next_id += 1
        body = json.dumps({"jsonrpc": "2.0", "id": rpc_id, "method": method, "params": params or {}}).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["X-Nexus-Token"] = self.token
        req = request.Request(self.base_url, data=body, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except error.URLError as exc:
            raise RpcError(f"Unable to reach Nexus Game Kit RPC host at {self.base_url}: {exc}") from exc
        try:
            decoded = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RpcError(f"RPC response was not JSON: {raw[:200]}") from exc
        if isinstance(decoded, dict) and decoded.get("error"):
            raise RpcError(json.dumps(decoded["error"], indent=2, sort_keys=True))
        return decoded

    def health(self) -> dict[str, Any]:
        return self.call("nexus.health")

    def queue_check(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.call("queue.check", payload)

    def queue_submit(self, payload: dict[str, Any]) -> dict[str, Any]:
        return self.call("queue.submit", payload)

    def queue_status(self, queue_id: str) -> dict[str, Any]:
        return self.call("queue.status", {"queue_id": queue_id})

    def queue_results(self, queue_id: str) -> dict[str, Any]:
        return self.call("queue.results", {"queue_id": queue_id})

    def queue_wait(self, queue_id: str, timeout_seconds: float = 120.0, poll_seconds: float = 2.0) -> dict[str, Any]:
        try:
            return self.call("queue.wait", {"queue_id": queue_id, "timeout_seconds": timeout_seconds})
        except RpcError:
            deadline = time.monotonic() + timeout_seconds
            last_status: dict[str, Any] | None = None
            while time.monotonic() < deadline:
                last_status = self.queue_status(queue_id)
                text = json.dumps(last_status).lower()
                if any(word in text for word in ["completed", "failed", "cancelled", "rejected"]):
                    return last_status
                time.sleep(poll_seconds)
            raise RpcError(f"Queue job {queue_id} did not finish before timeout. Last status: {last_status}")
