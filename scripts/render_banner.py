#!/usr/bin/env python3
"""生成 assets/banner-{light,dark}.svg —— 几何共用，只换调色板。

版式：左侧一句定位陈述 + 一行副标题；右侧一个「一份 spec → 两个消费端」的小示意图，
取代原先漂浮的装饰点。高度 200（原 320），把首屏让给内容。
"""
import pathlib

W, H = 1280, 200
PALETTES = {
    "light": dict(
        bg_from="#f6f8fa", bg_to="#eaeff5",
        thread_a="#0969da", thread_b="#1a7f37",
        ink="#1f2328", dim="#57606a", faint="#8b949e",
        line="#c3ccd6", node_fill="#ffffff", node_stroke="#0969da",
    ),
    "dark": dict(
        bg_from="#161b22", bg_to="#1c2128",
        thread_a="#58a6ff", thread_b="#3fb950",
        ink="#e6edf3", dim="#adbac7", faint="#8b949e",
        line="#3d444d", node_fill="#0d1117", node_stroke="#58a6ff",
    ),
}
SANS = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Menlo,monospace"

TPL = '''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img"
     aria-label="Tools that make a codebase walkable — one spec, two consumers">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{bg_from}"/><stop offset="1" stop-color="{bg_to}"/>
    </linearGradient>
    <linearGradient id="thread" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{thread_a}"/><stop offset="1" stop-color="{thread_b}"/>
    </linearGradient>
    <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">
      <path d="M0,0 L8,4 L0,8 z" fill="{line}"/>
    </marker>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bg)"/>
  <rect width="{W}" height="4" fill="url(#thread)"/>

  <!-- 左：一句陈述 -->
  <text x="64" y="86" font-family="{SANS}" font-size="40" font-weight="700" letter-spacing="-0.8"
        fill="{ink}">Tools that make a codebase walkable.</text>
  <text x="64" y="126" font-family="{SANS}" font-size="19" fill="{dim}">call-chain walkthroughs · agent plugins · upstream fixes</text>

  <!-- 右：一份 spec → 两个消费端 -->
  <g>
    <rect x="852" y="77" width="128" height="46" rx="6" fill="{node_fill}" stroke="{line}"/>
    <text x="916" y="106" text-anchor="middle" font-family="{MONO}" font-size="17" fill="{ink}">spec.json</text>

    <path d="M980 100 H 1010" stroke="{line}" stroke-width="2" fill="none" marker-end="url(#arrow)" opacity="0"/>
    <path d="M980 100 H 1012" stroke="{line}" stroke-width="2" fill="none"/>
    <path d="M1012 57 V 143" stroke="{line}" stroke-width="2" fill="none"/>
    <path d="M1012 57 H 1028" stroke="{line}" stroke-width="2" fill="none" marker-end="url(#arrow)"/>
    <path d="M1012 143 H 1028" stroke="{line}" stroke-width="2" fill="none" marker-end="url(#arrow)"/>

    <rect x="1032" y="34" width="184" height="46" rx="6" fill="{node_fill}" stroke="{node_stroke}"/>
    <text x="1124" y="63" text-anchor="middle" font-family="{SANS}" font-size="17" fill="{ink}">Neovim walkthrough</text>

    <rect x="1032" y="120" width="184" height="46" rx="6" fill="{node_fill}" stroke="{node_stroke}"/>
    <text x="1124" y="149" text-anchor="middle" font-family="{SANS}" font-size="17" fill="{ink}">HTML code map</text>
  </g>
</svg>
'''

for name, pal in PALETTES.items():
    out = pathlib.Path(f"assets/banner-{name}.svg")
    out.write_text(TPL.format(W=W, H=H, SANS=SANS, MONO=MONO, **pal), encoding="utf-8")
    print(f"  {out}  ({out.stat().st_size} bytes)")
