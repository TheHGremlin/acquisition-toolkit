# Acquisition Toolkit

A blank, configurable toolkit for people searching for a small business to buy (self-funded search, "ETA", search-fund style). It runs on [Claude](https://claude.ai): a first-look **Scorecard** with a setup wizard and a swing-weighting quiz, a **Deal Room** for deals past the first look, a daily **Listing Digest**, and Claude Code skills that prep your broker calls, review a CIM, and turn financial statements into an audit-ready Excel workbook.

It started as one MBA student's tools for a real acquisition search. This version has the personal parts taken out: your money, gates, criteria, weights, geography and what makes a business interesting to *you* are all set by you, in a guided setup.

> **Not financial, legal, tax or lending advice.** It's a screening tool. The loan math uses rough US SBA 7(a) assumptions (prime rate, maximum spreads, lien rules) that change and that you should check with a lender. Items marked ⚑ in the docs are known to need verifying.

## What's in it

| Piece | What it does | Where it runs |
|---|---|---|
| **Acquisition Scorecard** | Score a listing on Fit (0–100) and Joy (1–5), with gates, deal math (loan coverage, take-home), broker questions and a Fit × Joy map. Includes the **Setup** wizard and the two-round weighting quiz. "Challenge me" has Claude critique your scores against the listing. | A claude.ai Artifact, or a plain HTML file in your browser |
| **Deal Room** | Contacts, call log, documents checklist and open questions for deals you're actively pursuing. | claude.ai Artifact |
| **Listing Digest** | A dated digest of new listings from your alert emails, screened against your gates. | claude.ai Artifact |
| **Partner quiz** | The weighting quiz for a partner or advisor, built from your criteria and compared with your weights. For a conversation, not to change your scores. | claude.ai Artifact, or an HTML file |
| `setup` skill | Publishes your own private copies of the pages and wires them together. | Claude Code |
| `listing-digest` skill | Reads listing alerts from your mail, screens them, loads survivors into your Scorecard facts-only, writes the digest. | Claude Code + a mail connector |
| `graduate-deal`, `call-prep`, `call-debrief` | Move a deal into the Deal Room; get a one-page brief before a call; turn your call notes into log entries and answered questions. | Claude Code |
| `cim-review`, `financials-workup` | Turn a broker's CIM/CBR into a cited fact sheet, then the financials into an Excel workbook with charts and a findings sheet. | Claude Code + Python |

The method behind the Scorecard (gates vs. criteria, anchors, two-sided weights, calibration) is in [docs/METHOD.md](docs/METHOD.md). Read it before you set up; it takes ten minutes and saves you a redo.

## Setup

### Option A: with Claude Code (recommended)
You need [Claude Code](https://code.claude.com) signed in to a claude.ai account. Publishing Artifacts with a database depends on your account's features (⚑ verify: they vary by plan); the setup skill checks and tells you.

1. **Add the plugin.** In a terminal:
   ```
   claude plugin marketplace add TheHGremlin/acquisition-toolkit
   claude plugin install acq@acquisition-toolkit
   ```
   Or, inside a Claude Code session, `/plugin marketplace add TheHGremlin/acquisition-toolkit`, then install `acq` from the `/plugin` menu.
2. **Make a private folder for your search**, for example `Documents/my-business-search`, and start Claude Code there. Don't use a clone of this repository: your search data shouldn't live anywhere you might push.
3. **Run `/acq:setup`.** It creates a `my-search/` folder (links, config backup, page copies), publishes your private Scorecard, and offers the other pages.
4. **Open your Scorecard and click Setup.** Money → gates → criteria and anchors → the weighting quiz (30–45 minutes; you can stop and come back) → geography and Joy → Save.
5. **Back up your config:** Settings → Export config, saved into `my-search/`, or ask Claude to "back up my config".

To get page updates later, update the plugin (`claude plugin update acq@acquisition-toolkit`) and ask Claude to "update my toolkit pages". Your deals and config live in each page's database and aren't touched.

### Option B: just the Scorecard, no Claude Code
Download [`plugins/acq/pages/scorecard.html`](plugins/acq/pages/scorecard.html) and open it in your browser. It runs in **local mode**: everything is saved in that browser only, "Challenge me" is unavailable, and **Settings → Export everything** is your only backup. The partner quiz works the same way (the partner loads your exported config into it).

### Other requirements
- **Listing digest:** a mail connector (Gmail) in Claude, and saved-search alerts from the listing sites you use. Running it daily is optional (a scheduled task in the Claude desktop app ⚑).
- **CIM review and financials:** Python 3 with `pip install pymupdf openpyxl`.
- **Excel refresh** (caches formula values and makes a PDF to check): Windows with Excel only. Without it, open the workbook once in a spreadsheet app and save it.

## Privacy
- Your pages are **private** when published. If you share the Scorecard by link (with a partner, say), anyone with the link can read it, so keep anything under an NDA out of it. The CIM, financials and fact sheets live in the Deal Room and your local `my-search/deals/` folder.
- `my-search/` holds your money figures, home base and deal files. Keep it out of any public repository (the setup skill adds it to `.gitignore` if your folder is a git repository).
- The plugin itself holds no data and sends nothing anywhere.

## A walkthrough (fictional)
Robin is a fictional former operations manager in the fictional Example State with $300K to put in, a $2M ceiling on total project cost, and a need to earn $120K. They want a stable local business with a team in place, and they light up at bike shops, print shops and maker spaces. (Robin's settings are the example config that ships with the toolkit: [`plugins/acq/templates/config.example.json`](plugins/acq/templates/config.example.json).)

1. **Setup.** Robin runs `/acq:setup`, opens the Scorecard, and works through Setup.
   - Gates: food service, outside Example State, and owner-is-the-product as hard gates; franchise resales as a soft gate; car washes screened out by the digest only.
   - Criteria: the starter ten. Robin rewrites the anchors in their own words and takes the quiz. "Deal math" and "owner dependence" come out with the heaviest downside weights: Robin can live with a dull business, not with one that falls apart when the owner leaves.
2. **The digest.** A week of listing alerts come in. The digest skips a café (food service) and a car wash (Robin's screen-out), loads six listings facts-only, and puts one in "Worth a look": **Northwind Bike Shop**, asking $600K, SDE $240K, revenue $1.2M, 12 years open and growing, 22 minutes away.
3. **First look.** Robin scores the judgment calls: revenue predictability 4 (service contracts plus regulars), seasonality 3, team 4 (a shop manager runs the floor), owner dependence 3, transition support 2 (the seller wants out in a month), operator upside "?" (can't tell from the listing). Premises: a storefront with 5–10 years left on the lease. The listing mentions transferable fleet-service contracts, a +2 perk.
   - The Scorecard does the math with Robin's settings: total project $660K, a $360K loan at 10% (prime 7% + the 3-point SBA cap for loans over $350K ⚑), payments of about $58.6K a year, **DSCR 2.04**, take-home **$181K**. Deal math scores 3 (the take-home band is the lower one).
   - **Fit 81**, Joy 4: **Go look.** One flag: the home-lien gap, since the shop's equipment isn't listed and the loan isn't covered by business assets. The broker-questions list includes "what equipment, vehicles and receivables come with the business?"
   - "Challenge me" is likely to point out that a one-month handover from an owner who's a face of the shop deserves a question before Robin gets attached.
4. **Engage.** Robin calls the broker, then runs `/acq:graduate-deal`. The deal moves to the Deal Room with a snapshot of its Fit, its open questions split into "for the broker" and "for the seller", and a next action. Before the next call, `/acq:call-prep` gives Robin a one-page brief; afterwards, `/acq:call-debrief` turns the notes into a log entry and marks what got answered.
5. **Documents.** The CIM arrives. Robin saves it in `my-search/deals/northwind-bike-shop/docs/` and runs `/acq:cim-review` (a cited fact sheet, listing claims vs. documents, red flags, deal math at the documents' numbers), then `/acq:financials-workup`. The resulting workbook is built from the same kind of JSON as [`examples/northwind-bike-shop/`](examples/northwind-bike-shop/), with formulas you can audit, charts, and a findings sheet of boons, red flags and things to watch.

Every name, number and business in this walkthrough is made up.

## Repository layout
```
.claude-plugin/marketplace.json   the plugin marketplace (one plugin: acq)
plugins/acq/
  .claude-plugin/plugin.json
  pages/        scorecard.html, deal-room.html, listing-digest.html, partner-quiz.html
  skills/       setup, listing-digest, graduate-deal, call-prep, call-debrief, cim-review, financials-workup
  templates/    config.example.json, criteria-library.json, gate-templates.json
  tools/        fin_workbook.py, excel_refresh.ps1 (Windows, optional)
docs/           METHOD.md (the method), CONFIG.md (config reference), PLAN.md (original design record)
examples/       fictional example data
tools/dev/      maintainer scripts
```

## Changing the toolkit
- The pages are single HTML files with no build step. Each embeds a copy of the template JSON files; after editing anything in `plugins/acq/templates/`, run `python tools/dev/sync_templates.py` (add `--check` to only verify).
- Validate the plugin with `claude plugin validate ./plugins/acq`. To try it without installing, start Claude Code with `claude --plugin-dir ./plugins/acq`.
- Decisions and their reasons are in [DECISIONS.md](DECISIONS.md); status and test records in [PROGRESS.md](PROGRESS.md).
- Example data must be obviously fictional.

## Known limits
- Built around US small-business acquisitions and SBA 7(a) financing. Other countries' lending rules aren't modeled.
- Listing-site parsing is written for BizBuySell, BizQuest and Acquire alerts; others are best effort.
- The deal skills and the digest are adapted from tools used in one real search; this blank version has been tested on fictional data, not yet on someone else's real search.
- No pipeline dashboard or valuation model in v1.

## License
[MIT](LICENSE).
