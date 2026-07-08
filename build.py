# -*- coding: utf-8 -*-
"""template.html + data/takujitsu.json -> index.html を生成する。
使い方: python build.py  （takujitsu フォルダ内で実行）
データ更新時（10-12月追加など）は data/takujitsu.json を更新してから実行する。
"""
import json, os

base = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(base, "data", "takujitsu.json"), encoding="utf-8"))
data.sort(key=lambda r: r["date"])
tpl = open(os.path.join(base, "template.html"), encoding="utf-8").read()

# --- 月破の計算（日支が月支と冲する日）---
# 検証済み：カレンダー登録済みの月破大耗6日（2026 1-3月）と全一致
# 2026年の節入り日（この日から月支が切り替わる）
TERMS = [
    ("2026-01-05", "丑"), ("2026-02-04", "寅"), ("2026-03-05", "卯"),
    ("2026-04-05", "辰"), ("2026-05-05", "巳"), ("2026-06-05", "午"),
    ("2026-07-07", "未"), ("2026-08-07", "申"), ("2026-09-07", "酉"),
    ("2026-10-08", "戌"), ("2026-11-07", "亥"), ("2026-12-07", "子"),
]
CHONG = {"子": "午", "丑": "未", "寅": "申", "卯": "酉", "辰": "戌", "巳": "亥",
         "午": "子", "未": "丑", "申": "寅", "酉": "卯", "戌": "辰", "亥": "巳"}

def month_branch(d):
    mb = "子"  # 1/1〜1/4 は前年12月の子月
    for t, b in TERMS:
        if d >= t:
            mb = b
    return mb

for r in data:
    day_branch = r["kanshi"][1]
    if day_branch == CHONG[month_branch(r["date"])] or "月破大耗" in r["items"]:
        r["geppa"] = 1

# --- 六曜（旧暦の月＋日から算出。2026年7月分を外部カレンダーと全日照合済み）---
# 依存: pip install lunardate
from lunardate import LunarDate
import datetime
ROKUYO = ["大安", "赤口", "先勝", "友引", "先負", "仏滅"]  # (旧暦月+旧暦日)%6

for r in data:
    d = datetime.date.fromisoformat(r["date"])
    l = LunarDate.from_solar_date(d.year, d.month, d.day)
    r["r"] = ROKUYO[(l.month + l.day) % 6]

# --- 個人相性マーク（日柱 乙巳・用神 水・喜神 木、2026-07-08 鑑定書照合済み）---
# 冲: 日支が亥（巳亥冲）→「▲」。月破と重なれば大凶。
# 吉: 干支の両方に木水が巡る日 →「⭐」
GOOD_KANSHI = {"甲子", "壬子", "甲寅", "壬寅", "乙卯", "癸卯"}
for r in data:
    if r["kanshi"][1] == "亥":
        r["p"] = "冲"
    elif r["kanshi"] in GOOD_KANSHI:
        r["p"] = "吉"

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
out = tpl.replace("/*__DATA__*/[]", payload, 1)
assert out != tpl, "placeholder not found"

open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(out)
print(f"index.html generated: {len(data)} days ({data[0]['date']} - {data[-1]['date']})")
