# R(3,5) — 検証記録

## 現在の状態

R35-C001（証明書の回避条件）・R35-C002（下界）は `PROVEN × UNREVIEWED`。
2026-09-12の検査は研究担当と同じCodexセッションによる自己検算であり、独立Reviewerの判定はない。
探索コードと検査コードは分離されているが、それだけで独立レビュー済みとはしない。

## 入力・環境

- `certificate.json`: 頂点 `0,...,12` と26辺。探索で得た最大頂点数の証明書。
- `certificates/n05.json` ～ `certificates/n13.json`: 実行中に得た全9証明書。
- Python 3.9.6、標準ライブラリのみ、macOS 13.7.4 arm64で実行。
- 実行場所: リポジトリのルート。
- 証明書だけを受け取る `verify.py` は探索コードもログもimport・参照しない。

## 証明書の再検査

```sh
python3 benchmarks/r3-5/verify.py benchmarks/r3-5/certificate.json
python3 -m unittest discover -s benchmarks/r3-5 -p 'test_*.py' -v
```

期待する主要出力は `n=13, edges=26, triples_checked=286, five_sets_checked=1287,
triangles=0, independent_fives=0, valid=true, ramsey_lower_bound=14`。
完全な保存出力は `verification-result.json`。
CLIの終了コードは有効な証明書0、禁止構造を含む証明書1、入力エラー2。

6テストの内容:

1. 5頂点サイクルの受理と列挙数。
2. 複数の頂点数の完全グラフ・空グラフにおける全違反数と列挙数。
3. ラベル付き5頂点グラフ全1024個について、隣接行列の `trace(A^3)/6` による別計算と照合。
4. 両方の禁止構造を持つ8頂点グラフでも、最後まで列挙すること。
5. 不正な型・重複辺・自己ループ・範囲外頂点等の拒否。
6. CLIの成功・不成立・不正JSON・不正型・ファイル欠損に対する終了コード。

テストのグラフは検査器の検証用入力であり、探索候補や新たな下界の発見には使用しない。
全9証明書の検査出力は `all-certificates-verification.json` に保存した。各入力は次で再検査できる。

```sh
for certificate in benchmarks/r3-5/certificates/*.json; do
  python3 benchmarks/r3-5/verify.py "$certificate" || exit 1
done
```

## 探索の再実行

```sh
python3 -u benchmarks/r3-5/search.py --output /tmp/r35-g001-replay --seed 35001 --max-evaluations 5000000 --seconds 1200 --restart-interval 10000
python3 benchmarks/r3-5/verify.py /tmp/r35-g001-replay/certificate.json
cmp benchmarks/r3-5/certificate.json /tmp/r35-g001-replay/certificate.json
```

出力先には空のディレクトリを使う。同じPython環境とパラメータで候補数上限まで進めば、
証明書・評価数・段階別結果は決定的に再現される。時刻・実行時間・プラットフォームの文字列は変わる。
低速な環境では時間上限が先に来る可能性があり、その場合の評価数・到達範囲は異なる。
本セッションでは5,000,000評価の本実験を1回実施した。予算消費後の探索再実行は行わず、証明書の再検査とテストを実施した。

目的関数は三角形数と独立5集合数の和。5頂点から始め、目的関数0になったときだけ頂点数を1増やす。
各サイズでは各辺を独立に確率0.35で入れたグラフから開始する。既存の証明書を初期グラフにしない。
提案の90%は現在の禁止集合から1辺を選び、残りは全辺から選ぶ。
温度は10,000提案ごとに1.5から0.05へ減衰し、ランダム初期化を繰り返す。
`search-result.json` の `restarts` は最初の初期化を含む回数。
これはヒューリスティックであり、全グラフ列挙でも一様サンプリングでもない。

候補評価の定義は `search.py` 冒頭と実行ログに固定されている。
初期化・再始動の目的関数評価または1辺反転の差分評価を各1回と数え、棄却提案も含む。
発見時の整合性assert、証明書検査、テストは候補の提案・探索ではなく、評価数に加算しない。
生ログは `search-progress.jsonl`、集計は `search-result.json`。

## fresh-session評価

- 会話履歴の引継ぎ: `NO`。このタスクに過去のRamsey研究会話は渡されなかった。
- ユーザー入力: リポジトリと `benchmarks/r3-5/goals/G001.md` の指定。
- 最初のcheckout: `e546714`。指定ファイルが存在しなかった。
- Git更新後の入力commit: `1d9ef4ddad02e5a120dddee508bb9c33979d1b3d`。
- 追加情報要求: ユーザーへの質問なし。`git fetch origin` でGoalを取得。
- GitだけでGoalを理解し研究開始: `YES`。実行設定の確認不能項目は欠測と明記。
- 保存資材からの検証: 同じセッションで実施。さらに別のfresh sessionによる再実行は未実施。
- 以上は研究担当の実行記録であり、独立Reviewerによるfresh-session監査は未実施。

## Reviewerへの引継ぎ

証明書・検査器の完全性、下界への帰結、予算、Git開始記録、汚染checkpointの順序を監査する。
`research-notes.md` のClaim台帳に対象commitとDiscovery記録がある。
独立した補助検査を実施する場合、そのコードと出力も保存する。
判定後は本書・研究ノート・証明・benchmark-summaryのレビュー状態を同期する。
