"""Build a deal's financial workup workbook (Excel) from a structured JSON file.

Usage:  python -I fin_workbook.py my-search/deals/<id>/<id>_financials.json my-search/deals/<id>/<id>_Financials.xlsx

The JSON (written by the financials-workup skill from the CBR/CIM, P&Ls and tax returns) holds:
  deal      {id, name, preparedAt, preparedBy, note}
  periods   [{key, label, kind: "year"|"partial", days}]  in time order; a partial period is annualized
            for charts and ratios as value * 365 / days (napkin: ignores seasonality)
  pl        {rows: [{key, label, type: "revenue"|"cogs"|"expense", values{period: n}, sources{period: "CBR p.N"}}],
             statedNet {period: n}, statedNetSource {period: "..."}}
  tax       {rows: [{key, label, values{...}, sources{...}}]}                optional
  sde       {rows: [{label, values{...}, sources{...}}], total: {label, values{...}, sources{...}}}
            rows are the build-up (starting basis, then each add-back with its sign)
  monthly   {label, months: ["Jan 2024", ...], rows: [{key, label, values: [...]}], source}   optional
  mix       {label, rows: [{label, value}], source}                                           optional
  concentration {label, rows: [{label, share}], source}                                      optional
  dealMath  {label, assumptions, rows: [{label, sde, dscr, takeHome, score}], gate}           optional
  charts    [{title, kind, ...}]  see build_charts() for the kinds
  findings  [{kind: "boon"|"flag"|"watch", severity: "high"|"medium"|"low", title, detail, source, ask}]

Every number in the workbook is either typed from a cited source or an Excel formula over those cells,
so the buyer can audit it. Re-saving in Excel (see the skill) caches formula values for later readers.
"""
import json, sys
from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, PieChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.table import Table, TableStyleInfo

INK, MUTED, ACCENT, ACCENT_SOFT, LINE = "25212C", "6C6577", "9446B3", "F2E7F7", "E2DDE8"
SERIES = ["9446B3", "3D5F9E", "2C7A57", "A86A12", "B03445", "6C6577", "C68BDF", "8FAEE6"]
FILL = {"boon": "E3F2EA", "flag": "FBE6E9", "watch": "FBF0DD"}
TEXT = {"boon": "2C7A57", "flag": "B03445", "watch": "A86A12"}
HEAD = PatternFill("solid", fgColor="25212C")
SUB = PatternFill("solid", fgColor=ACCENT_SOFT)
THIN = Border(bottom=Side(style="thin", color=LINE))
MONEY = '#,##0;[Red]-#,##0'
PCT = '0.0%'
RATIO = '0.00'


def hdr(ws, row, values, widths=None):
    for c, v in enumerate(values, 1):
        cell = ws.cell(row=row, column=c, value=v)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = HEAD
        cell.alignment = Alignment(horizontal="center" if c > 1 else "left", vertical="center", wrap_text=True)
    if widths:
        for c, w in enumerate(widths, 1):
            ws.column_dimensions[get_column_letter(c)].width = w


def title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=14, color=INK)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, color=MUTED)


