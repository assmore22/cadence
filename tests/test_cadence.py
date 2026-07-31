"""Executable Cadence V2 payout and dispute-lifecycle tests."""
import json
from pathlib import Path

CONTRACT = str(Path(__file__).resolve().parents[1] / "contracts" / "cadence_v2.py")

def _setup(deploy, vm, owner, subscriber):
    vm.warp("2026-07-16T12:00:00Z")
    vm.sender = owner
    contract = deploy(CONTRACT)
    record_id = contract.draft_sla("Public API", "https://example.com", "Endpoint reports healthy", "0x" + subscriber.hex(), "0")
    return contract, record_id

def _review(vm):
    vm.mock_llm(r"Cadence V2, a neutral", json.dumps({"outcome":"healthy","confidenceBps":8500,"healthBps":9000,"summary":"Endpoint is healthy.","rationale":"Public response satisfies the SLA.","riskFlags":[],"reasoningDigest":"Healthy check."}))

def _ruling(vm, kind, ruling, revised):
    vm.mock_llm(rf"Cadence V2 resolving a {kind}", json.dumps({"ruling":ruling,"revisedOutcome":revised,"confidenceDeltaBps":-800,"reason":"Controlling evidence changed the health result.","riskFlags":[],"reasoningDigest":"Outcome revised."}))

def test_permissions_execute(deploy, direct_vm, direct_alice, direct_bob, direct_charlie):
    contract, record_id = _setup(deploy, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_charlie
    with direct_vm.expect_revert("admin_only"):
        contract.set_cadence_standard("attacker standard")
    with direct_vm.expect_revert("record_operator_only"):
        contract.add_evidence(str(record_id), "https://example.org", "probe", "outsider mutation")
    with direct_vm.expect_revert("record_operator_only"):
        contract.check_sla_with_genlayer(str(record_id))

def test_disputes_gate_bond_release_and_revise_outcome(deploy, direct_vm, direct_alice, direct_bob, direct_charlie):
    contract, record_id = _setup(deploy, direct_vm, direct_alice, direct_bob)
    direct_vm.sender = direct_alice
    _review(direct_vm)
    contract.check_sla_with_genlayer(str(record_id))
    with direct_vm.expect_revert("review_not_mature"):
        contract.check(record_id)
    contract.open_challenge_window(str(record_id))
    direct_vm.sender = direct_charlie
    challenge_id = contract.submit_challenge(str(record_id), "New incident evidence shows a breach.", "https://example.org/challenge")
    direct_vm.sender = direct_alice
    with direct_vm.expect_revert("open_filing_blocks_settlement"):
        contract.check(record_id)
    _ruling(direct_vm, "challenge", "accepted", "breach")
    contract.resolve_challenge_with_genlayer(str(record_id), challenge_id)
    assert json.loads(contract.get_sla_record(str(record_id)))["outcome"] == "breach"
    direct_vm.sender = direct_charlie
    appeal_id = contract.submit_appeal(str(record_id), "Final uptime record restores health.", "https://example.net/appeal")
    direct_vm.sender = direct_alice
    _ruling(direct_vm, "appeal", "granted", "healthy")
    contract.resolve_appeal_with_genlayer(str(record_id), appeal_id)
    direct_vm.warp("2026-07-16T13:00:01Z")
    contract.check(record_id)
    contract.close(record_id)
    record = json.loads(contract.get_sla_record(str(record_id)))
    assert record["outcome"] == "healthy"
    assert record["status"] == "CLOSED"
