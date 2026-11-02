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
| X01 | The repository is a plugin marketplace (`.claude-plugin/marketplace.json`, name `acquisition-toolkit`) listing one plugin at `./plugins/acq`, the documented layout. Install id: `acq@acquisition-toolkit`. Validated and install-tested 2026-11-02. | LOCKED |
| X02 | Skills reference bundled pages and templates through `${CLAUDE_PLUGIN_ROOT}`. | LOCKED |
| X03 | No top-level `bin/` in the plugin: claude.ai and Cowork refuse plugins that have one. Scripts live in `tools/`. | LOCKED |
| X04 | ⚑ Not every account may have the Artifact tool or the `db`, `user` and `sample` capabilities. `/acq:setup` checks first and falls back to local HTML. | OPEN (verify) |
| X05 | ⚑ Whether claude.ai chat can publish an artifact with a database from a plugin skill. v1 documents Claude Code as the supported path. | OPEN (verify) |

## Scorecard build (2026-11-02)

| ID | Decision | Status |
|---|---|---|
| B01 | Pages embed copies of the template JSON files (artifacts can't fetch files from the repository). `tools/dev/sync_templates.py` copies them in; `--check` fails when a page is stale. | LOCKED |
| B02 | Until a user imports a config or runs Setup, the Scorecard runs on the fictional example profile and says so in a banner. | LOCKED |
| B03 | Deal scores are keyed by criterion id (`predictability`, `team`…) instead of the original `c1`…`c12`. | LOCKED |
| B04 | Built-in gates can be retiered (hard/soft) or switched off in the config; the declining-revenue gate's overrule can be disabled. | LOCKED |
| B05 | Fixed a latent bug carried over from the original: `normalize()` dropped defaults (such as commute presence) from partially filled deals. Only affects deals written by something other than the page. | LOCKED |
| B06 | Pages start with `<meta charset>` and a viewport tag so they render correctly as plain local files; the artifact wrapper ignores the duplicates. | LOCKED |
| B07 | Local mode stores everything under one browser-storage key (`acq-scorecard-v1`), with Export config / Export everything / Import in Settings. | LOCKED |
| B08 | The Setup wizard edits a draft kept in browser storage (`acq-setup-draft`), so it can be paused; only "Save" writes the profile. | LOCKED |
| B09 | The wizard's quiz reuses the original quiz's method and math unchanged: round A bests, round B worsts with a dealbreaker option, ratio scale 5/2/1/0.5/0.2, row geometric means, round B inverted. Weights are rounded to integers summing to 100 by largest remainder. | LOCKED |
| B10 | Quiz cards show the criterion's own 5 and 1 anchors, so a criterion needs both before the quiz starts. | LOCKED |
| B11 | A criterion marked a dealbreaker in at least a third of its round-B pairs (minimum 2) is flagged as a gate candidate, with the advice to re-anchor or gate it and retake round B. | LOCKED |
| B12 | "Start from scratch" blanks the money fields so example numbers can't slip through; the Finish step blocks saving until weights sum to 100, judgment criteria have 1/3/5 anchors, money is set, the region gate has a region, and prime was checked in the last 60 days. | LOCKED |
| S01 | `/acq:setup` works in a private `my-search/` folder (links in `toolkit.json`, config backup in `config.json`, page copies in `pages/`), refuses to run inside a clone of the toolkit, and adds `my-search/` to `.gitignore` when the folder is a git repository. | LOCKED |
| S02 | Every published page's database rule is root read `view`, write `admin`, so sharing by link lets people read but not edit; the partner quiz keeps the original per-person results rule. | LOCKED |
| S03 | Updating a page republishes the user's copy to the same URL without `capabilities` or `icon`, so the existing ones stay; data in the database is untouched. | LOCKED |
| P01 | The Deal Room and Listing Digest get the Scorecard's link from their own `config/links` document (written by `/acq:setup`) instead of a hard-coded URL; the link hides when it's missing. | LOCKED |
| P02 | The Listing Digest page was restyled from the original's personal brand palette and fonts to the Scorecard's neutral tokens. Brand colours and fonts were added to the privacy grep. | LOCKED |
| P03 | The Deal Room has no local mode in v1 (it holds post-NDA notes and is useful mainly with Claude writing to it). The Digest has none either: Claude writes it. | LOCKED |
| P04 | The partner quiz reads the searcher's criteria, anchors and weights from its own `config/quiz` document, which `/acq:setup` derives from the profile and limits to those fields (no money, no home base), since the quiz is shared. As a local file it accepts that document or an exported config. | LOCKED |