def build(data, out):
    wb = Workbook()
    periods = data["periods"]
    pkeys = [p["key"] for p in periods]
    factor = {p["key"]: (365 / p["days"] if p.get("kind") == "partial" else 1) for p in periods}
    deal = data["deal"]

    # ---------- README ----------
    ws = wb.active
    ws.title = "README"
    title(ws, f"Financial workup: {deal['name']}", f"Prepared {deal['preparedAt']} by {deal.get('preparedBy', 'Claude')}. Confidential: under NDA.")
    lines = [
        "What's here",
        "Findings: boons, red flags and things to watch, color coded, each with its source and what to ask.",
        "Annual P&L: each year's statement in common categories, with formulas for the subtotals and a check against the stated net income.",
        "Tax returns: what was filed, side by side with the P&L where available.",
        "SDE: how the broker (or Claude) got from profit to seller's discretionary earnings (SDE = profit + owner pay + one-off and non-cash costs added back).",
        "Ratios: each cost line as a % of revenue, plus growth, as formulas over the Annual P&L.",
        "Monthly, Mix, Deal math: the monthly view where one exists, revenue by service or customer, and the loan test at different SDE levels.",
        "Charts: the visual version of all of the above.",
        "",
        "How to read it",
        "Blue-grey numbers are typed from the documents (source in the column beside them). Black numbers are formulas.",
        "Partial periods are annualized for charts and ratios (value × 365 ÷ days). That ignores seasonality: napkin math.",
        "These are the seller's numbers. Treat them as claims until diligence checks them against full tax returns and bank statements.",
        "",
        deal.get("note", ""),
    ]
    for i, t in enumerate(lines, 4):
        ws.cell(row=i, column=1, value=t)
        if t in ("What's here", "How to read it"):
            ws.cell(row=i, column=1).font = Font(bold=True, color=ACCENT)
    ws.column_dimensions["A"].width = 130

    # ---------- Findings ----------
    fs = wb.create_sheet("Findings")
    title(fs, "Boons, red flags and things to watch", "Green = boon · Red = red flag · Amber = watch. Sorted by kind, then severity.")
    hdr(fs, 4, ["Kind", "Severity", "Finding", "Detail", "Source", "Ask or verify"], [10, 10, 38, 70, 22, 50])
    order = {"flag": 0, "watch": 1, "boon": 2}
    sev = {"high": 0, "medium": 1, "low": 2}
    for r, f in enumerate(sorted(data.get("findings", []), key=lambda f: (order[f["kind"]], sev[f["severity"]])), 5):
        vals = [{"boon": "Boon", "flag": "Red flag", "watch": "Watch"}[f["kind"]], f["severity"].title(), f["title"], f["detail"], f.get("source", ""), f.get("ask", "")]
        for c, v in enumerate(vals, 1):
            cell = fs.cell(row=r, column=c, value=v)
            cell.fill = PatternFill("solid", fgColor=FILL[f["kind"]])
            cell.alignment = Alignment(wrap_text=True, vertical="top")
            cell.border = THIN
            if c <= 3:
                cell.font = Font(bold=True, color=TEXT[f["kind"]])
    fs.freeze_panes = "A5"

    # ---------- Annual P&L ----------
    ps = wb.create_sheet("Annual P&L")
    title(ps, "Annual P&L in common categories", "Typed values come from the cited pages. Subtotals and the check row are formulas.")
    cols = ["Line"] + [p["label"] for p in periods] + ["Sources"]
    hdr(ps, 4, cols, [36] + [16] * len(periods) + [44])
    rowref = {}
    r = 5

    def put_row(label, values=None, formula=None, bold=False, fmt=MONEY, src=None, key=None, fill=None):
        nonlocal r
        ps.cell(row=r, column=1, value=label).font = Font(bold=bold, color=INK)
        for i, k in enumerate(pkeys, 2):
            col = get_column_letter(i)
            if formula:
                v = formula(col)
                font = Font(bold=bold, color=INK)
            else:
                v = (values or {}).get(k)
                font = Font(bold=bold, color="3D5F9E")
            cell = ps.cell(row=r, column=i, value=v)
            cell.number_format = fmt
            cell.font = font
            if fill:
                cell.fill = fill
        if fill:
            ps.cell(row=r, column=1).fill = fill
        if src:
            ps.cell(row=r, column=len(pkeys) + 2, value=src).font = Font(color=MUTED, size=9)
        if key:
            rowref[key] = r
        r += 1

    def srcs(row):
        s = row.get("sources", {})
        return "; ".join(f"{periods[pkeys.index(k)]['label']}: {v}" for k, v in s.items() if k in pkeys)

    rows = data["pl"]["rows"]
    rev = [x for x in rows if x["type"] == "revenue"]
    cogs = [x for x in rows if x["type"] == "cogs"]
    exps = [x for x in rows if x["type"] == "expense"]
    start = r
    for x in rev:
        put_row(x["label"], x["values"], src=srcs(x), key=x["key"])
    put_row("Total revenue", formula=lambda c: f"=SUM({c}{start}:{c}{r - 1})", bold=True, key="revenue_total", fill=SUB)
    s2 = r
    for x in cogs:
        put_row(x["label"], x["values"], src=srcs(x), key=x["key"])
    put_row("Gross profit", formula=lambda c: f"={c}{rowref['revenue_total']}-SUM({c}{s2}:{c}{r - 1})" if r > s2 else f"={c}{rowref['revenue_total']}", bold=True, key="gross_profit", fill=SUB)
    s3 = r
    for x in exps:
        put_row(x["label"], x["values"], src=srcs(x), key=x["key"])
    e_end = r - 1
    put_row("Total operating expenses", formula=lambda c: f"=SUM({c}{s3}:{c}{e_end})", bold=True, key="opex_total", fill=SUB)
    # Non-operating items (asset-sale gains, misc. income) sit below the line so they don't inflate revenue.
    others = [x for x in rows if x["type"] == "other"]
    s4 = r
    for x in others:
        put_row(x["label"], x["values"], src=srcs(x), key=x["key"])
    o_end = r - 1
    put_row("Net income (computed)", formula=lambda c: f"={c}{rowref['gross_profit']}-{c}{rowref['opex_total']}" + (f"+SUM({c}{s4}:{c}{o_end})" if others else ""), bold=True, key="net", fill=SUB)
    stated = data["pl"].get("statedNet", {})
    put_row("Net income as stated on the P&L", stated, src="; ".join(f"{k}: {v}" for k, v in data["pl"].get("statedNetSource", {}).items()), key="net_stated")
    put_row("Check: computed minus stated (should be 0)", formula=lambda c: f"=ROUND({c}{rowref['net']}-{c}{rowref['net_stated']},0)", key="net_check")
    ps.freeze_panes = "B5"

    # ---------- Tax returns ----------
    if data.get("tax"):
        ts = wb.create_sheet("Tax returns")
        title(ts, "What was filed (Form 1120-S, page 1)", "Compare with the Annual P&L. Big gaps are questions for the broker and the seller's CPA.")
        hdr(ts, 4, ["Line"] + [p["label"] for p in periods] + ["Sources"], [36] + [16] * len(periods) + [44])
        for i, x in enumerate(data["tax"]["rows"], 5):
            ts.cell(row=i, column=1, value=x["label"])
            for j, k in enumerate(pkeys, 2):
                c = ts.cell(row=i, column=j, value=x["values"].get(k))
                c.number_format = MONEY
                c.font = Font(color="3D5F9E")
            ts.cell(row=i, column=len(pkeys) + 2, value=srcs(x)).font = Font(color=MUTED, size=9)
        n = 5 + len(data["tax"]["rows"])
        ts.cell(row=n, column=1, value="Revenue gap: tax return minus P&L").font = Font(bold=True)
        rk = next((i for i, x in enumerate(data["tax"]["rows"], 5) if x["key"] == "revenue"), None)
        ik = next((i for i, x in enumerate(data["tax"]["rows"], 5) if x["key"] == "income"), None)
        for j, k in enumerate(pkeys, 2):
            col = get_column_letter(j)
            if rk:
                c = ts.cell(row=n, column=j, value=f"=IF(OR({col}{rk}=\"\",'Annual P&L'!{col}{rowref['revenue_total']}=\"\"),\"\",{col}{rk}-'Annual P&L'!{col}{rowref['revenue_total']})")
                c.number_format = MONEY
            if ik:
                c = ts.cell(row=n + 1, column=j, value=f"=IF(OR({col}{ik}=\"\",'Annual P&L'!{col}{rowref['net_stated']}=\"\"),\"\",{col}{ik}-'Annual P&L'!{col}{rowref['net_stated']})")
                c.number_format = MONEY
        ts.cell(row=n + 1, column=1, value="Profit gap: tax-return income minus P&L net").font = Font(bold=True)

    # ---------- SDE ----------
    ss = wb.create_sheet("SDE")
    title(ss, "SDE build-up (seller's discretionary earnings)", "Profit plus owner pay plus one-off and non-cash costs. Each add-back is typed from its source; the total is a formula.")
    hdr(ss, 4, ["Line"] + [p["label"] for p in periods] + ["Sources"], [40] + [16] * len(periods) + [44])
    sde = data["sde"]
    for i, x in enumerate(sde["rows"], 5):
        ss.cell(row=i, column=1, value=x["label"])
        for j, k in enumerate(pkeys, 2):
            c = ss.cell(row=i, column=j, value=x["values"].get(k))
            c.number_format = MONEY
            c.font = Font(color="3D5F9E")
        ss.cell(row=i, column=len(pkeys) + 2, value=srcs(x)).font = Font(color=MUTED, size=9)
    tr = 5 + len(sde["rows"])
    ss.cell(row=tr, column=1, value="SDE (computed)").font = Font(bold=True)
    for j, k in enumerate(pkeys, 2):
        col = get_column_letter(j)
        c = ss.cell(row=tr, column=j, value=f"=IF(COUNT({col}5:{col}{tr - 1})=0,\"\",SUM({col}5:{col}{tr - 1}))")
        c.number_format = MONEY
        c.font = Font(bold=True)
        c.fill = SUB
    ss.cell(row=tr, column=1).fill = SUB
    if sde.get("stated"):
        x = sde["stated"]
        ss.cell(row=tr + 1, column=1, value=x["label"])
        for j, k in enumerate(pkeys, 2):
            c = ss.cell(row=tr + 1, column=j, value=x["values"].get(k))
            c.number_format = MONEY
            c.font = Font(color="3D5F9E")
        ss.cell(row=tr + 1, column=len(pkeys) + 2, value=srcs(x)).font = Font(color=MUTED, size=9)
    ss.cell(row=tr + 2, column=1, value="SDE margin (of P&L revenue)")
    ss.cell(row=tr + 3, column=1, value="SDE, annualized for partial periods")
    for j, k in enumerate(pkeys, 2):
        col = get_column_letter(j)
        c = ss.cell(row=tr + 2, column=j, value=f"=IFERROR({col}{tr}/'Annual P&L'!{col}{rowref['revenue_total']},\"\")")
        c.number_format = PCT
        c.font = Font(color=INK)
        c = ss.cell(row=tr + 3, column=j, value=f"=IFERROR({col}{tr}*{factor[k]:.6f},\"\")")
        c.number_format = MONEY
    sde_row = tr

    # ---------- Ratios (formulas over Annual P&L, annualized) ----------
    rs = wb.create_sheet("Ratios")
    title(rs, "Ratios and annualized view", "Partial periods are scaled to a full year (× 365 ÷ days). Napkin: ignores seasonality.")
    hdr(rs, 4, ["Measure"] + [p["label"] + (" (annualized)" if p.get("kind") == "partial" else "") for p in periods], [40] + [18] * len(periods))
    rr = 5
    ratio_rows = {}

    def rrow(label, f, fmt, key):
        nonlocal rr
        rs.cell(row=rr, column=1, value=label)
        for j, k in enumerate(pkeys, 2):
            col = get_column_letter(j)
            c = rs.cell(row=rr, column=j, value=f(col, k))
            c.number_format = fmt
        ratio_rows[key] = rr
        rr += 1

    P = "'Annual P&L'!"
    rrow("Revenue (annualized)", lambda c, k: f"={P}{c}{rowref['revenue_total']}*{factor[k]:.6f}", MONEY, "rev_ann")
    rrow("Total costs incl. COGS (annualized)", lambda c, k: f"=({P}{c}{rowref['revenue_total']}-{P}{c}{rowref['net']})*{factor[k]:.6f}", MONEY, "cost_ann")
    rrow("Net income (annualized)", lambda c, k: f"={P}{c}{rowref['net']}*{factor[k]:.6f}", MONEY, "net_ann")
    rrow("SDE (annualized)", lambda c, k: f"=IFERROR(SDE!{c}{sde_row}*{factor[k]:.6f},\"\")", MONEY, "sde_ann")
    rev_row = ratio_rows["rev_ann"]
    rrow("Revenue growth vs. prior period (annualized)", lambda c, k: "" if k == pkeys[0] else f"=IFERROR({c}{rev_row}/{get_column_letter(pkeys.index(k) + 1)}{rev_row}-1,\"\")", PCT, "growth")
    rrow("Gross margin %", lambda c, k: f"=IFERROR({P}{c}{rowref['gross_profit']}/{P}{c}{rowref['revenue_total']},\"\")", PCT, "gm")
    rrow("Net margin %", lambda c, k: f"=IFERROR({P}{c}{rowref['net']}/{P}{c}{rowref['revenue_total']},\"\")", PCT, "nm")
    for x in exps:
        rrow(f"{x['label']} as % of revenue", lambda c, k, x=x: f"=IFERROR({P}{c}{rowref[x['key']]}/{P}{c}{rowref['revenue_total']},\"\")", PCT, "pct_" + x["key"])
    for x in exps:
        rrow(f"{x['label']} (annualized)", lambda c, k, x=x: f"={P}{c}{rowref[x['key']]}*{factor[k]:.6f}", MONEY, "ann_" + x["key"])

    # ---------- Monthly ----------
    if data.get("monthly"):
        m = data["monthly"]
        ms = wb.create_sheet("Monthly")
        title(ms, m["label"], "Source: " + m.get("source", ""))
        hdr(ms, 4, ["Line"] + m["months"] + ["Total"], [34] + [12] * len(m["months"]) + [14])
        for i, x in enumerate(m["rows"], 5):
            ms.cell(row=i, column=1, value=x["label"])
            for j, v in enumerate(x["values"], 2):
                c = ms.cell(row=i, column=j, value=v)
                c.number_format = MONEY
                c.font = Font(color="3D5F9E")
            last = get_column_letter(len(m["months"]) + 1)
            c = ms.cell(row=i, column=len(m["months"]) + 2, value=f"=SUM(B{i}:{last}{i})")
            c.number_format = MONEY
            c.font = Font(bold=True)
        ms.freeze_panes = "B5"

    # ---------- Mix / concentration ----------
    if data.get("mix") or data.get("concentration"):
        xs = wb.create_sheet("Mix")
        row = 1
        for block in ("mix", "concentration"):
            b = data.get(block)
            if not b:
                continue
            xs.cell(row=row, column=1, value=b["label"]).font = Font(bold=True, size=13)
            xs.cell(row=row + 1, column=1, value="Source: " + b.get("source", "")).font = Font(italic=True, color=MUTED)
            hdr(xs, row + 2, ["Category", "Value" if block == "mix" else "Share of revenue", "Share"], [40, 18, 12])
            first = row + 3
            for i, x in enumerate(b["rows"], first):
                xs.cell(row=i, column=1, value=x["label"])
                if block == "mix":
                    c = xs.cell(row=i, column=2, value=x["value"]); c.number_format = MONEY; c.font = Font(color="3D5F9E")
                    c = xs.cell(row=i, column=3, value=f"=B{i}/SUM(B{first}:B{first + len(b['rows']) - 1})"); c.number_format = PCT
                else:
                    c = xs.cell(row=i, column=2, value=x["share"]); c.number_format = PCT; c.font = Font(color="3D5F9E")
            data[block]["_range"] = (xs.title, first, first + len(b["rows"]) - 1)
            row = first + len(b["rows"]) + 2

    # ---------- Deal math ----------
    if data.get("dealMath"):
        dm = data["dealMath"]
        ds = wb.create_sheet("Deal math")
        title(ds, dm["label"], dm.get("assumptions", ""))
        hdr(ds, 4, ["SDE basis", "SDE", "DSCR", "Loan-test line", "Take-home", "Deal-math score (1–5)"], [44, 14, 10, 14, 14, 20])
        for i, x in enumerate(dm["rows"], 5):
            vals = [x["label"], x["sde"], x["dscr"], dm.get("gate", 1.25), x["takeHome"], x["score"]]
            fmts = [None, MONEY, RATIO, RATIO, MONEY, "0"]
            for j, v in enumerate(vals, 1):
                c = ds.cell(row=i, column=j, value=v)
                if fmts[j - 1]:
                    c.number_format = fmts[j - 1]
            fill = PatternFill("solid", fgColor=FILL["boon"] if x["dscr"] >= dm.get("gate", 1.25) else FILL["flag"])
            for j in range(1, 7):
                ds.cell(row=i, column=j).fill = fill
        dm["_range"] = (ds.title, 5, 4 + len(dm["rows"]))

    build_charts(wb, data, periods, rowref, ratio_rows, sde_row)
    wb.move_sheet("Charts", offset=1 - wb.sheetnames.index("Charts"))  # README, Charts, Findings, ...
    wb.save(out)


