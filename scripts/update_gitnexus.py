#!/usr/bin/env python3
"""gitnexus.json → 重写 README.md 里 <!-- gitnexus-stats --> 标记之间的文字。

输入: {"stars": 48446, "mergedPRs": 18}
输出: 标记之间变成 "★48.4k · contributor with **18** merged pull requests"
标记缺失时只警告、不动文件（避免把 README 改坏）。
"""
import json, pathlib, re, sys

START, END = "<!-- gitnexus-stats:start -->", "<!-- gitnexus-stats:end -->"
readme = pathlib.Path("README.md")

def fmt_stars(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k"
    return str(n)

data = json.loads(pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "gitnexus.json").read_text())
text = readme.read_text(encoding="utf-8")
if START not in text or END not in text:
    print(f"warn: README 里找不到 {START} / {END}，跳过", file=sys.stderr)
    sys.exit(0)

body = f'★{fmt_stars(data["stars"])} · contributor with **{data["mergedPRs"]}** merged pull requests'
# 标记必须各占一行：inline HTML 注释会让 GitHub 把整行当原始 HTML，**粗体** 就不生效了
block = f"> {START}\n> {body}\n> {END}"
new = re.sub(r"^> " + re.escape(START) + r"(?:\n> .*)*?\n> " + re.escape(END), block, text, flags=re.M)
if new == text:
    print("no change")
else:
    readme.write_text(new, encoding="utf-8")
    print(f'updated → "{body}"')
