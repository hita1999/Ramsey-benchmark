# R(4,4) — 検証記録

## 現在の状態

研究担当Codexによる有限証明書の完全検査に加え、独立Reviewerの別実装検査も成功。
R44-C001（17頂点の回避グラフ）およびR44-C002（R(4,4)>=18）は **PROVEN × ACCEPTED**。
Discoveryは **CONTAMINATED**。独立レビュー詳細は [reviews/G001.md](reviews/G001.md)。


## R44-G001: 独立レビュー結果

- Reviewer: ChatGPT / GPT-5.6 Sol、reasoning effort High。
- 日付: 2026-09-21。
- Goal execution base: `a0658a0fe5ca5e957b35f9460477fb6ebc089b95`。
- 対象数学成果commit: `02b7fee706a2f569be8a9d1f3b5c7aa9324e5078`。
- レビュー開始時PR head: `1028ee0fa1b49df9c201c53c9a24970c11a6e297`。
- R44-C001: **PROVEN × ACCEPTED**。
- R44-C002: **PROVEN × ACCEPTED**。
- R44-G001: `SOLVED` を受理。
- Discovery: `CONTAMINATED`。

独立Reviewerは研究側 `verify.py` / `search.py` をimportしないbitmask実装を使用した。実行環境はPython 3.13.5、Linux x86_64。保存資材:

```text
review/r44-g001-independent.py
review/r44-g001-independent-result.json
```

独立検査結果は17頂点、68辺、全頂点次数8、全 `C(17,4)=2380` 集合、K4=0、独立4集合=0。さらに三角形68個・独立3集合68個を検出したため、clique number = independence number = 3 も確認した。証明書SHA-256は研究記録と一致した。

従って保存グラフは単色K4を避けるK17の2彩色を与え、定義から `R(4,4)>17`、すなわち `R(4,4)>=18` が従う。

探索全体の10,000,000候補は独立再実行していない。n=18での探索不成功は数学的Claimに使われておらず、C001/C002の受理は保存証明書だけに依存する。

汚染記録の順序は `fb433354`（開始契約）→ `8ca54fd7`（notes-only contamination checkpoint）→ `abb6dfd5`（探索・verifier実装）→ `02b7fee7`（成果）の順であることを確認した。既知値・Paley構成の想起があったためDiscoveryはCLEANへ変更しない。

fresh-session handoff、budget、model/effort欠測、明示的branch pushの記録はGit上で整合している。Reviewerは当該研究セッション自体を再演していないため、fresh-session評価は保存記録に基づく運用監査であり、探索再現とは区別する。

## 研究側の検査

- 入力: `run/certificate.json`、17頂点68辺。
- verifier: `verify.py`。探索コードをimportせず、証明書だけを入力する。
- 実行環境: `environment.json`、Python 3.9.6、macOS 13.7.4 arm64。
- 実行コマンド: `reproduce.md`。
- 全C(17,4)=2380集合を検査。K4=0、独立4集合=0、valid=true。
- 保存結果: `verification-result.json`。n=4..17の全14証明書の検査は `all-certificates-verification.json`。
- `verify.py` と証明書のみをtemporary directoryへコピーし、`python3 -I` で実行成功。
  結果と入力hashは `isolated-verification.json`。ソース依存性の独立性を示し、Reviewerの独立性を示すものではない。
- `test-results.txt`: 7テスト成功。n<=5の全1,100 labeled graphsを別の隣接行列oracleと比較。
  不正形式、空/完全グラフの全件検査、両種の違反を含むグラフ、全保存証明書も検査。
- 探索スコアは全4頂点グラフの全辺反転と、9頂点での1,000反転列について完全再計算と一致。
  これらのテストは探索候補を増やす研究実験ではなく、実装検査である。

全探索を再実行した別fresh sessionはまだない。保存証明書の全列挙検査は実際に実行済み。
CLIの不正JSONはinvalid/exit 1として扱う。形式検査を通過しない入力のchecked件数0は、
有効な証明書を検査したという意味ではない。

## 研究提出時の独立Reviewerへの引継ぎ（履歴）

以下は研究提出当時の記録であり、上記独立レビューで完了した。

レビューartifactの保存先は `benchmarks/r4-4/reviews/G001.md`。
補助計算資材は `benchmarks/r4-4/review/` に研究側と別のコード・環境・コマンド・結果として保存する。
対象研究commitは専用PRの提出commit（research-notesの提出記録参照）、
baseは `a0658a0fe5ca5e957b35f9460477fb6ebc089b95`。

Reviewerは証明書の形式、全4集合の両禁止構造不存在、下界の論理、verifier完全性、テスト、
heuristic failureの扱い、想起checkpointの時系列、fresh sessionとbase、model/effort欠測、
候補数・時間・PR-only運用を確認する。実際の再実行とコード保存を区別する。
Reviewer自身のmodel/effort・日付・対象commit・独立性を記録する。

レビュー後のclosure担当は独立Reviewer（または明示的に引き継いだclosure担当）。
同じclosure PRでproof・research-notes・verification・results/benchmark-summaryの4文書を同期する。
統合担当は同期を確認してからGitHub上でmergeし、merge SHAを記録する。
本研究担当は独立受理・統合完了を代行して宣言しない。