def style_series(chart, i0=0):
    for i, s in enumerate(chart.series):
        color = SERIES[(i + i0) % len(SERIES)]
        if isinstance(chart, LineChart):
            s.graphicalProperties.line.solidFill = color
            s.graphicalProperties.line.width = 28000
            s.smooth = False
        else:
            s.graphicalProperties.solidFill = color
            s.graphicalProperties.line.solidFill = color


def build_charts(wb, data, periods, rowref, ratio_rows, sde_row):
    cs = wb.create_sheet("Charts")
    cs["A1"] = f"Charts: {data['deal']['name']}"
    cs["A1"].font = Font(bold=True, size=14, color=INK)
    cs["A2"] = "Partial periods are annualized (napkin). Each chart's data lives on the sheet named in its title note."
    cs["A2"].font = Font(italic=True, color=MUTED)
    n = len(periods)
    rs = wb["Ratios"]
    cats = Reference(rs, min_col=2, max_col=1 + n, min_row=4, max_row=4)
    slot = 0

    def tidy(chart):
        # Newer Excel hides axes openpyxl leaves unspecified; show them, keep legends out of the plot,
        # and make data labels show the value only.
        for c in [chart] + list(getattr(chart, "_charts", [])):
            for ax in (getattr(c, "x_axis", None), getattr(c, "y_axis", None)):
                if ax is not None:
                    ax.delete = False
            if getattr(c, "x_axis", None) is not None:
                c.x_axis.tickLblPos = "low"  # category labels stay at the bottom even when values go negative
            if c.dataLabels is not None:
                for flag in ("showSerName", "showCatName", "showLegendKey"):
                    setattr(c.dataLabels, flag, False)
        if chart.legend is not None:
            chart.legend.position = "b"
            chart.legend.overlay = False

    def place(chart, note=None):
        nonlocal slot
        tidy(chart)
        chart.width, chart.height = 17, 9.5
        anchor_row = 4 + (slot // 2) * 21
        anchor_col = "A" if slot % 2 == 0 else "L"
        cs.add_chart(chart, f"{anchor_col}{anchor_row}")
        if note:
            cs[f"{anchor_col}{anchor_row + 19}"] = note
            cs[f"{anchor_col}{anchor_row + 19}"].font = Font(italic=True, color=MUTED, size=9)
        slot += 1

    for spec in data.get("charts", []):
        kind = spec["kind"]
        if kind == "timeline":
            # Revenue, total costs, net income and SDE over the periods (annualized).
            ch = LineChart()
            ch.title = spec["title"]
            for key in ("rev_ann", "cost_ann", "net_ann", "sde_ann"):
                ref = Reference(rs, min_col=1, max_col=1 + n, min_row=ratio_rows[key], max_row=ratio_rows[key])
                ch.add_data(ref, titles_from_data=True, from_rows=True)
            ch.set_categories(cats)
            ch.y_axis.numFmt = '$#,##0,"K"'
            style_series(ch)
            ch.y_axis.majorGridlines.spPr = GraphicalProperties(ln=LineProperties(solidFill=LINE))
            place(ch, spec.get("note"))
        elif kind == "rows_vs_revenue":
            # Revenue and chosen cost rows (annualized) as bars, with each row's share of revenue as a line.
            bar = BarChart()
            bar.type = "col"
            bar.title = spec["title"]
            for key in ["rev_ann"] + ["ann_" + k for k in spec["rows"]]:
                ref = Reference(rs, min_col=1, max_col=1 + n, min_row=ratio_rows[key], max_row=ratio_rows[key])
                bar.add_data(ref, titles_from_data=True, from_rows=True)
            bar.set_categories(cats)
            bar.y_axis.numFmt = '$#,##0,"K"'
            style_series(bar)
            line = LineChart()
            for key in spec["rows"]:
                ref = Reference(rs, min_col=1, max_col=1 + n, min_row=ratio_rows["pct_" + key], max_row=ratio_rows["pct_" + key])
                line.add_data(ref, titles_from_data=True, from_rows=True)
            line.y_axis.axId = 200
            line.y_axis.numFmt = "0%"
            line.y_axis.crosses = "max"
            style_series(line, i0=3)
            bar += line
            place(bar, spec.get("note"))
        elif kind == "cost_structure":
            ch = BarChart()
            ch.type = "col"
            ch.grouping = "stacked"
            ch.overlap = 100
            ch.title = spec["title"]
            for key in spec["rows"]:
                ref = Reference(rs, min_col=1, max_col=1 + n, min_row=ratio_rows["pct_" + key], max_row=ratio_rows["pct_" + key])
                ch.add_data(ref, titles_from_data=True, from_rows=True)
            ch.set_categories(cats)
            ch.y_axis.numFmt = "0%"
            style_series(ch)
            place(ch, spec.get("note"))
            ch.legend.position = "r"
        elif kind == "monthly" and data.get("monthly"):
            ms = wb["Monthly"]
            m = data["monthly"]
            keys = [x["key"] for x in m["rows"]]
            bar = BarChart()
            bar.type = "col"
            bar.title = spec["title"]
            for key in spec["bars"]:
                i = 5 + keys.index(key)
                bar.add_data(Reference(ms, min_col=1, max_col=1 + len(m["months"]), min_row=i, max_row=i), titles_from_data=True, from_rows=True)
            bar.set_categories(Reference(ms, min_col=2, max_col=1 + len(m["months"]), min_row=4, max_row=4))
            bar.y_axis.numFmt = '$#,##0,"K"'
            style_series(bar)
            if spec.get("lines"):
                line = LineChart()
                for key in spec["lines"]:
                    i = 5 + keys.index(key)
                    line.add_data(Reference(ms, min_col=1, max_col=1 + len(m["months"]), min_row=i, max_row=i), titles_from_data=True, from_rows=True)
                style_series(line, i0=len(spec["bars"]))
                bar += line
            place(bar, spec.get("note"))
        elif kind == "mix" and data.get("mix"):
            sheet, a, b = data["mix"]["_range"]
            xs = wb[sheet]
            ch = BarChart()
            ch.type = "bar"
            ch.title = spec["title"]
            ch.add_data(Reference(xs, min_col=3, min_row=a, max_row=b), titles_from_data=False)
            ch.set_categories(Reference(xs, min_col=1, min_row=a, max_row=b))
            ch.legend = None
            ch.x_axis.scaling.orientation = "maxMin"
            ch.y_axis.numFmt = "0%"
            ch.dataLabels = DataLabelList()
            ch.dataLabels.showVal = True
            style_series(ch)
            place(ch, spec.get("note"))
            ch.y_axis.delete = True  # values are labeled on the bars
        elif kind == "concentration" and data.get("concentration"):
            sheet, a, b = data["concentration"]["_range"]
            xs = wb[sheet]
            ch = PieChart()
            ch.title = spec["title"]
            ch.add_data(Reference(xs, min_col=2, min_row=a, max_row=b), titles_from_data=False)
            ch.set_categories(Reference(xs, min_col=1, min_row=a, max_row=b))
            ch.dataLabels = DataLabelList()
            ch.dataLabels.showPercent = True
            ch.dataLabels.showVal = False
            from openpyxl.chart.series import DataPoint
            for i in range(b - a + 1):
                pt = DataPoint(idx=i)
                pt.graphicalProperties.solidFill = SERIES[i % len(SERIES)]
                ch.series[0].dPt.append(pt)
            place(ch, spec.get("note"))
        elif kind == "dscr" and data.get("dealMath"):
            sheet, a, b = data["dealMath"]["_range"]
            ds = wb[sheet]
            bar = BarChart()
            bar.type = "bar"
            bar.title = spec["title"]
            bar.add_data(Reference(ds, min_col=3, min_row=4, max_row=b), titles_from_data=True)
            bar.set_categories(Reference(ds, min_col=1, min_row=a, max_row=b))
            bar.x_axis.scaling.orientation = "maxMin"
            bar.dataLabels = DataLabelList()
            bar.dataLabels.showVal = True
            bar.y_axis.numFmt = "0.00"
            bar.legend = None
            style_series(bar)
            # Color each bar by whether it clears the loan test.
            from openpyxl.chart.series import DataPoint
            for i, x in enumerate(data["dealMath"]["rows"]):
                pt = DataPoint(idx=i)
                pt.graphicalProperties.solidFill = "2C7A57" if x["dscr"] >= data["dealMath"].get("gate", 1.25) else "B03445"
                bar.series[0].dPt.append(pt)
            place(bar, spec.get("note"))
            bar.y_axis.delete = True  # values are labeled on the bars


if __name__ == "__main__":
    src, out = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        data = json.load(fh)
    build(data, out)
    print("wrote", out)
