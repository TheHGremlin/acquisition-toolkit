# Decisions log

Every design decision for this toolkit, with its status and date. Newest sections at the bottom.
Status keys: **LOCKED** = decided by the maintainer · **PROPOSED** = default, waiting for the maintainer · **OPEN** = needs a call · ⚑ = unverified fact.

The original design record is [docs/PLAN.md](docs/PLAN.md).

## v1 scope and setup (2026-11-02)

| ID | Decision | Status |
|---|---|---|
| D01 | License: **MIT**, copyright held under the maintainer's GitHub handle. | LOCKED |
| D02 | Repository name: **`acquisition-toolkit`**. | LOCKED |
| D03 | Plugin name **`acq`**, so skills run as `/acq:<skill>`. | LOCKED |
| D04 | v1 ships the Scorecard (with setup wizard), partner quiz, Deal Room, Listing Digest page and digest skill, deal skills (graduate-deal, call-prep, call-debrief, cim-review, financials-workup) and the financial workbook builder. **Not in v1:** pipeline dashboard and its sync job, valuation, the chat/inbox handoff, buyer-brand material. | LOCKED |
| D05 | The setup wizard is a **"Setup" view inside the Scorecard**, because artifacts can't read each other's databases. The partner quiz stays a separate optional page. | LOCKED |
| D06 | Config lives in the Scorecard's database (`config/profile`) as the live copy, with an exported JSON file in the user's own `my-search/` folder as the backup and seed. | LOCKED |
| D07 | The Scorecard and partner quiz also run as **plain local HTML** (browser storage plus export/import) when there is no Claude runtime. | LOCKED |
| D08 | `excel_refresh.ps1` ships as an **optional, Windows-only** step. The workbook builder itself is cross-platform. | LOCKED |
| D09 | The tools keep their dry, teasing voice by default, with a `voice: "plain"` switch. | LOCKED |
| D10 | Ship the ten-criterion set as an editable **starter set with generic anchors**, plus a wider criteria library. | LOCKED |
| D11 | Commits use the maintainer's GitHub no-reply address, set in this repository only. | LOCKED |
| D12 | The README may say the toolkit grew out of an MBA acquisition search. No names. | LOCKED |
| D13 | Privacy check: a pre-commit hook greps staged files for personal terms. The term list lives in `.git/info/`, so it is never committed. | LOCKED |
| D14 | Example values (money, drive limits, weights) are deliberately **different** from any real searcher's settings and labelled as examples. | LOCKED |

## Distribution (2026-11-02)

Checked against the Claude Code plugin and marketplace docs and the claude.com plugin platform-support page on 2026-11-02.

| ID | Decision | Status |
|---|---|---|
| X01 | The repository is a plugin marketplace (`.claude-plugin/marketplace.json`) listing one plugin at `./plugins/acq`, the documented layout. | LOCKED |
| X02 | Skills reference bundled pages and templates through `${CLAUDE_PLUGIN_ROOT}`. | LOCKED |
| X03 | No top-level `bin/` in the plugin: claude.ai and Cowork refuse plugins that have one. Scripts live in `tools/`. | LOCKED |
| X04 | ⚑ Not every account may have the Artifact tool or the `db`, `user` and `sample` capabilities. `/acq:setup` checks first and falls back to local HTML. | OPEN (verify) |
| X05 | ⚑ Whether claude.ai chat can publish an artifact with a database from a plugin skill. v1 documents Claude Code as the supported path. | OPEN (verify) |
