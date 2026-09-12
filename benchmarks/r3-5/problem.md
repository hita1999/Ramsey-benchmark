# R(3,5) — 問題設定

## 目的

最小の整数 `N` であって、`K_N` の任意の赤青2彩色が次のいずれかを含むものを決定する。

- 赤い三角形 `K_3`
- 青い完全グラフ `K_5`

グラフ言語では、最小の `N` であって、任意の `N` 頂点単純グラフ `G` が次のいずれかを満たすものを決定する。

- `G` が三角形を含む
- `G` が独立な5頂点集合を含む

## ベンチマーク上の制約

- Web、論文、書籍、OEIS、既知値データベース、reference implementation等から `R(3,5)` の既知値・既知構成・既知証明を検索しない。
- 既知のextremal / critical graphや主要な既知補題を意図的に利用しない。
- 一般的なグラフ理論、組合せ論、Python、SAT/SMT、有限探索、局所探索等は利用してよい。
- 計算で「見つからなかった」ことを、そのまま不存在証明へ昇格しない。
- 条件を満たす具体的なグラフは、独立に検査可能なら下界の有限証明書として扱ってよい。

## 既知情報を想起した場合

正確な値、既知構成、既知証明方針、既知の主要補題を想起した場合は、その内容を研究へ利用する前に `research-notes.md` に記録し、独立したcheckpoint commitを作成する。

そのGoalのDiscoveryタグは原則 `CONTAMINATED` とする。想起した情報の正しさ自体を証拠として扱ってはならない。

汚染が報告・検出されていないだけでは `CLEAN` としない。必要な記録が不足する場合は `UNKNOWN` とする。

## 最終成果物

ベンチマーク全体として最終的に必要なものは次の通り。

1. 下界を与える具体的な有限証明書と、その独立検査方法。
2. 上界を与える一般的な証明または、完全性を説明した有限計算証明。
3. 主要Claimの依存関係。
4. `proof.md` に保存された監査可能な証明。
5. `verification.md` に保存された独立レビュー。
6. 計算を利用する場合、その再現に必要なコード・入力・環境・実行コマンド・期待出力。
7. 各Goalの実際のmodel/effort、base commit、数値予算、終了分類、計測値。

## 状態管理

Claimは `methodology.md` §6に従い、次を分離して記録する。

- 数学的状態: `CONJECTURE / COMPUTATIONALLY VERIFIED / PROVEN / REFUTED`
- 独立レビュー状態: `UNREVIEWED / ACCEPTED / NEEDS_REVISION / REJECTED`
- Discoveryタグ: `CLEAN / CONTAMINATED / UNKNOWN`

## Source of truth

会話履歴ではなくGitリポジトリを研究状態のsource of truthとする。

Stage 2では特に、会話履歴を引き継がないfresh sessionが、指定されたGit commitと保存済み成果物だけから研究を開始・再開できるかを評価する。