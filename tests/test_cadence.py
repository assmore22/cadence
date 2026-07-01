"""Tests for CADENCE (direct runner). AI check() validated live on studionet."""
from pathlib import Path

CONTRACT = str(Path(__file__).resolve().parents[1] / "contracts" / "cadence.py")
GEN = 10 ** 18
S_ACTIVE = 0; S_BREACHED = 1; S_CLOSED = 2
SUB = "0x" + "33" * 20


def _create(c, vm, who, service="Docs site", url="https://example.com",
            cond="The page loads and shows the notice", sub=SUB, bond=5):
    vm.sender = who; vm.value = bond * GEN
    sid = c.create_sla(service, url, cond, sub)
    vm.value = 0
    return sid


def test_create_sla(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    sid = _create(c, direct_vm, direct_alice)
    assert sid == 0
    s = c.get_sla(0)
    assert s["status"] == S_ACTIVE
    assert int(s["bond"]) == 5 * GEN
    assert s["checks"] == 0


def test_create_requires_bond(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    direct_vm.sender = direct_alice; direct_vm.value = 0
    with direct_vm.expect_revert("post a bond"):
        c.create_sla("svc", "https://x.com", "cond", SUB)


def test_create_requires_service(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    direct_vm.sender = direct_alice; direct_vm.value = GEN
    with direct_vm.expect_revert("a service name is required"):
        c.create_sla("", "https://x.com", "cond", SUB)
    direct_vm.value = 0


def test_close(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    _create(c, direct_vm, direct_alice)
    direct_vm.sender = direct_alice
    c.close(0)
    assert c.get_sla(0)["status"] == S_CLOSED


def test_only_provider_closes(deploy, direct_vm, direct_alice, direct_bob):
    c = deploy(CONTRACT)
    _create(c, direct_vm, direct_alice)
    direct_vm.sender = direct_bob
    with direct_vm.expect_revert("only the provider can close"):
        c.close(0)


def test_check_bad_id(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("no such SLA"):
        c.check(0)


def test_multiple(deploy, direct_vm, direct_alice):
    c = deploy(CONTRACT)
    _create(c, direct_vm, direct_alice, service="Svc A")
    _create(c, direct_vm, direct_alice, service="Svc B")
    assert c.get_sla_count() == 2
    assert c.get_sla(1)["service"] == "Svc B"
