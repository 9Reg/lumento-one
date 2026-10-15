#!/usr/bin/env python3
"""Render keep/advice.html from keep/rules/v1/rules.json (stdlib only, idempotent).

Run from anywhere:  python3 keep/render-advice.py
Refresh yearly: replace rules/v1/rules.json, re-run, commit both.
"""
import html
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
SRC = HERE / "rules" / "v1" / "rules.json"
OUT = HERE / "advice.html"

GROUPS = [
    ("disks", "Your disks"),
    ("health", "Disk health"),
    ("integrity", "File integrity"),
    ("backup", "Backups"),
    ("power", "Power"),
    ("security", "Security"),
]
LEVELS = {"critical": "Critical", "error": "Serious", "warning": "Worth fixing", "info": "Good to know"}


def e(s):
    return html.escape(str(s), quote=True)


def listy(v):
    if not v:
        return "see advisory"
    return v if isinstance(v, str) else "; ".join(str(x) for x in v)


def link(url, text):
    return '<a href="%s" rel="noopener">%s</a>' % (e(url), e(text))


def rule_html(r):
    o = ['<article class="feature" id="%s">' % e(r["id"])]
    o.append('<span class="status">%s</span>' % e(LEVELS.get(r["level"], r["level"])))
    o.append("<h3>%s</h3>" % e(r["title"]))
    o.append("<p>%s</p>" % e(r["say"]))
    if r.get("sides"):
        o.append("<h4>Experts differ: the options</h4><ul>")
        for s in r["sides"]:
            rec = ' <span class="yes">Recommended</span>' if s.get("recommended") else ""
            o.append(
                "<li><strong>%s</strong>%s<br>For: %s<br>Against: %s</li>"
                % (e(s["label"]), rec, e(s["for"]), e(s["against"]))
            )
        o.append("</ul>")
    if r.get("steps"):
        o.append("<h4>What to do</h4><ol>%s</ol>" % "".join("<li>%s</li>" % e(s) for s in r["steps"]))
    if r.get("sources"):
        o.append("<h4>Sources</h4><ul>")
        for s in r["sources"]:
            o.append(
                "<li>%s, %s. Checked %s.</li>"
                % (link(s["url"], s["publisher"]), e(s["date"]), e(s["checked"]))
            )
        o.append("</ul>")
    o.append("</article>")
    return "\n".join(o)


def table(headers, rows):
    o = ['<div class="table-wrap"><table class="compare"><thead><tr>']
    o += ["<th>%s</th>" % e(h) for h in headers]
    o.append("</tr></thead><tbody>")
    for row in rows:
        o.append("<tr>")
        for h, c in zip(headers, row):
            o.append('<td data-label="%s">%s</td>' % (e(h), c))
        o.append("</tr>")
    o.append("</tbody></table></div>")
    return "".join(o)


