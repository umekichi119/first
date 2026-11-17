#!/usr/bin/env python3
"""チラシ郵送の集計。使い方: python3 flyer/report.py [号(例 2026-11)]"""
import csv, sys, collections, pathlib

base = pathlib.Path(__file__).parent
offices = list(csv.DictReader(open(base / "offices.csv", encoding="utf-8")))
sends = list(csv.DictReader(open(base / "sends.csv", encoding="utf-8")))
issue = sys.argv[1] if len(sys.argv) > 1 else (max((s["号"] for s in sends), default=""))

active = [o for o in offices if o["ステータス"] in ("", "送付中")]
sent_ids = {s["id"] for s in sends if s["号"] == issue}
count = collections.Counter(s["id"] for s in sends)

print(f"【{issue or '(未送付)'}号】対象 {len(active)} 件 / 送付済 {len([o for o in active if o['id'] in sent_ids])} 件")
print("\n未送付:")
for o in active:
    if o["id"] not in sent_ids:
        print(f"  {o['id']:>4} {o['事業所名']} ({o['エリア']}) 累計{count[o['id']]}回")
