#!/usr/bin/env python3
"""stats.json → assets/activity-{light,dark}.svg（3 个 KPI，深浅两版）"""
import json, pathlib, sys

data = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "stats.json").read_text())
u = data["data"]["user"]
kpis = [
    (f'{u["contributionsCollection"]["contributionCalendar"]["totalContributions"]:,}', "contributions (all types) · last year"),
    (f'{u["repositories"]["totalCount"]:,}', "public repos"),
    (f'{u["pullRequests"]["totalCount"]:,}', "merged pull requests"),
]

W, H, PAD, GAP = 760, 116, 6, 20
COLS = [(300, 44, True), (190, 26, False), (210, 26, False)]   # 宽度 / 字号 / 是否主数
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
CARD = '''  <text x="{x}" y="{ny}" text-anchor="middle"
        font-family="ui-monospace,SFMono-Regular,Menlo,monospace" font-size="{size}" font-weight="700"
        fill="{ncolor}">{value}</text>
  <text x="{x}" y="90" text-anchor="middle"
        font-family="-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
        font-size="12.5" fill="{dim}">{label}</text>
'''
alt = " · ".join(f"{v} {l}" for v, l in kpis)
for name, t in THEMES.items():
    e = dict(t); e["accent"] = "#0969da" if name == "light" else "#58a6ff"
    cards, x = [], PAD
    for i, ((value, label), (w, size, primary)) in enumerate(zip(kpis, COLS)):
        if i:
            sep = x - GAP // 2
            cards.append(f'  <line x1="{sep}" y1="26" x2="{sep}" y2="{H-26}" stroke="{t["border"]}"/>')
        cards.append(CARD.format(
            x=x + w // 2, value=value, label=label,
            size=size, ny=62 if primary else 60,
            ncolor=e["accent"] if primary else t["num"], **t))
        x += w + GAP
    svg = TPL.format(w=W, h=H, alt=alt, cards="\n".join(cards), **t)
    out = pathlib.Path(f"assets/activity-{name}.svg")
    out.write_text(svg, encoding="utf-8")
    print(f"  {out}  ({len(svg.encode())} bytes)")