def main():
    d = json.loads(SRC.read_text(encoding="utf-8"))
    t = d["tables"]
    parts = []
    known = {g for g, _ in GROUPS}
    order = GROUPS + [(g, g.capitalize()) for g in dict.fromkeys(r["group"] for r in d["rules"]) if g not in known]
    n = 0
    for g, heading in order:
        rs = [r for r in d["rules"] if r["group"] == g]
        if not rs:
            continue
        alt = " alt" if n % 2 == 0 else ""
        n += 1
        parts.append(
            '<section class="section%s" id="%s">\n  <div class="wrap">\n    <div class="kicker">Advice</div>\n    <h2>%s</h2>\n    <div class="rules">\n%s\n    </div>\n  </div>\n</section>'
            % (alt, e(g), e(heading), "\n".join(rule_html(r) for r in rs))
        )

    smr = t["smr_models"]
    smr_rows = [
        [e(m["model"]), e(m["vendor"] + " " + m["line"]), e(m["size_tb"]) + " TB", e(m["type"].upper()), ", ".join(link(u, "source") for u in m["sources"])]
        for m in smr["entries"]
    ]
    fam = t["smr_families_not_matched"]
    fam_rows = [
        [
            e(f["vendor"]),
            e(f["family"]),
            e(", ".join("%s TB" % x for x in f["smr_sizes_tb"]) if "smr_sizes_tb" in f else f.get("type", "")),
            ", ".join(link(u, "source") for u in f["sources"]),
            e(f["checked"]),
        ]
        for f in fam["entries"]
    ]
    adv = t["adm_advisories"]

    def score(a):
        if a.get("cvss") is None:
            return e("not scored")
        return e("%s (CVSS %s)" % (a["cvss"], a.get("cvss_version", "")))

    def summary(a):
        txt = a.get("summary", "")
        if a.get("note"):
            txt += ". " + a["note"]
        return e(txt)

    adv_rows = [
        [
            link(a["url"], a["id"]),
            e(a.get("date") or "not stated"),
            e(a.get("cve", "none listed")),
            score(a),
            summary(a),
            e(listy(a.get("affected"))),
            e(listy(a.get("fixed"))),
        ]
        for a in adv["entries"]
    ]
    parts.append(
        '<section class="section%s" id="tables">\n  <div class="wrap">\n    <div class="kicker">Reference tables</div>\n    <h2>Drives and ADM versions</h2>\n'
        "    <h3>Drives that use shingled recording (SMR)</h3>\n    <p class=\"intro\">%s</p>\n    %s\n"
        "    <h3>SMR families not matched by model</h3>\n    <p class=\"intro\">These are published by capacity, not by model number, so KEEP does not match them. They are shown here only. Check your drive's exact model with its maker.</p>\n    %s\n"
        "    <h3>ADM security advisories</h3>\n    <p class=\"intro\">Advisories up to %s. Newer ones are not listed here: see <a href=\"%s\" rel=\"noopener\">Asustor's advisory list</a>.</p>\n    %s\n"
        "  </div>\n</section>"
        % (
            " alt" if n % 2 == 0 else "",
            e(smr["note"]),
            table(["Model", "Drive", "Size", "Type", "Source"], smr_rows),
            table(["Maker", "Family", "SMR sizes", "Source", "Checked"], fam_rows),
            e(d["published"]),
            e(adv["list_url"]),
            table(["Advisory", "Date", "CVE", "Score", "Summary", "Affected", "Fixed in"], adv_rows),
        )
    )

    page = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="The advice lumento KEEP gives about your NAS: disks, backups, file integrity and security, with the sources behind every rule.">
<title>What KEEP teaches — lumento KEEP</title>
<link rel="preconnect" href="https://fonts.bunny.net">
<link rel="stylesheet" href="https://fonts.bunny.net/css2?family=Inter:wght@400;500;600;700&display=swap">
<link rel="stylesheet" href="../styles.css">
</head>
<body>
<header>
  <div class="wrap">
    <nav>
      <a class="brand product-name" href="../index.html">
        <span class="lu">lu</span><span class="mento">mento</span>
      </a>
      <a class="link" href="../index.html#family">The lumento family</a>
    </nav>
  </div>
</header>

<main>
<section class="section">
  <div class="wrap">
    <a class="crumb" href="../keep.html">← lumento KEEP</a>
    <div class="kicker">Advice</div>
    <h1>What KEEP teaches</h1>
    <p class="intro">KEEP only reads your files, so it can't fix anything.  What it can do is tell you what to look at and why.  This page is every rule KEEP uses, in plain words, with the sources behind it.  Where experts disagree, you get each side and the one we recommend.</p>
    <div class="advice-note">
      <p>Rules published %(published)s.  %(attribution)s  Licence: <a href="%(licence_url)s" rel="noopener">%(licence)s</a>.  You may copy and adapt this text if you credit lumento.  The sources linked below are cited, not copied.  The same rules, as data, are in <a href="rules/v1/rules.json">rules.json</a>.</p>
    </div>
  </div>
</section>

%(body)s
</main>

<footer>
  <div class="wrap foot">
    <div class="footer-brand">
      <div class="brand product-name">
        <span class="lu">lu</span><span class="mento">mento</span>
      </div>
    </div>
    <div class="foot-links">
      <a href="../index.html">Home</a>
      <a href="../privacy.html">Privacy</a>
      <a href="../impressum.html">Impressum</a>
    </div>
  </div>
</footer>

</body>
</html>
""" % {
        "published": e(d["published"]),
        "attribution": e(d["attribution"]),
        "licence": e(d["licence"]),
        "licence_url": e(d["licence_url"]),
        "body": "\n\n".join(parts),
    }
    OUT.write_text(page, encoding="utf-8")


if __name__ == "__main__":
    main()
