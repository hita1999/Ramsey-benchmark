# R(4,4) — 検証記録

## 現在の状態

研究担当Codexによる有限証明書の完全検査に加え、独立Reviewerの別実装検査も成功。
R44-C001（17頂点の回避グラフ）およびR44-C002（R(4,4)>=18）は **PROVEN × ACCEPTED**。
Discoveryは **CONTAMINATED**。独立レビュー詳細は [reviews/G001.md](reviews/G001.md)。

R44-G002は理論証明により **SOLVED**。新規のR44-L001、R44-C003（上界）、R44-C004（等号）は
**PROVEN × UNREVIEWED**。以下は研究担当の自己監査であり、独立受理ではない。

## R44-G002: 理論証明の自己監査とReviewerへの引継ぎ

- 実行base: `89b05a18ecd69baa2d01c815c7e350bfa7c39841`。
- 対象成果commit: research-notes.mdのG002提出記録参照。
- 依存確認: Stage 1 C005および依存C003/C004はPROVEN × ACCEPTED。
  `../r3-4/proof.md` と `../r3-4/verification.md` でstatement・証明・受理対象head `55444df461ac40c28f1462413416b17dfa9ad44f` を確認。
- 下界確認: `reviews/G001.md` でR44-C002のPROVEN × ACCEPTEDを確認。上界証明内部では使用していない。
- 完全性: 任意の18頂点グラフと任意のvを取り、整数次数0..17をd>=9とd<=8で尽くす。境界8/9を含む。
- 補グラフ変換: 補グラフのK3→元の独立3集合、補グラフの独立4集合→元のK4。
- 頂点の拡張: 近傍の三角形はvへの3辺を加えてK4、非近傍の独立3集合はvへの3非辺を加えて独立4集合になる。
- 非循環: 上界はStage 1 C005→R44-L001→R44-C003だけ。等号の段階でのみR44-C002を結合する。
- 主要依存の理論証明をproof.mdへ再掲したため、上界はproof.md単独で外部資料・一般再帰公式・探索実行を前提にせず追跡できる。
- G002で計算による仮説形成・検算・全探索は行っていない。新規の計算再現資材は不要。
  既存G001 verifierやStage 1の独立計算も本セッションでは再実行していない。
- 自己監査結果: 数学的gapなし。これは独立レビュー、形式証明、全18頂点グラフの機械列挙を行ったという意味ではない。
- Discovery: CONTAMINATED。想起した再帰式・具体的な近傍分割ルートと、summaryから流入したStage 2の経路は
  notes-only `9dd3fcbd2b7d5f5b7c8978be6970429d09a64cd4` に証明作成前に固定。

Reviewer重点項目:

1. Stage 1 C005の正確なstatement、受理状態、proof.md再掲の忠実性。
2. 9頂点以上への制限と補グラフでの向き、非近傍にvが含まれないこと。
3. 18頂点の全グラフ、次数境界8/9、両場合の構造の拡張を網羅していること。
4. 上界がG001探索失敗・証明書の特殊構造・未証明の再帰公式に依存していないこと。
5. 下界は等号結合時だけに使用し、Claim DAGが非循環であること。
6. 契約→汚染checkpoint→成果というGit順序、fresh-session、model/effort欠測、20分予算、明示pushの記録。

独立レビューは別工程。保存先は `reviews/G002.md`、必要な計算資材は `review/`。
Reviewer自身のmodel/effort・日付・対象commit・方法を明示し、研究担当の自己監査と区別する。
closure担当は独立Reviewer（または明示的に引き継いだ担当）とし、proof・research-notes・verification・benchmark-summaryを同期する。
統合担当は同期後にPRをmergeし、merge SHAを記録する。


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
