import { makeReader, write, connectWallet, activeAccount, balanceOf, short, toGen, GEN, fmtErr }
  from "../shared/genlayer-lite.js";

const CONTRACT = "0x8814b925F9Db3A4B89b127339190125d65ec319B";
const { read } = makeReader(CONTRACT);
const S_ACTIVE = 0, S_BREACHED = 1, S_CLOSED = 2;
let account = null, slas = [], openRow = null;
const $ = (id) => document.getElementById(id);
const esc = (s) => (s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const hostOf = (u) => { try { return new URL(u).hostname.replace(/^www\./, ""); } catch (_) { return u; } };

$("contractLink").textContent = "Contract " + short(CONTRACT) + " \u2197";

function toast(msg, kind = "", title = "cadence") {
  const el = document.createElement("div"); el.className = "toast " + kind;
  el.innerHTML = `<span class="tt">${title}</span>`; el.appendChild(document.createTextNode(msg));
  $("log").appendChild(el); setTimeout(() => el.remove(), kind === "err" ? 15000 : 5000);
}

async function refreshWallet() {
  account = await activeAccount();
  const slot = $("walletslot");
  if (account) { let bal = 0n; try { bal = await balanceOf(account); } catch (_) {} slot.innerHTML = `<span class="mono" style="font-size:12.5px;color:var(--txt2)">${short(account)} \u00b7 ${toGen(bal)} GEN</span>`; }
  else { slot.innerHTML = `<button class="btn ghost sm" id="connectBtn">Connect</button>`; $("connectBtn").onclick = doConnect; }
}
async function doConnect() { try { account = await connectWallet(); toast("Connected on studionet.", "ok"); await refreshWallet(); } catch (e) { toast(fmtErr(e), "err"); } }
async function ensureWallet() { if (!account) account = await connectWallet(); await refreshWallet(); }

async function load() {
  try {
    const count = Number(await read("get_sla_count"));
    const out = [];
    for (let i = 0; i < count; i++) out.push({ id: i, ...(await read("get_sla", [i])) });
    slas = out; renderBanner(); renderBoard();
    $("svcCount").textContent = count + (count === 1 ? " service" : " services");
    const breached = out.filter((s) => Number(s.status) === S_BREACHED).length;
    $("stOperational").textContent = out.filter((s) => Number(s.status) === S_ACTIVE).length;
    $("stBreached").textContent = breached;
    $("stBonded").textContent = toGen(out.filter((s) => Number(s.status) === S_ACTIVE).reduce((a, s) => a + BigInt(s.bond), 0n).toString());
  } catch (e) { $("board").innerHTML = `<div class="b-empty">Could not reach the chain. ${fmtErr(e)}</div>`; }
}

function renderBanner() {
  const breached = slas.filter((s) => Number(s.status) === S_BREACHED).length;
  const active = slas.filter((s) => Number(s.status) === S_ACTIVE).length;
  const banner = $("statusBanner"), dot = $("sbDot");
  if (breached > 0) {
    banner.className = "status-banner bad"; dot.className = "sb-dot bad";
    $("sbHeadline").textContent = "Service disruption";
    $("sbSub").textContent = `${breached} service${breached === 1 ? "" : "s"} in breach \u2014 bonds paid out`;
  } else if (active > 0) {
    banner.className = "status-banner ok"; dot.className = "sb-dot ok";
    $("sbHeadline").textContent = "All systems operational";
    $("sbSub").textContent = `${active} service${active === 1 ? "" : "s"} bonded and healthy`;
  } else {
    banner.className = "status-banner"; dot.className = "sb-dot";
    $("sbHeadline").textContent = "No services yet";
    $("sbSub").textContent = "Register the first bonded service";
  }
}

function ticks(s) {
  const total = Number(s.checks), healthy = Number(s.healthy_checks), breached = Number(s.status) === S_BREACHED;
  let html = "";
  for (let i = 0; i < Math.max(total, 1); i++) {
    const bad = breached && i === total - 1;
    html += `<span class="tick ${bad ? "bad" : (i < healthy ? "" : "none")}"></span>`;
  }
  return `<div class="tick-row">${html}</div>`;
}

function renderBoard() {
  const el = $("board");
  if (!slas.length) { el.innerHTML = `<div class="b-empty">No services monitored yet.</div>`; return; }
  el.innerHTML = "";
  [...slas].reverse().forEach((s) => {
    const st = Number(s.status);
    const dotc = st === S_ACTIVE ? "sd-ok" : st === S_BREACHED ? "sd-bad" : "sd-mut";
    const lbl = st === S_ACTIVE ? `<span class="sstatus ss-ok">Operational</span>` : st === S_BREACHED ? `<span class="sstatus ss-bad">Breach</span>` : `<span class="sstatus ss-mut">Closed</span>`;
    const isProvider = account && account.toLowerCase() === s.provider.toLowerCase();
    const wrap = document.createElement("div"); wrap.className = "svc" + (openRow === s.id ? " open" : "");
    wrap.innerHTML = `
      <div class="svc-row">
        <span class="svc-dot ${dotc}"></span>
        <div class="svc-m"><div class="svc-name">${esc(s.service)}</div><div class="svc-ep">${esc(hostOf(s.endpoint_url))}</div></div>
        <div class="svc-uptime"><b>${s.healthy_checks}/${s.checks}</b><span>healthy</span></div>
        ${lbl}
      </div>
      <div class="svc-detail">
        <div class="dl">
          <div class="svc-cond">Healthy when <b>${esc(s.healthy_condition)}</b></div>
          ${ticks(s)}
          ${s.last_result ? `<div class="svc-last">Last check: ${esc(s.last_result)}</div>` : ""}
          <div class="svc-cond" style="font-size:13px">Bond <b>${toGen(s.bond)} GEN</b> \u00b7 covers ${short(s.subscriber)}</div>
          <div class="svc-actions">
            ${st === S_ACTIVE ? `<button class="btn primary xs checkBtn" data-id="${s.id}"><i class="ph-bold ph-pulse"></i> Run check</button>` : ""}
            ${st === S_ACTIVE && isProvider ? `<button class="btn ghost xs closeBtn" data-id="${s.id}">Close & reclaim</button>` : ""}
            <a class="btn ghost xs" href="${esc(s.endpoint_url)}" target="_blank" rel="noopener">Open endpoint \u2197</a>
          </div>
        </div>
      </div>`;
    wrap.querySelector(".svc-row").onclick = () => { openRow = openRow === s.id ? null : s.id; renderBoard(); };
    el.appendChild(wrap);
  });
  document.querySelectorAll(".checkBtn").forEach((b) => b.onclick = (e) => { e.stopPropagation(); doCheck(Number(b.dataset.id)); });
  document.querySelectorAll(".closeBtn").forEach((b) => b.onclick = (e) => { e.stopPropagation(); doClose(Number(b.dataset.id)); });
}

function openModal() { $("scrim").classList.add("on"); }
function closeModal() { $("scrim").classList.remove("on"); }

function openNew() {
  $("modalTitle").textContent = "Register a service";
  $("modalBody").innerHTML = `
    <p>Back a service promise with a bond. Name the endpoint, what healthy means, and who is covered. A breach pays them automatically.</p>
    <label>Service name</label><input id="nSvc" maxlength="80" placeholder="Payments API" />
    <label>Endpoint URL</label><input id="nUrl" placeholder="https://status.example.com" />
    <label>Healthy when (plain English)</label><textarea id="nCond" placeholder="The status endpoint returns operational for the payments API"></textarea>
    <label>Subscriber covered (address)</label><input id="nSub" placeholder="0x..." />
    <label>Bond (GEN)</label><input id="nBond" type="number" min="0" step="0.5" value="5" />
    <button class="btn primary block" id="createBtn"><i class="ph-bold ph-shield-check"></i> Post bond & monitor</button>`;
  $("createBtn").onclick = doCreate; openModal();
}

async function doCreate() {
  const svc = $("nSvc").value.trim(), url = $("nUrl").value.trim(), cond = $("nCond").value.trim(), sub = $("nSub").value.trim();
  const bond = parseFloat($("nBond").value);
  if (!svc) return toast("Name the service.", "err");
  if (!url) return toast("Enter the endpoint URL.", "err");
  if (!cond) return toast("Define healthy.", "err");
  if (!/^0x[0-9a-fA-F]{40}$/.test(sub)) return toast("Enter a valid subscriber address.", "err");
  if (!(bond > 0)) return toast("Bond must be above zero.", "err");
  const btn = $("createBtn"); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> posting bond';
  try { await ensureWallet(); await write(CONTRACT, "create_sla", [svc, url, cond, sub], GEN(bond)); toast("Service registered.", "ok"); closeModal(); await load(); }
  catch (e) { toast(fmtErr(e), "err"); btn.disabled = false; btn.innerHTML = "Post bond & monitor"; }
}
async function doCheck(id) {
  if (!confirm("Run a check? Validators read the endpoint and rule healthy or breach. Calls a real LLM; a breach pays the subscriber.")) return;
  toast("Validators reading the endpoint\u2026", "", "check");
  try { await ensureWallet(); await write(CONTRACT, "check", [id]); toast("Check recorded on-chain.", "ok"); await load(); }
  catch (e) { toast(fmtErr(e), "err"); }
}
async function doClose(id) {
  try { await ensureWallet(); await write(CONTRACT, "close", [id]); toast("SLA closed, bond reclaimed.", "ok"); await load(); }
  catch (e) { toast(fmtErr(e), "err"); }
}

$("navPostBtn").onclick = openNew;
$("refreshBtn").onclick = load;
$("closeModal").onclick = closeModal;
$("scrim").onclick = (e) => { if (e.target === $("scrim")) closeModal(); };
const _cb = $("connectBtn"); if (_cb) _cb.onclick = doConnect;
if (window.ethereum) window.ethereum.on?.("accountsChanged", refreshWallet);

refreshWallet();
load();
