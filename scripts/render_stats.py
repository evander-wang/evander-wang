#!/usr/bin/env python3
"""stats.json → assets/activity-{light,dark}.svg（3 个 KPI，深浅两版）"""
import json, pathlib, sys

data = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "stats.json").read_text())
u = data["data"]["user"]
kpis = [
    (f'{u["contributionsCollection"]["contributionCalendar"]["totalContributions"]:,}', "contributions · last year"),
    (f'{u["repositories"]["totalCount"]:,}', "public repos"),
    (f'{u["pullRequests"]["totalCount"]:,}', "merged pull requests"),
]

W, H, PAD, CARD_W, GAP = 760, 116, 6, 236, 20
THEMES = {
    "light": dict(bg="#ffffff", border="#d0d7de", num="#1f2328", dim="#57606a"),
    "dark":  dict(bg="#161b22", border="#30363d", num="#e6edf3", dim="#8b949e"),
}
TPL = '''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
     aria-label="{alt}">
  <rect width="{w}" height="{h}" rx="10" fill="{bg}" stroke="{border}"/>
{cards}
</svg>
'''
CARD = '''  <text x="{x}" y="58" text-anchor="middle"
        font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="34" font-weight="700"
        fill="{num}">{value}</text>
  <text x="{x}" y="84" text-anchor="middle"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="13" fill="{dim}">{label}</text>
'''
alt = " · ".join(f"{v} {l}" for v, l in kpis)
for name, t in THEMES.items():
    cards, x = [], PAD
    for i, (value, label) in enumerate(kpis):
        if i:
            sep = x - GAP // 2
            cards.append(f'  <line x1="{sep}" y1="30" x2="{sep}" y2="{H-30}" stroke="{t["border"]}"/>')
        cards.append(CARD.format(x=x + CARD_W // 2, value=value, label=label, **t))
        x += CARD_W + GAP
    svg = TPL.format(w=W, h=H, alt=alt, cards="\n".join(cards), **t)
    out = pathlib.Path(f"assets/activity-{name}.svg")
    out.write_text(svg, encoding="utf-8")
    print(f"  {out}  ({len(svg.encode())} bytes)")
