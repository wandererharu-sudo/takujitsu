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

payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
out = tpl.replace("/*__DATA__*/[]", payload, 1)
assert out != tpl, "placeholder not found"

open(os.path.join(base, "index.html"), "w", encoding="utf-8").write(out)
print(f"index.html generated: {len(data)} days ({data[0]['date']} - {data[-1]['date']})")
