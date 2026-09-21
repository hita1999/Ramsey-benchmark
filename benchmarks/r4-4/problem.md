# R(4,4) — 問題設定

## 目的

最小の整数 `N` であって、`K_N` の任意の赤青2彩色が赤または青の `K_4` を含むものを決定する。

グラフ言語では、最小の `N` であって、任意の `N` 頂点単純グラフ `G` が次のいずれかを満たすものを決定する。

- `G` が `K_4` を含む。
- `G` が独立な4頂点集合を含む。

## Stage 3 root

Stage 3の運用上のroot commitは、PR必須rulesetの検証をmainへ統合した

`ab5624e9c411afe50137875811c26b46ecf13551`

とする。

各Goalの実際の研究baseは、そのGoalファイルを含むmainのcommitを研究開始時に記録する。Stage 3 rootとGoal execution baseを混同しない。

## ベンチマーク上の制約

- Web、論文、書籍、OEIS、既知値データベース、reference implementation等から `R(4,4)` の既知値・既知構成・既知証明を検索しない。
- 既知のcritical / extremal graphや既知の分類結果を検索・流用しない。
- 一般的なグラフ理論、組合せ論、Python、SAT/SMT、有限探索、局所探索、対称性削減等は利用してよい。
- 計算で「見つからなかった」ことを不存在証明へ昇格しない。
- 条件を満たす具体的グラフは、禁止された4頂点集合を完全検査できるなら下界の有限証明書として扱ってよい。
- 上界で計算を使う場合は、完全な探索空間・symmetry breaking・再現資材を保存し、heuristic failureと区別する。

## 既知情報を想起した場合

正確な値、既知構成、既知証明方針、既知の主要補題、特定のRamsey graphを想起した場合は、**研究へ利用する前に** `research-notes.md` に具体的内容を記録し、その変更だけを独立checkpoint commitとして保存する。

そのGoalのDiscoveryは原則 `CONTAMINATED` とする。想起した情報の正しさ自体を証拠・探索停止条件・目標頂点数・初期グラフとして使ってはならない。

想起記録がないだけでは `CLEAN` としない。評価に必要な記録が不足する場合は `UNKNOWN` とする。

## Git / PR運用

Stage 3では `main` にactive rulesetが適用され、PR経由の統合が必須である。証跡は `results/stage3-pr-policy-verification.md` にある。

- 研究・checkpoint・review・closureは専用branchからPR経由で統合する。
- `main` への直接push、force push、引数なしpushを行わない。
- push先を明示し、research branchが `origin/main` をupstreamにしていないことを確認する。
- 数学的完了、独立レビュー受理、状態同期、PR統合を別の完了条件として扱う。

## 状態管理

Claimは `methodology.md` §6に従う。

- 数学的状態: `CONJECTURE / COMPUTATIONALLY VERIFIED / PROVEN / REFUTED`
- 独立レビュー状態: `UNREVIEWED / ACCEPTED / NEEDS_REVISION / REJECTED`
- Discovery: `CLEAN / CONTAMINATED / UNKNOWN`

研究担当が証明を完成させても、独立Reviewerが判定するまでは通常 `PROVEN × UNREVIEWED` とする。

## 最終成果物

ベンチマーク全体として最終的に必要なものは次の通り。

1. 下界を与える具体的な有限証明書と独立検査。
2. 上界を与える一般的な証明、または完全性が監査可能な有限計算証明。
3. Claim依存DAG。
4. `proof.md` の人間可読な証明。
5. `verification.md` と `reviews/` の独立レビュー。
6. 計算を使う場合のコード・入力・環境・実行コマンド・結果。
7. 各Goalのmodel/effort、base、数値予算、終了分類、計測値。
8. fresh sessionがGitだけから研究を開始・再開できたかの記録。

## Source of truth

会話履歴ではなくGitリポジトリを研究状態のsource of truthとする。
