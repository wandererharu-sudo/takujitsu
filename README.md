# 擇日こよみ

Googleカレンダーに登録した擇日データ（鍾福堂通書系）から、用途別の吉日をiPhone・PCで即確認できる一枚ページ。

- 公開URL: https://wandererharu-sudo.github.io/takujitsu/
- データ正本: `data/takujitsu.json`（Googleカレンダーから書き出し）
- 更新手順: `data/takujitsu.json` を更新 → `python build.py` → `index.html` を commit & push
- 依存: `python -m pip install lunardate`（六曜の旧暦計算に使用）
