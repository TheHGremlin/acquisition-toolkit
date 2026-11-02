# Config reference (`config/profile`, schema 1)

Your preferences live in one JSON document. The Scorecard stores it in its database as `config/profile`; **Export config** saves a copy to `my-search/config.json` (keep that folder out of git: it's in `.gitignore`). The setup wizard writes all of it; you can also edit the JSON and import it.

A complete fictional example: [`plugins/acq/templates/config.example.json`](../plugins/acq/templates/config.example.json).

> **Not financial, legal or lending advice.** The rate and lien sections are rough US SBA 7(a) assumptions so the napkin math has numbers in it. Check them with a lender.

## `about` and `voice`
`about` is a few sentences in your own words: who you are, what you're good at, what you want from a business. "Challenge me" reads it. `voice` is `"snarky"` (default) or `"plain"`.

## `money`
| Field | Meaning |
|---|---|
| `cashDown` | Cash you'll put into a deal, **after** setting aside your household reserve. |
| `projectCap` | Largest total project you'll take on. Feeds the built-in `cap` gate. |
| `projectFactor` | Asking price → total project (closing costs, fees, working capital). 1.10 = price + 10%. |
| `operatorSalary` | What the business must pay whoever runs it (you, or a hired manager later). DSCR is measured after this. |
| `sdeFloor` | Minimum seller's discretionary earnings (SDE). Feeds the `sdeFloor` soft gate. |
| `loanTermYears` / `realEstateTermYears` | Loan terms for the business share and the real-estate share. |
| `softGatePenalty` | Fit points taken off per active soft gate. |
| `rentFlagPct` | Flag when rent is more than this % of revenue. |
| `tinyLoan` | Below this, the loan is treated as "realistically cash" and coverage shows n/a. |

## `rates` ⚑ check before use
`prime` (with `primeCheckedOn` and `primeSource`) plus `sbaTiers`: the maximum spread over the base rate for variable-rate 7(a) loans by loan size (`upTo: null` = everything above the last tier). A deal's rate = prime + the spread for its loan size. The Scorecard warns when `primeCheckedOn` is more than 60 days old.

## `bands`
Deal-math score = the lower of the take-home band and the DSCR band. `takeHome` and `dscr` are `[threshold, score]` pairs, highest first; below the last threshold scores 1. `dscrGate` is the coverage floor for the `dscr` soft gate (1.25 is a common lender minimum ⚑).

## `gates`
- `builtin`: calculated gates (`cap`, `declining`, `sdeFloor`, `dscr`, `cashOnly`, `commute`, `landLease`, `turnaround`). Each has `tier` (`hard` | `soft`) and `enabled`. `declining` can be `overrulable`, which lets you downgrade it to a soft gate on a specific deal once you know why revenue fell.
- `manual`: gates you tick per deal, copied from [`gate-templates.json`](../plugins/acq/templates/gate-templates.json) or written yourself. Fields: `id`, `label`, `tier` (`hard` | `soft` | `digest-only`), `explain`, optional `text` (e.g. your region), `brokerQ` (soft gates), `digestRule` (how the listing digest recognizes it).

## `criteria`
An ordered list. Each entry is `{id, weight: {up, down}}` referring to [`criteria-library.json`](../plugins/acq/templates/criteria-library.json), optionally overriding `name`, `hint`, `anchors` (`"1"`…`"5"`, 2 and 4 optional) or `brokerQ`. A new `id` with all fields is a custom judgment criterion. Calculated criteria (`dealMath`, `track`, `commute`, `premises`) can be dropped but not redefined.

Weights are two-sided: `up` applies when a deal scores above 3, `down` when it scores below 3. Each set sums to 100.

**Fit = 50 + Σ (score − 3) / 2 × weight**, using `up` above 3 and `down` below 3. All 5s = 100, all 3s = 50, all 1s = 0. An unknown ("?") counts as 2. Then perks and dings (capped at ±`perkCap`) and the soft-gate penalties.

`quiz` records how the weights were made: when, how many circular answers (`loops`), toss-ups, and dealbreaker clicks per criterion.

## `track`
`yearBands`: the years-open thresholds for scores 2, 3, 4 and 5 (below the first = 1). `growthBonus`: added when revenue is clearly growing (capped at 5).

## `geo`
`regionLimit` is free text shown in the region gate. `homeBase` is used only by Claude to estimate drive times: it stays in your database, never in the repo. `presenceLimits` are the longest one-way drives (minutes) you'll accept if you have to be there daily, a few days a week, or weekly (`weeklyStretch` is flagged but allowed). Commute scores 5 within `fullScoreWithin` minutes, sliding to 1 at the limit, plus `presenceBonus`. With `presenceFromTeam`, presence is guessed from the team-in-place score when the listing doesn't say.

## `joy`
Your own 1–5 anchors for "how interesting is this to me?". Joy = the higher of standalone Joy and plan Joy − `planDiscount` (a plan = this deal as step one of something bigger). Quadrants split at `fitCut` and `joyCut`; the siren-song and sensible-shoes callouts use the other four numbers.

## `household`
A callout, no score effect, for when the handover looks thin: at least `minLow` of the listed `criteria` score `lowAtOrBelow` or less and none scores `noneAtOrAbove` or more. `partnerLabel` is how the callout refers to the person you'd talk it over with.

## `lien` ⚑
Flags deals where business collateral (real estate × `reHaircut` + equipment × `ffeHaircut`) is less than the bank loan, since lenders then generally look to personal real estate for the gap. No score effect.

## `perks`, `dings`, `perkCap`
`[label, points]` tags you click on a deal. The total is capped at ±`perkCap`.

## `digest`
Settings for the optional listing-digest skill: `gmailQuery` (the Gmail search that finds your listing alerts), `sites`, and `topTierPreferences` in plain English for the "worth a look" tier.

## `links`
Filled in by `/acq:setup`: the URLs of your own Deal Room and Listing Digest, so pages can link to each other.
