# Cadence

Milestone and schedule claims with source-aware settlement.

Cadence is built for timing disputes: whether a deadline was met, a release happened, or a public milestone actually landed. The contract keeps commitments, evidence and GenLayer settlement in one timeline.

## Review Links

| Surface | Link |
| --- | --- |
| Live app | https://assmore22-cadence.vercel.app |
| GitHub | https://github.com/assmore22/cadence |
| Contract | https://explorer-studio.genlayer.com/contracts/0x8814b925F9Db3A4B89b127339190125d65ec319B |

## Chain Record

- Network: GenLayer Studionet
- Chain ID: 61999
- Contract: `0x8814b925F9Db3A4B89b127339190125d65ec319B`
- Deploy transaction: [0x4f18100a...ded7a5](https://explorer-studio.genlayer.com/tx/0x4f18100adee260131e77ced3bfb65f976bf5519d1101682ed7c5c03d3aded7a5)
- Deployed: `2026-06-23T19:47:05.336Z`
- Source: `contracts/cadence_v2.py` (36,749 bytes)

## Protocol Path

1. Set a timing standard.
2. Open a cadence record.
3. Attach milestone evidence.
4. Review the result.
5. Challenge or finalize the timeline.

The frontend reads milestones, open reviews, recent records and status-filtered lists. Contract state is public; write actions still require a connected wallet on GenLayer Studionet.

## Finalized Smoke

| Action | Transaction |
| --- | --- |
| `set_cadence_standard` | [0xdd891e91...da789c](https://explorer-studio.genlayer.com/tx/0xdd891e91b4ce6b6819c398430e1d7747d74774f319127ccabd78600d30da789c) |
| `draft_sla` | [0xb7c49b4d...1cdf42](https://explorer-studio.genlayer.com/tx/0xb7c49b4d3d926d046055bc03213c193db472651034a6a03fece7d4ead51cdf42) |
| `add_objective` | [0x3604bb12...98fa30](https://explorer-studio.genlayer.com/tx/0x3604bb12cf4119fcc26997666058560dff277f948eb0fa7732490e909098fa30) |
| `add_evidence_docs` | [0x10371ae5...516b8c](https://explorer-studio.genlayer.com/tx/0x10371ae5df4dbd900cb2265f335a841935c2f5e634bd001131fc2dc42e516b8c) |
| `add_evidence_status` | [0x1457b020...069e40](https://explorer-studio.genlayer.com/tx/0x1457b020b66d9c2523b638ca7382c3596237edc4b5ae60212723cf7aaa069e40) |
| `open_check` | [0xa4de73fb...54670a](https://explorer-studio.genlayer.com/tx/0xa4de73fbe528aadaccaa445f9a941637384cf74bea15f13c1acfc8425054670a) |

## Local Run

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Release Hygiene

The public package is static and has no install step. Vercel receives only frontend, contract source and public deployment metadata.

Keep wallet private keys, vault exports, `.env` files, Vercel project state and dashboard data out of Git. This repository is for public source, UI, tests and deployment receipts only.
