// The Conditioning Atlas — dependency-free dashboard.
// Loads atlas.csv (sibling file), renders faceted filters + a sortable table,
// and ships a one-click "flagship" preset for the bivalve/metamorphosis question.

"use strict";

// ---- Minimal RFC-4180 CSV parser (handles quoted fields, commas, newlines) ----
function parseCSV(text) {
  const rows = [];
  let row = [], field = "", i = 0, inQuotes = false;
  const n = text.length;
  while (i < n) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') { field += '"'; i += 2; continue; }
        inQuotes = false; i++; continue;
      }
      field += c; i++; continue;
    }
    if (c === '"') { inQuotes = true; i++; continue; }
    if (c === ",") { row.push(field); field = ""; i++; continue; }
    if (c === "\r") { i++; continue; }
    if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; i++; continue; }
    field += c; i++;
  }
  if (field.length > 0 || row.length > 0) { row.push(field); rows.push(row); }
  if (!rows.length) return [];
  const header = rows[0];
  return rows.slice(1)
    .filter(r => r.length > 1 || (r.length === 1 && r[0].trim() !== ""))
    .map(r => Object.fromEntries(header.map((h, j) => [h, (r[j] ?? "").trim()])));
}

// ---- Config ----
const FACETS = [
  ["taxon_group", "Taxon"],
  ["life_stage_primed", "Life stage primed"],
  ["stressor_category", "Stressor"],
  ["generation_primed", "Generation primed"],
  ["persisted_past_metamorphosis", "Persisted past metamorphosis"],
  ["methylation_measured", "Methylation measured"],
];

const COLUMNS = [
  ["study", "Study", r => studyCell(r)],
  ["species", "Species", r => `<span class="small"><i>${esc(r.species)}</i></span>`],
  ["taxon_group", "Taxon", r => esc(r.taxon_group)],
  ["life_stage_primed", "Primed at", r => esc(r.life_stage_primed)],
  ["stressor", "Stressor", r => `${esc(r.stressor_category)}<div class="small">${esc(r.stressor_specific)}</div>`],
  ["dose", "Dose", r => doseCell(r)],
  ["gen", "Gen", r => `${esc(r.generation_primed)}&rarr;${esc(r.generation_assayed)}`],
  ["assay_type", "Assay", r => esc(r.assay_type)],
  ["effect_direction", "Effect", r => `<span class="pill dir-${esc(r.effect_direction)}">${esc(r.effect_direction)}</span>`],
  ["persisted_past_metamorphosis", "Past metam.?", r => persistCell(r)],
  ["methylation_measured", "Methyl?", r => yesno(r.methylation_measured)],
];

let ALL = [];
const active = {};        // facet -> Set of selected values
let searchText = "";
let sortKey = null, sortDir = 1;

