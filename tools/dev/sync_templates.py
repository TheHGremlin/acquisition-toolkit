"""Copy the template JSON files into the pages that embed them.

The pages are single self-contained HTML files (an artifact can't fetch files from this repository),
so each one carries a copy of the templates in <script type="application/json" id="..."> blocks.
Edit the files in plugins/acq/templates/, then run:  python tools/dev/sync_templates.py
Run with --check to fail (exit 1) when a page is out of date, without changing anything.
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
TEMPLATES = ROOT / "plugins" / "acq" / "templates"
PAGES = ROOT / "plugins" / "acq" / "pages"
BLOCKS = {"lib-criteria": "criteria-library.json", "lib-gates": "gate-templates.json", "lib-example": "config.example.json"}


def main():
    check = "--check" in sys.argv
    stale = []
    for page in sorted(PAGES.glob("*.html")):
        html = page.read_text(encoding="utf-8")
        new = html
        for block_id, name in BLOCKS.items():
            data = json.dumps(json.loads((TEMPLATES / name).read_text(encoding="utf-8")), ensure_ascii=False, separators=(",", ":"))
            data = data.replace("</", "<\\/")
            pat = re.compile(r'(<script type="application/json" id="' + block_id + r'">)(.*?)(</script>)', re.S)
            new = pat.sub(lambda m: m.group(1) + data + m.group(3), new)
        if new != html:
            stale.append(page.name)
            if not check:
                page.write_text(new, encoding="utf-8")
    verb = "out of date" if check else "updated"
    print(f"{verb}: {', '.join(stale) if stale else 'none'}")
    sys.exit(1 if check and stale else 0)


if __name__ == "__main__":
    main()
