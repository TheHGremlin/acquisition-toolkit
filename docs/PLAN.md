# Plan: open, blank acquisition toolkit (v1)

Status: ACCEPTED 2026-11-02 (all recommended defaults; see DECISIONS.md). Kept as the original design record.
Status keys: LOCKED = decided · PROPOSED = Claude's default, maintainer to confirm · ⚑ = unverified.

This file deliberately contains no personal values. Where it says "yours", it means "the value in the original toolkit", which becomes configuration.

---

## 1. Components: generic vs. personal

| Component | Source | Generic (keep) | Personal (becomes config or goes) |
|---|---|---|---|
| **Acquisition Scorecard** | `Acquisition_Scorecard.html` (97 KB) | Fit formula with two-sided weights, "?" = 2 + broker questions, deal-math engine (SBA tiers, DSCR, take-home, seller note, cash-only, tiny loan, real-estate split), track record, commute and premises calculators, perks & dings, trust, golden ticket, Fit × Joy map, quadrants, status workflow, cheat sheet, "Challenge me", `ascEngine.calc` | Weights, the 10-criterion set, anchors and hints (some mention one state's tourism and hurricanes), hard-gate list, money settings, prime rate, commute limits, quadrant cutoffs, household-check callout (names a person), Joy examples, multiples table contents, the Deal Room URL, the "Challenge me" prompt's profile |
| **Priorities quiz** | `Deal_Priorities_Quiz.html` | Two-round swing-weighting quiz, geometric-mean (AHP-style) math, loop and toss-up counts, dealbreaker button, comparison view | Hard-coded criteria cards and wording, the original searcher's weights baked in as the comparison, "household edition" copy naming people and a state |
| **Deal Room** | `Deal_Room.html` | Stages, contacts, activity log subcollection, docs checklist, questions split broker/seller with notes and drag-reorder, snapshot, valuation summary, staleness flags | Scorecard URL only |
| **Listing Digest page** | `Listing_Digest.html` | Fully generic renderer of `digests/<date>` | Scorecard URL only |
| **Daily digest task** | scheduled-task `SKILL.md` | Window logic, de-dup by listing number, browser fetching with no-CAPTCHA rule, gate screening, facts-only load, tiering, digest write | Gmail label and sender search, listing sites, home base, every gate and screen-out rule (routes, fintech, US-only, real-estate-sold-separately), money figures, "worth a look" preferences, Joy bonus interests |
| **Skills** | `.claude/skills/*` | graduate-deal, call-prep, call-debrief, cim-review, financials-workup: the workflows are generic | Artifact URLs, project path, names, one partner's handover concern, project-specific file paths |
| **pipeline-refresh + Dashboard** | `Pipeline_Sync/` | The idea (done log, next up, funnel) | Built on a **Dashboard artifact type** that may not exist on other accounts ⚑, plus `state.json` (excluded) |
| **Financial workbook builder** | `Tools/fin_workbook.py` | Fully generic (JSON → audited Excel with charts) | Colour palette only; docstring names a person |
| **Excel refresh** | `Tools/excel_refresh.ps1` | Works | **Windows + Excel only** (COM) |
| **Method docs** | decisions log, anchors file | The method: gates vs. weights, "1 = worst you'd still accept", re-anchoring when a swing contains a dealbreaker, two-sided weights, calibration protocol, first-look framing | Every specific value, date, deal, name and quiz result |

Never copied: `Deals/`, `Pipeline_Sync/state.json` and `out/`, database exports, buyer-brand files, `Brand_Assets/`, `buyer_profile_site/`, bio, letterhead, profile .docx, SBA rules doc, course files, any artifact URL.

## 2. Personal → configuration inventory

One config document, `config/profile` (shape below), replaces every constant in the table.

| Area | Becomes |
|---|---|
| Money | `money.cashDown`, `money.projectCap`, `money.operatorSalary`, `money.sdeFloor`, `money.projectFactor` (price → total project), `money.loanTermYears`, `money.realEstateTermYears`, `money.softGatePenalty`, `money.rentFlagPct` |
| Rates ⚑ | `rates.prime` with `rates.checkedOn`, `rates.sbaTiers` (loan-size → max spread). Shipped values are labelled **"example values as of <date>: check current prime and SBA 7(a) caps before trusting the math"**. The page nags when `checkedOn` is older than 60 days. |
| Deal-math bands | `bands.takeHome`, `bands.dscr`, `bands.dscrGate` (default 1.25, labelled as the common lender floor ⚑) |
| Hard gates | `gates[]`, picked from a template menu: food service, trade knowledge in the owner role, outside my region, owner-is-the-product, declining revenue (overrulable), project over cap (built-in), route businesses, fintech, franchise resale, health-care licensing, regulated/vice industries, online-only, plus "write your own". Each: `{id, label, tier: hard|soft|digest-only, overrulable, digestRule}` |
| Soft gates | Built-in calculated ones toggle on/off: SDE under floor, fails DSCR at asking, land lease, past commute limit, cash-only over cash, non-operational turnaround; plus custom |
| Criteria | `criteria[]` from a library: the 6 calculated/built-in ones (deal math, track record, commute burden, premises, plus revenue predictability and tourism/seasonality as judgment calls with stock anchors) and judgment criteria (team in place, owner dependence, transition support, operator upside, customer concentration, growth runway, licensing transferability…), plus custom. Each judgment criterion carries user-written 1/3/5 anchors (2/4 optional), a hint and a broker question. |
| Weights | `weights[id] = {up, down}` from the quiz; each set sums to 100 |
| Geography | `geo.homeBase` (free text, used only by Claude for drive-time estimates, never shipped), `geo.regionLimit` (free text: a state, a metro, "US"), `geo.presenceLimits` `{daily, few, weekly, weeklyStretch}` in minutes, `geo.fullScoreWithin` |
| Joy | `joy.anchors` 1–5 in the user's words, `joy.planDiscount` (default 1), quadrant cutoffs `fitCut`, `joyCut` |
| Household | `household.enabled`, `household.partnerLabel` (e.g. "your partner"), which criteria trigger it |
| Home-lien flag | `lien.enabled`, `lien.reHaircut`, `lien.ffeHaircut`, all labelled rough US SBA 7(a) assumptions ⚑, not advice |
| Digest | `digest.gmailQuery`, `digest.sites[]`, `digest.screenOuts[]` (gate ids with `digestRule`), `digest.topTierRule` (plain-English preferences) |
| Voice | `voice: "snarky" | "plain"` (the callouts keep their bite by default; plain mode for people who'd rather not be roasted by a spreadsheet) |

## 3. Wizard design

Five steps, saving as you go, so the 90-pair quiz can be paused:

1. **Money**: cash for the deal (after reserves, with a one-line explainer of why reserves come off first), total project cap, the salary you need, SDE floor. Shows the "max asking price by SDE" table live so the numbers mean something.
2. **Gates**: template menu with on/off/edit, tier per gate, "write your own". Teaches the rule: *a gate is anything that ends the conversation; a weight is a trade-off.*
3. **Criteria**: pick from the library (with the four tests: judgeable from a listing, varies by deal, not already a gate, you care), add your own, write what a 1 / 3 / 5 look like. Enforces "1 = worst you'd still accept". Warns above ~12 criteria (90+ quiz pairs gets long fast: n(n−1)/2 per round).
4. **Quiz**: the two-round swing quiz generated from *their* criteria and anchors. Afterwards: weights, loops, toss-ups, and any dealbreaker clicks flagged as "this is a gate candidate: re-anchor and re-run those pairs", which is the C04/C06 lesson turned into a feature.
5. **Geography and Joy**: region limit, drive limits by presence level, Joy anchors in their own words, quadrant cutoffs.

Output: `config/profile`, plus **Export config** (JSON download/copy) and **Import config**.

**Where the wizard lives (PROPOSED): inside the Scorecard as a "Setup" view**, not a separate artifact. Artifacts can't read each other's databases, so a separate wizard would need Claude (or the user) to carry the config across. Inside the Scorecard, finishing setup *is* configuring the Scorecard, and re-taking the quiz later re-weights in place. The partner quiz stays a separate, optional page (it's shared with someone else) that outputs a results JSON for comparison only.

**Where config lives (PROPOSED): the Scorecard's database is the live copy; `my-search/config.json` in the user's repo copy is the backup and the seed.** The setup skill writes the file to the db; the Scorecard's Export writes the db back to a file. Skills read `config/profile` from the db, so there is one live source.

## 4. Distribution

Findings from current docs (code.claude.com plugins + marketplace pages, claude.com platform-support page, read 2026-11-02):
- A GitHub repo with `.claude-plugin/marketplace.json` is a marketplace. Users run `claude plugin marketplace add <owner>/<repo>` then `claude plugin install <plugin>@<marketplace>` (or `/plugin` in a session). Plugin skills run as `/<plugin>:<skill>`.
- A plugin's skills can reference bundled files via `${CLAUDE_PLUGIN_ROOT}`, which is substituted in skill content. So the setup skill can publish `${CLAUDE_PLUGIN_ROOT}/pages/scorecard.html`.
- The same plugin installs on **claude.ai chat and Cowork** via Customize → Plugins from a GitHub marketplace. Skills load there; a top-level `bin/` makes chat and Cowork refuse the plugin, so ship scripts under `tools/`, not `bin/`.
- ⚑ Whether every Claude Code user has the Artifact publish tool and the `db`, `user` and `sample` capabilities. The capability list is per account ("anything not listed is unavailable to this user"). The setup skill must check and fall back.
- ⚑ Whether a plugin skill running in claude.ai chat can publish an artifact *with* `db`. Unverified; v1 documents Claude Code as the supported path.
- ⚑ Whether `source: "./"` (repo root as both marketplace and plugin) is accepted. The documented pattern is `./plugins/<name>`, so use that.

**Proposed path for a stranger:**
1. `claude plugin marketplace add <owner>/<repo>` → `claude plugin install acq@<marketplace>`.
2. Make a private folder for their search (outside the plugin cache) and run `/acq:setup` there. The skill: checks for the Artifact tool and capabilities; publishes their own Scorecard (and, as they choose, Deal Room, Digest, partner quiz) with the right capabilities; records the URLs in `my-search/toolkit.json`; opens the Setup view.
3. They do the wizard in the Scorecard. `/acq:setup` re-run (or `/acq:sync-config`) exports the config to `my-search/config.json`.
4. Other skills (`/acq:graduate-deal`, `/acq:call-prep`, …) read URLs from `my-search/toolkit.json` and settings from `config/profile`.

**No Claude Code? (PROPOSED: yes, for Scorecard + quiz.)** The pages detect a missing `window.claude` and switch to localStorage, with Export/Import JSON as the backup. "Challenge me" hides. Open `scorecard.html` from the repo in a browser and it works. Deal Room gets the same adapter in v1 if cheap; the Digest has no local mode (it's fed by Claude).

## 5. Repo layout (PROPOSED)

```
acquisition-toolkit/
  .claude-plugin/marketplace.json
  plugins/acq/
    .claude-plugin/plugin.json
    skills/  setup/ graduate-deal/ call-prep/ call-debrief/ cim-review/ financials-workup/ listing-digest/
    pages/   scorecard.html  partner-quiz.html  deal-room.html  listing-digest.html
    tools/   fin_workbook.py  excel_refresh.ps1 (Windows, optional)
    templates/ config.example.json  gate-templates.json  criteria-library.json  digest-task.md
  examples/  fictional config + 5 fictional deals + a fictional CIM fact sheet
  docs/      METHOD.md (how to pick gates, criteria, anchors, weights)  DISTRIBUTION.md  CONFIG.md (schema)
  README.md  LICENSE  PROGRESS.md  DECISIONS.md  .gitignore (my-search/, Deals/, *.xlsx outside examples)
```

## 6. Leave out of v1 (PROPOSED)

Pipeline Dashboard and pipeline-refresh (needs an artifact type that may not exist elsewhere, and a state file), valuation (not built yet), the Cowork/INBOX handoff, buyer brand, SBA rules doc, LOI/diligence placeholders, online-business special cases (keep as a gate template only).

## 7. Build order (PROPOSED)

1. Repo skeleton, LICENSE, DECISIONS.md, PROGRESS.md, `.gitignore`, privacy grep script (`tools/privacy_check.py` kept *outside* the repo, since its search terms are themselves personal).
2. Config schema + example config + gate templates + criteria library.
3. Scorecard generalized to read `config/profile` (engine first, tested against the original's numbers with a fictional deal), plus storage adapter (db / localStorage).
4. Setup view (wizard) with the quiz generalized from `Deal_Priorities_Quiz.html`.
5. Setup skill + plugin/marketplace manifests; test with `--plugin-dir` and a throwaway local marketplace.
6. Deal Room, deal skills, fin_workbook, digest page + digest skill template.
7. README with a fictional walkthrough, METHOD.md.
8. GitHub: create repo (private first), push, review, then public. Each with the maintainer's OK.

---

## Open decisions (recommended default first)

1. **License**: MIT (code) · or MIT + CC BY 4.0 for docs/method · or no license (= nobody may legally reuse it).
2. **Repo name**: `acquisition-toolkit` · `eta-search-toolkit` · `first-look`.
3. **Plugin name (the skill prefix)**: `acq` (→ `/acq:setup`) · `acquisition-toolkit` (long to type).
4. **v1 scope**: Scorecard + wizard + partner quiz + Deal Room + deal skills + workbook + digest · or ship v0.1 with only Scorecard + wizard + setup, and add the rest in v0.2.
5. **Wizard location**: inside the Scorecard (Setup view) · or a separate artifact whose output Claude carries over.
6. **Config home**: Scorecard db live + JSON backup · db only · JSON only.
7. **Local (no-Claude) mode**: Scorecard + quiz · all pages · none.
8. **Windows-only Excel refresh**: ship it as optional with a note (workbook still builds everywhere; values just aren't cached until opened in Excel) · drop it.
9. **Snark**: keep the voice by default with a "plain" switch · plain by default · snark only.
10. **Default criteria set**: ship the 10 criteria (with *generic* stock anchors) as the starter set users edit · ship only the calculated four and make users add the rest.
11. **Commit identity**: commit as `TheHGremlin` with the GitHub no-reply address (`<id>+TheHGremlin@users.noreply.github.com`), set in this repo only, so no real email lands in public commit history.
12. **Credit**: say in the README that it grew out of your MBA search (no names, school optional) · or say nothing about origins.
