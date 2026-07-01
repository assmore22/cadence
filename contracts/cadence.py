# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
"""
CADENCE - SLA / Uptime Escrow
=============================
A provider backs a service-level promise with a bond. They name the endpoint to
watch, what "healthy" means in plain English, and the subscriber who is covered.
Anyone can run a check: the contract reads the endpoint and a validator set
agrees (Equivalence Principle) whether the service is healthy. Healthy checks
build an on-chain uptime record. The first time a check finds the service in
breach, the bond is paid to the subscriber automatically. If the term ends with
no breach, the provider closes the SLA and reclaims the bond.

Status:  ACTIVE(0) -> BREACHED(1, bond paid to subscriber) | CLOSED(2, bond returned)
"""

from genlayer import *
from dataclasses import dataclass
import json
import typing


S_ACTIVE = 0
S_BREACHED = 1
S_CLOSED = 2


@allow_storage
@dataclass
class Sla:
    provider: Address
    subscriber: Address
    service: str
    endpoint_url: str
    healthy_condition: str
    bond: u256
    status: u8
    checks: u256
    healthy_checks: u256
    last_result: str


class Cadence(gl.Contract):
    slas: DynArray[Sla]

    def __init__(self) -> None:
        pass

    @gl.public.write.payable
    def create_sla(self, service: str, endpoint_url: str, healthy_condition: str, subscriber: str) -> int:
        if len(service.strip()) == 0:
            raise gl.vm.UserError("a service name is required")
        if len(endpoint_url.strip()) == 0:
            raise gl.vm.UserError("an endpoint URL is required")
        if len(healthy_condition.strip()) == 0:
            raise gl.vm.UserError("a healthy condition is required")
        bond = gl.message.value
        if bond == u256(0):
            raise gl.vm.UserError("post a bond to back the SLA")
        s = self.slas.append_new_get()
        s.provider = gl.message.sender_address
        s.subscriber = Address(subscriber)
        s.service = service
        s.endpoint_url = endpoint_url
        s.healthy_condition = healthy_condition
        s.bond = bond
        s.status = u8(S_ACTIVE)
        s.checks = u256(0)
        s.healthy_checks = u256(0)
        s.last_result = ""
        return len(self.slas) - 1

    @gl.public.write
    def check(self, sla_id: int) -> None:
        """Read the endpoint; validators agree whether the service is healthy.
        A breach pays the bond to the subscriber."""
        s = self._get(sla_id)
        if s.status != S_ACTIVE:
            raise gl.vm.UserError("SLA is not active")

        url = s.endpoint_url
        condition = s.healthy_condition

        def leader_fn() -> str:
            page = ""
            try:
                page = gl.nondet.web.get(url).body.decode("utf-8")[:6000]
            except Exception:
                page = "(endpoint unreachable)"
            prompt = (
                f"Service healthy condition: {condition}\n\n"
                f"Current endpoint content:\n{page}\n\n"
                "Judge strictly on what the endpoint shows right now. Is the "
                "service HEALTHY (meeting the condition)? Reply with ONLY JSON: "
                "{\"healthy\": true} if it is healthy, {\"healthy\": false} if it is "
                "in breach, plus a short \"reason\"."
            )
            return gl.nondet.exec_prompt(prompt)

        def validator_fn(leader_res) -> bool:
            if not isinstance(leader_res, gl.vm.Return):
                return False
            return self._decision_of(leader_res.calldata)[0] == self._decision_of(leader_fn())[0]

        result = gl.vm.run_nondet_unsafe(leader_fn, validator_fn)
        healthy, reason = self._decision_of(result)
        s.checks = s.checks + u256(1)
        s.last_result = reason[:300]
        if healthy:
            s.healthy_checks = s.healthy_checks + u256(1)
        else:
            s.status = u8(S_BREACHED)
            self._pay(s.subscriber, s.bond)

    @gl.public.write
    def close(self, sla_id: int) -> None:
        s = self._get(sla_id)
        if s.status != S_ACTIVE:
            raise gl.vm.UserError("only an active SLA can be closed")
        if gl.message.sender_address != s.provider:
            raise gl.vm.UserError("only the provider can close")
        s.status = u8(S_CLOSED)
        self._pay(s.provider, s.bond)

    # ------------------------------------------------------------------ views
    @gl.public.view
    def get_sla_count(self) -> int:
        return len(self.slas)

    @gl.public.view
    def get_sla(self, sla_id: int) -> dict:
        s = self._get(sla_id)
        return {
            "provider": s.provider.as_hex,
            "subscriber": s.subscriber.as_hex,
            "service": s.service,
            "endpoint_url": s.endpoint_url,
            "healthy_condition": s.healthy_condition,
            "bond": str(s.bond),
            "status": int(s.status),
            "checks": int(s.checks),
            "healthy_checks": int(s.healthy_checks),
            "last_result": s.last_result,
        }

    # -------------------------------------------------------------- internals
    def _get(self, sla_id: int) -> Sla:
        if sla_id < 0 or sla_id >= len(self.slas):
            raise gl.vm.UserError("no such SLA")
        return self.slas[sla_id]

    def _decision_of(self, result: typing.Any) -> tuple:
        data = result
        if isinstance(data, str):
            data = self._extract_json(data)
        if not isinstance(data, dict):
            return (False, "")
        raw = data.get("healthy", None)
        reason = str(data.get("reason", ""))
        if isinstance(raw, bool):
            return (raw, reason)
        if isinstance(raw, str):
            return (raw.strip().lower() == "true", reason)
        return (False, reason)

    def _extract_json(self, text: str) -> typing.Any:
        try:
            return json.loads(text)
        except (ValueError, TypeError):
            pass
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except (ValueError, TypeError):
                return None
        return None

    def _pay(self, recipient: Address, amount: u256) -> None:
        if amount == u256(0):
            return
        _Payee(recipient).emit_transfer(value=amount)


@gl.evm.contract_interface
class _Payee:
    class View:
        pass

    class Write:
        pass