// ---- Cell renderers ----
function esc(s) { return String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
function studyCell(r) {
  const label = `${esc(r.first_author)} ${esc(r.year)}`;
  const doi = (r.doi && r.doi !== "NR") ? `https://doi.org/${esc(r.doi)}` : null;
  return doi ? `<a href="${doi}" target="_blank" rel="noopener">${label}</a>` : label;
}
function doseCell(r) {
  if (r.dose_value) return `${esc(r.dose_value)} ${esc(r.dose_unit)}`;
  return `<span class="small">${esc(r.dose_text || "—")}</span>`;
}
function persistCell(r) {
  const v = r.persisted_past_metamorphosis;
  if (v === "yes") return `<span class="yes">yes</span>`;
  if (v === "no") return `<span class="no">no</span>`;
  return `<span class="muted">${esc(v)}</span>`;
}
function yesno(v) {
  if (v === "yes") return `<span class="yes">yes</span>`;
  if (v === "no") return `<span class="muted">no</span>`;
  return `<span class="muted">${esc(v)}</span>`;
}

// ---- Filtering ----
function passesFacets(r, exclude) {
  for (const [key] of FACETS) {
    if (key === exclude) continue;
    const sel = active[key];
    if (sel && sel.size && !sel.has(r[key])) return false;
  }
  return true;
}
function passesSearch(r) {
  if (!searchText) return true;
  const hay = [r.species, r.common_name, r.stressor_specific, r.stressor_category,
    r.first_author, r.short_title, r.notes, r.outcome_metric].join(" ").toLowerCase();
  return hay.includes(searchText);
}
function filtered() {
  return ALL.filter(r => passesFacets(r, null) && passesSearch(r));
}

// ---- Rendering ----
function renderCards() {
  const rows = filtered();
  const studies = new Set(rows.map(r => r.study_key)).size;
  const taxa = new Set(rows.map(r => r.taxon_group)).size;
  const bivalve = rows.filter(r => r.taxon_group === "bivalve").length;
  const stuck = rows.filter(r => r.persisted_past_metamorphosis === "yes").length;
  const cards = [
    [rows.length, "contrasts", ""],
    [studies, "studies", ""],
    [taxa, "taxa", ""],
    [bivalve, "bivalve rows", ""],
    [stuck, "persist past metam.", "flag"],
  ];
  document.getElementById("cards").innerHTML = cards.map(
    ([n, l, cls]) => `<div class="card ${cls}"><div class="n">${n}</div><div class="l">${l}</div></div>`
  ).join("");
}

function renderFacets() {
  const el = document.getElementById("facets");
  el.innerHTML = FACETS.map(([key, label]) => {
    // counts respect all OTHER active facets (classic faceted-search behavior)
    const pool = ALL.filter(r => passesFacets(r, key) && passesSearch(r));
    const counts = {};
    for (const r of pool) counts[r[key]] = (counts[r[key]] || 0) + 1;
    const values = Object.keys(counts).sort();
    const sel = active[key] || new Set();
    const opts = values.map(v => `
      <label>
        <input type="checkbox" data-facet="${esc(key)}" value="${esc(v)}" ${sel.has(v) ? "checked" : ""}>
        <span>${esc(v)}</span><span class="cnt">${counts[v]}</span>
      </label>`).join("");
    return `<div class="facet"><h4>${esc(label)}</h4>${opts || '<span class="muted">—</span>'}</div>`;
  }).join("");
  el.querySelectorAll("input[type=checkbox]").forEach(cb => {
    cb.addEventListener("change", () => {
      const f = cb.dataset.facet;
      active[f] = active[f] || new Set();
      cb.checked ? active[f].add(cb.value) : active[f].delete(cb.value);
      if (!active[f].size) delete active[f];
      renderAll();
    });
  });
}

function renderChips() {
  const parts = [];
  for (const [key, label] of FACETS) {
    const sel = active[key];
    if (sel && sel.size) parts.push(`<span class="chip">${esc(label)}: <b>${[...sel].map(esc).join(", ")}</b></span>`);
  }
  if (searchText) parts.push(`<span class="chip">search: <b>${esc(searchText)}</b></span>`);
  document.getElementById("chips").innerHTML = parts.join("");
}

function renderTable() {
  let rows = filtered();
  if (sortKey) {
    rows = rows.slice().sort((a, b) => {
      const av = (a[sortKey] || "").toString(), bv = (b[sortKey] || "").toString();
      const an = parseFloat(av), bn = parseFloat(bv);
      const cmp = (!isNaN(an) && !isNaN(bn)) ? an - bn : av.localeCompare(bv);
      return cmp * sortDir;
    });
  }
  document.getElementById("count").textContent = `${rows.length} contrast${rows.length === 1 ? "" : "s"} shown`;

  const head = COLUMNS.map(([key, label]) => {
    const arrow = sortKey === key ? (sortDir === 1 ? "▲" : "▼") : "";
    return `<th data-key="${esc(key)}">${esc(label)} <span class="arrow">${arrow}</span></th>`;
  }).join("");

  const body = rows.map(r => {
    const tds = COLUMNS.map(([, , fn]) => `<td>${fn(r)}</td>`).join("");
    return `<tr>${tds}</tr><tr class="detailrow"><td colspan="${COLUMNS.length}">${detail(r)}</td></tr>`;
  }).join("");

  document.getElementById("tableWrap").innerHTML =
    `<table><thead><tr>${head}</tr></thead><tbody>${body}</tbody></table>`;

  document.querySelectorAll("th[data-key]").forEach(th => {
    th.addEventListener("click", () => {
      const k = th.dataset.key;
      if (sortKey === k) sortDir = -sortDir; else { sortKey = k; sortDir = 1; }
      renderTable();
    });
  });
}

function detail(r) {
  const fields = [
    ["Short title", r.short_title], ["Priming window", r.priming_window_text],
    ["Transmission", r.transmission_channel], ["Life stage assayed", r.life_stage_assayed],
    ["Exposure", [r.exposure_duration_value, r.exposure_duration_unit].filter(Boolean).join(" ")],
    ["Env. realistic", r.environmentally_realistic], ["Outcome metric", r.outcome_metric],
    ["Effect size", [r.effect_size_value, r.effect_size_type].filter(Boolean).join(" ")],
    ["Significance", r.significance],
    ["Persistence", [r.persistence_value, r.persistence_unit].filter(Boolean).join(" ")],
    ["Latest timepoint", r.latest_timepoint_assayed], ["Persistence notes", r.persistence_notes],
    ["Methylation method", r.methylation_method], ["Transcriptome", r.transcriptome_measured],
    ["ncRNA", r.ncRNA_measured], ["Study design", r.study_design], ["Sample size", r.sample_size],
    ["Source", r.source_location], ["Confidence", r.extraction_confidence], ["Notes", r.notes],
  ].filter(([, v]) => v && v !== "");
  const kv = fields.map(([k, v]) => `<div class="k">${esc(k)}</div><div>${esc(v)}</div>`).join("");
  return `<details class="detail"><summary>details &middot; <code>${esc(r.record_id)}</code></summary><div class="kv">${kv}</div></details>`;
}

function renderAll() {
  renderCards();
  renderFacets();
  renderChips();
  renderTable();
}

// ---- Controls ----
function applyFlagship() {
  for (const k of Object.keys(active)) delete active[k];
  active.taxon_group = new Set(["bivalve"]);
  active.persisted_past_metamorphosis = new Set(["yes", "no"]);
  searchText = "";
  document.getElementById("search").value = "";
  renderAll();
}
function resetAll() {
  for (const k of Object.keys(active)) delete active[k];
  searchText = "";
  document.getElementById("search").value = "";
  sortKey = null;
  renderAll();
}

// ---- Boot ----
async function boot() {
  document.getElementById("flagship").addEventListener("click", applyFlagship);
  document.getElementById("reset").addEventListener("click", resetAll);
  document.getElementById("search").addEventListener("input", e => {
    searchText = e.target.value.trim().toLowerCase(); renderAll();
  });
  try {
    const res = await fetch("atlas.csv", { cache: "no-store" });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    ALL = parseCSV(await res.text());
    if (!ALL.length) throw new Error("atlas.csv parsed to 0 rows");
    renderAll();
  } catch (err) {
    document.getElementById("content").innerHTML =
      `<div class="err"><b>Could not load atlas.csv.</b><br>${esc(err.message)}<br><br>
       If viewing locally, serve the folder over HTTP (browsers block file:// fetches):<br>
       <code>cd docs &amp;&amp; python3 -m http.server</code> then open
       <code>http://localhost:8000/</code>.</div>`;
  }
}
boot();
