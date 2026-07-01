# Cadence

Milestone and schedule claims with source-aware settlement.

Cadence is built for timing disputes: whether a deadline was met, a release happened, or a public milestone actually landed. The contract keeps commitments, evidence and GenLayer settlement in one timeline.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://assmore22-cadence.vercel.app |
| GitHub | https://github.com/assmore22/cadence |
| Contract | https://explorer-bradbury.genlayer.com/address/0x444E17A449fdECeEEB93eFA470C2833c7a6E3681 |

## Chain Record

- Network: GenLayer Bradbury
- Chain ID: 4221
- Contract: `0x444E17A449fdECeEEB93eFA470C2833c7a6E3681`
- Deploy transaction: [0x096e87a3...01d338](https://explorer-bradbury.genlayer.com/tx/0x096e87a333589a156b000b5c1235a43e2953f7bc9201f122edff2048a701d338)
- Deployed: `2026-07-01T15:52:01.109Z`
- Source: `contracts/cadence_v2.py` (36,749 bytes)

## Protocol Path

1. Set a timing standard.
2. Open a cadence record.
3. Attach milestone evidence.
4. Review the result.
5. Challenge or finalize the timeline.

The frontend reads milestones, open reviews, recent records and status-filtered lists. Contract state is public; write actions still require a connected wallet on GenLayer Bradbury.

## Bradbury Smoke

| Action | Transaction |
| --- | --- |
| `set_cadence_standard` | [0x28af6a3f...e97e1f](https://explorer-bradbury.genlayer.com/tx/0x28af6a3f0c9ec5e454d00d4ac5ac78f5cc7ab4626d0f72f44f1c229659e97e1f) |

Read verification passed on Bradbury after deploy. The public app points at this contract address and reads accepted state.

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.
