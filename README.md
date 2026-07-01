# Cadence V2

The project is built as a small on-chain court rather than a static demo: users create records, attach sources, ask GenLayer to reason over them, and keep the decision trail readable.

A GenLayer service-level court.

## Cadence Brief

This repo is organized for review: the app can be opened locally, the contract source is present, and the deployed Studionet address is pinned in `deployment.json`.

- Folder: `projects/20-cadence`
- Frontend shape: static browser app
- Contract source: `contracts/cadence_v2.py`
- Build status: Schema-valid (36749 bytes, 16 write + 18 view); deployed + 15 write smoke txs finalized incl 3 GenLayer reasoning calls; 35/35 read tests passed; legacy frontend shape verified; app.js repointed.

## Adjudication Mechanics

Cadence V2 (# v0.2.16), 36749 bytes, 16 write + 18 view.

- Primary source: `contracts/cadence_v2.py` (36,749 bytes)
- Public write/action methods: 16
- Read methods: 18
- GenLayer features: live web rendering, LLM adjudication, validator-comparative consensus, append-only collections

Typical flow: `create_sla` -> `open_check` -> `submit_challenge` -> `resolve_challenge_with_genlayer` -> `open_challenge_window` -> `submit_appeal` -> `archive_sla`

Useful reads: `get_sla_count`, `get_sla`, `get_sla_record`, `get_recent_slas`, `get_slas_by_status`, `get_party_slas`, `get_objectives`, `get_evidence`

## Cadence Chain Links

- Network: studionet (61999)
- Contract: [0x8814b925F9Db3A4B89b127339190125d65ec319B](https://explorer-studio.genlayer.com/contracts/0x8814b925F9Db3A4B89b127339190125d65ec319B)
- Deploy tx: [0x4f18100a...ded7a5](https://explorer-studio.genlayer.com/tx/0x4f18100adee260131e77ced3bfb65f976bf5519d1101682ed7c5c03d3aded7a5)
- Deployed at: 2026-06-23T19:47:05.336Z
- Smoke writes recorded: 15

Smoke coverage:

- set_cadence_standard: [0xdd891e91...da789c](https://explorer-studio.genlayer.com/tx/0xdd891e91b4ce6b6819c398430e1d7747d74774f319127ccabd78600d30da789c)
- draft_sla: [0xb7c49b4d...1cdf42](https://explorer-studio.genlayer.com/tx/0xb7c49b4d3d926d046055bc03213c193db472651034a6a03fece7d4ead51cdf42)
- add_objective: [0x3604bb12...98fa30](https://explorer-studio.genlayer.com/tx/0x3604bb12cf4119fcc26997666058560dff277f948eb0fa7732490e909098fa30)
- add_evidence_docs: [0x10371ae5...516b8c](https://explorer-studio.genlayer.com/tx/0x10371ae5df4dbd900cb2265f335a841935c2f5e634bd001131fc2dc42e516b8c)
- add_evidence_status: [0x1457b020...069e40](https://explorer-studio.genlayer.com/tx/0x1457b020b66d9c2523b638ca7382c3596237edc4b5ae60212723cf7aaa069e40)
- open_check: [0xa4de73fb...54670a](https://explorer-studio.genlayer.com/tx/0xa4de73fbe528aadaccaa445f9a941637384cf74bea15f13c1acfc8425054670a)

## Inspect The App

```powershell
cd <private-workspace-root>
npm run preview:start
npm run preview:project -- 20-cadence
```

Open http://localhost:8080/20-cadence/.

## Shipping Notes

```powershell
cd <private-workspace-root>
npm run publish:project -- -Project 20-cadence -Repo https://github.com/aspro45/<repo-name>.git
```

## Security Notes

The repo is designed for public GitHub/Vercel release. Keep `.env`, `.vercel/`, wallet vaults, private keys and local dashboard state out of git. The publisher script enforces these ignore rules before it pushes.
