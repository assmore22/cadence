"""Seed CADENCE with real on-chain data on studionet."""
from pathlib import Path

from gltest_cli.config.general import get_general_config
from gltest_cli.config.user import load_user_config
from gltest import get_contract_factory, get_default_account

ROOT = Path(__file__).resolve().parents[1]
ADDR = "0x8d840D186a34be7a6D638cD3BAdFd98B4E214549"
GEN = 10 ** 18
URL = "https://example.com"
SUB = "0x431ACf85256AFcb3A8c66aff96b923366D5DdaC2"

cfg = load_user_config(str(ROOT / "gltest.config.yaml"))
get_general_config().user_config = cfg
c = get_contract_factory(contract_file_path=str(ROOT / "contracts" / "cadence.py")).build_contract(
    ADDR, account=get_default_account())

SLAS = [
    ("Docs reference page", "The page loads and shows the Example Domain notice text", 5 * GEN),
    ("Payments API status", "The endpoint returns a JSON body with status 'operational' for the payments API", 4 * GEN),
]


def main():
    if c.get_sla_count().call() == 0:
        for (svc, cond, bond) in SLAS:
            c.create_sla(args=[svc, URL, cond, SUB]).transact(value=bond)
            print("created:", svc)
    for sid in (0, 1):
        s = c.get_sla(args=[sid]).call()
        if int(s["status"]) == 0:
            print("checking", sid, "(AI)...")
            try:
                c.check(args=[sid]).transact()
            except Exception as e:
                print("check", sid, "->", e)
    for sid in (0, 1):
        s = c.get_sla(args=[sid]).call()
        print(sid, ["ACTIVE", "BREACHED", "CLOSED"][int(s["status"])], "checks=", s["checks"], "healthy=", s["healthy_checks"], "|", (s["last_result"] or "")[:50])


if __name__ == "__main__":
    main()
