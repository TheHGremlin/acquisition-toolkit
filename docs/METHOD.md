# The method: how to build a scorecard you'll actually trust

The Setup wizard walks you through this, but it helps to know why it asks what it asks. This is the reasoning behind the Scorecard, distilled from one searcher's rebuild of their own screening tool. Most of it was learned by getting it wrong first.

> This is a screening method, not financial, legal or lending advice. The deal math is napkin math with rough US SBA 7(a) assumptions. Check anything that matters with a lender, an accountant and a lawyer.

## 1. What the Scorecard is for
It covers the **first look** only: what you can judge from a listing or a teaser, before an NDA, financials or a call with the seller. The one question at this stage:

> **If the listing is telling the truth, is this worth digging into?**

Missing numbers are normal at this stage. Listings routinely hide SDE, trends and lease terms, and every claim gets verified later anyway. So a gap in the listing is never a reason to rule a deal out: it becomes a question for the broker. What *does* rule a deal out is a walk-away (a gate), a poor fit even in the best case, or a listing that's already sketchy on its own terms (claims that contradict each other or don't add up).

## 2. Two axes, not one score
- **Fit** (0–100): is this a sensible deal for you?
- **Joy** (1–5): how interested are you, or could you be, in owning it?

They're kept apart on purpose. A blended score lets a business you love paper over weak numbers, or a dull but solid one look better than it feels. Plotted against each other:

| | Low Joy | High Joy |
|---|---|---|
| **High Fit** | Sensible shoes | **Go look** |
| **Low Fit** | Hard pass | Siren song |

