# Furima Seller Toolkit

フリマ・ECの個人出品者のための、返信テンプレート集と小さな生成ツールです。
メルカリなどでよくある場面（在庫切れ、発送遅延、値下げ交渉、キャンセル依頼など）の
日本語テンプレートを、コピペではなく「変数を埋めて生成」できる形で提供します。

A small, dependency-free toolkit for individual flea-market / EC sellers:
polite Japanese reply templates for common situations (out of stock,
shipping delay, price negotiation, cancellation requests), rendered
from simple Markdown templates with `{variables}`.

## 使い方 / Usage

Python 3.10+ があれば動きます。外部ライブラリは不要です。

```bash
# テンプレート一覧
python seller_templates.py list

# テンプレートと変数を確認
python seller_templates.py show out_of_stock

# 変数を埋めて生成
python seller_templates.py render out_of_stock \
  --set item_name=シルクスカーフ \
  --set alt_item=ウールスカーフ \
  --set alt_detail=色違い・未使用 \
  --set alt_price=7500
```

埋めていない変数は `{item_name}` のようにそのまま残り、
標準エラーに未入力の一覧が出るので、送信前の見落としを防げます。

## テンプレート一覧 / Templates

| ファイル | 場面 |
|---|---|
| `out_of_stock` | 在庫切れの説明と代替品の提案 |
| `shipping_delay` | 発送遅延のお詫び |
| `price_negotiation` | 値下げ交渉への丁寧な返信 |
| `cancel_request` | キャンセル依頼への対応（全額返金） |
| `shipping_done` | 発送完了の連絡 |
| `question_reply` | 購入前の質問への返信 |
| `price_accept` | 値下げ了承の返信 |

テンプレートは `templates/` フォルダの Markdown ファイルです。
自分の言葉に合わせて自由に編集してください。

## Premium Pack（有料版）

全9テンプレートに、各テンプレートの記入例と送信前チェックポイント、
共通の送信前チェックリストを付けた Premium Pack を Gumroad で販売しています。
返品相談・まとめ買い相談の2テンプレートは Premium Pack のみの収録です。

A Premium Pack with all 9 templates — each with a filled example and
pre-send checks, plus a shared checklist — is available on Gumroad.
Two templates (returns and bundle purchases) are exclusive to the pack.

→ **Premium Pack Vol.1（$5.00）: https://tongjiejoy.gumroad.com/l/rekrub**

## ロードマップ / Roadmap

- [ ] テンプレート追加（返品相談、まとめ買い相談）
- [ ] 複数プラットフォーム向け表記（メルカリ / ラクマ / Yahoo!フリマ）
- [ ] 英語テンプレート
- [ ] 発送期限チェックなど、在庫・発送まわりの小物ツール

## ライセンス / License

MIT License. See [LICENSE](LICENSE).
