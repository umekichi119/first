#!/usr/bin/env python3
"""チラシ郵送の集計。
使い方:
  python3 flyer/report.py            最新号の状況(送付済・未送付)
  python3 flyer/report.py 2026-11    指定号の状況
  python3 flyer/report.py last       前回送付した事業所の一覧(今月の準備用)
"""
import csv, sys, collections, pathlib

base = pathlib.Path(__file__).parent
offices = {o["id"]: o for o in csv.DictReader(open(base / "offices.csv", encoding="utf-8"))}
sends = list(csv.DictReader(open(base / "sends.csv", encoding="utf-8")))
issues = sorted({s["号"] for s in sends})
arg = sys.argv[1] if len(sys.argv) > 1 else ""
count = collections.Counter(s["id"] for s in sends)

def line(o):
    return f"  {o['id']:>3} {o['事業所名']} ({o['エリア']}/{o['種別']}) 累計{count[o['id']]}回"

if arg == "last":
    if not issues:
        print("送付履歴なし"); sys.exit()
    last = issues[-1]
    ids = [s["id"] for s in sends if s["号"] == last]
    print(f"【前回({last}号)送付先】{len(ids)}件")
    for i in ids:
        print(line(offices[i]))
    sys.exit()

issue = arg or (issues[-1] if issues else "")
sent = {s["id"] for s in sends if s["号"] == issue}
targets = [o for o in offices.values() if o["ステータス"] == "送付中" or o["id"] in sent]
unsent = [o for o in targets if o["id"] not in sent]
print(f"【{issue or '(未送付)'}号】対象 {len(targets)} 件 / 送付済 {len(sent)} 件 / 未送付 {len(unsent)} 件")
if unsent:
    print("\n未送付(送付中のうち):")
    for o in unsent:
        print(line(o))
undecided = [o for o in offices.values() if o["ステータス"] == "未確認" and o["id"] not in sent]
if undecided:
    print(f"\n未確認(送付対象か未決定): {len(undecided)}件")