Joy can come from the business itself, or from where it could lead (step one of something you'd build over time). Plan-only Joy counts a point lower. **Joy never raises Fit**: buyers with a big vision tend to overpay for deal number one because of what it *could* become, so the first deal has to stand on its own numbers.

## 3. Gates vs. criteria
Ask of anything you care about: *would I walk away over this, no matter what else is good?*
- **Yes → it's a gate.** Hard gates put a deal out. Soft gates keep it visible but cost points and make you write down why you're still looking (useful when "no" is your default but you'd hear an exception).
- **No → it's a criterion**, a trade-off that gets weighted.

Mixing them up is the most common way a scorecard goes wrong. A walk-away hidden inside a criterion inflates that criterion's weight and distorts everything else (see §6).

Some gates are calculated from the deal's numbers: total project over your cap, declining revenue, SDE under your floor, failing the loan-coverage test at the asking price, past your commute limit, cash-only and more than your cash, a land lease, a turnaround whose problem isn't operational. The rest are yours: industries you won't run, the region you'll buy in, "the owner *is* the product".

## 4. Choosing criteria
Each criterion should pass four tests:
1. You can judge it from a listing.
2. It varies from deal to deal.
3. It isn't already a gate.
4. You actually care about it.

Ten is a good number. Every criterion adds pairs to the weighting quiz (*n*(*n*−1)/2 per round), and past about a dozen the quiz gets long enough that your answers get sloppy.

Two things are **left out on purpose**:
- **Growth potential.** It belongs to Joy, not Fit (see §2).
- **Price vs. the industry's typical multiple.** Deal math already depends on the asking price, so scoring the price twice double-counts it. The Scorecard shows a "priced rich / priced lean" flag instead.

Some things matter but aren't visible at first look (customer concentration, the owner's real hours). They're questions for the broker and the documents stage, not criteria.

## 5. Anchors: what a 1, 3 and 5 look like
For each judgment criterion, write in your own words:
- **5** = the best you could realistically find;
- **3** = solidly OK;
- **1** = **the worst you'd still accept.** Anything worse is a gate.

That last rule matters most. If your "1" is something you'd actually walk away from, the quiz's comparisons involving it are meaningless (you're comparing a real trade-off with a dealbreaker), and that criterion's weight comes out inflated.

When scoring a deal:
- **Score from evidence in the listing, not the broker's adjectives.** "Huge growth potential!" is not evidence.
- **"?" (unknown) is its own answer.** It counts as 2, shows as a grey badge, and becomes a line in the deal's "Questions for the broker". Listings that hide something usually hide bad news, and hiding shouldn't be rewarded, but it shouldn't be punished like a confirmed 1 either.
- 1s and 5s ask for one line of evidence. It's what keeps you honest when you re-read a deal a month later.

## 6. Weights: the two-round swing quiz
Instead of asking "how important is X?" (everyone says "very"), the quiz asks about trade-offs:
- **Round A:** two criteria, both at their best (your 5s). Which would you rather have?
- **Round B:** both at their worst still acceptable (your 1s). Which would you rather live with? Plus a **dealbreaker** button.

Each round gives a set of weights (the pairwise answers become a ratio matrix; the weights are its row geometric means, AHP-style). That produces **two-sided weights**:
- **Upside weight:** how much a 5 lifts Fit.
- **Downside weight:** how much a 1 drops it.

Some things only matter when they're bad: a business whose customers are loyal to the old owner can sink you, while a business whose customers love the brand is nice but not thrilling. One flat weight would average that away. The Fit formula uses the upside weight above 3 and the downside weight below:

**Fit = 50 + Σ (score − 3) ÷ 2 × weight.** All 3s = 50, all 5s = 100, all 1s = 0. Then perks and dings nudge it (capped), and each soft gate costs a penalty.

Reading your results:
- **Dealbreaker clicks are a signal, not an answer.** A criterion you marked a dealbreaker in many pairs has a walk-away hiding in its "1". Move that part into a gate, or rewrite the anchor to something you'd accept, then retake round B. In the original searcher's first run, one criterion came out with by far the biggest weight. Almost all of it came from a declining-revenue case they'd never accept anyway. Gating the decline and re-anchoring halved the weight, and the rest of the ranking finally made sense.
- **Circular answers** (A over B, B over C, C over A) are normal in small numbers. Lots of them means you were tired or indifferent; toss-ups are allowed for exactly that.
- **A low weight means tiebreaker, not irrelevant.** Keep a criterion at 3–4% if it should break ties between close deals.
- **Similar weights are a finding, not a bug.** If six things matter about equally, spreading the weights artificially would invent preferences you don't have. If scores bunch up across deals, the fix is in the gates and anchors, not the weights.

The quiz is long (about 30–45 minutes for ten criteria). It's worth it. The partner version exists because the person you share a household with may weigh things very differently; their results are for a conversation, not for changing your weights.

## 7. The calculated criteria
- **Deal math.** Total project = (asking + inventory sold on top) × your project factor. The loan is whatever your cash doesn't cover, at prime plus the SBA's maximum spread for that loan size ⚑. DSCR (debt service coverage ratio) = (SDE − your salary) ÷ yearly loan payments; take-home = SDE − payments. The score is the **lower** of a take-home band and a DSCR band, so a deal has to both pay you and be safely financeable. Only EBITDA given? SDE is estimated as EBITDA + your salary, and labeled. Cash-only and seller-note deals are modeled separately.
- **Home-lien flag** (no score effect) ⚑: when business assets don't cover an SBA loan, lenders generally look to personal real estate for the gap. It fires on most goodwill-heavy deals, which is the point.
- **Track record:** years open, plus a bonus for clear growth. Declining revenue is a gate, overrulable later once you know why.
- **Commute burden:** distance only matters as much as the business needs you there. Each presence level (daily, a few days a week, weekly) has its own drive limit.
- **Premises:** lease security × how much the business depends on its location. A short lease on a storefront is a real risk; on a business that could move, it barely matters.

## 8. Trust and the golden ticket
**Trust** (shown, not scored) asks only what a listing can show: do the numbers hang together, is there a believable reason for sale, how many unknowns. Low trust doesn't kill a deal; it tells you how much of the Fit score is vibes.

**Golden ticket:** affordable + performing + claims to run without the owner. If all three are true it's a no-brainer, which is exactly why padded listings claim it. The Scorecard flags it and attaches a "prove it" checklist.

## 9. Calibrate on real listings
Before trusting the tool, score 10–15 real listings **yourself first**, then compare with anything Claude suggests. (Seeing Claude's scores first anchors you; that's why the digest never pre-fills judgment calls.) If good and bad deals land close together, tighten the gates and anchors. Write down every rule you change and why: that log is how you'll remember, three months in, why the Scorecard says what it says.
