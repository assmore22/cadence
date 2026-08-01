# Cadence

Milestone and schedule claims with source-aware settlement.

Cadence is built for timing disputes: whether a deadline was met, a release happened, or a public milestone actually landed. The contract keeps commitments, evidence and GenLayer settlement in one timeline.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://tanawo3-cadence.vercel.app |
| GitHub | https://github.com/assmore22/cadence |
| Contract | https://explorer-bradbury.genlayer.com/address/0xA26d6730AfB85AeCfd543f25886D9d76dC77EB82 |

## Chain Record

- Network: GenLayer Bradbury
- Chain ID: 4221
- Contract: `0xA26d6730AfB85AeCfd543f25886D9d76dC77EB82`
- Deployer: `0x07A12871217d82ADE643Ef8c4EfC27e14F10A649`
- Deploy transaction: [0x8d759866...8f2ca5](https://explorer-bradbury.genlayer.com/tx/0x8d759866f29d4ba199f34bc4bda95411da576d2f691c191902dcc2b23d8f2ca5)
- Deployed: `2026-07-26T19:35:50.377Z`
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
| `draft_sla` | [0x5d8b624a...b65c09](https://explorer-bradbury.genlayer.com/tx/0x5d8b624ad77fd64b45828fb566eaa17885f2cdad8d885a2794b6d30550b65c09) |

The deployment and domain smoke transaction are finalized on Bradbury. The public app is pinned to this contract address.

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.
