# Ramsey-benchmark

**Status: v1.0 COMPLETED — 2026-10-25 (Asia/Tokyo).**

本リポジトリの目的は、Ramsey数の既知問題を題材に **Codex（Researcher）とChatGPT（Reviewer / Research Director）を組み合わせた、Gitをsource of truthとする数学研究ワークフロー** を検証することにある。Ramsey数の未解決問題を解決することや、特定モデル・複数担当方式の優越性を証明すること自体をv1.0の達成条件とはしていない。

Stage 1〜4の研究・独立レビュー・再現性確認・PR統合・retrospectiveを完了し、v1.0の検証をここで区切る。**Stage 5は実施しない（現時点で予定なし）**。

## v1.0の成果

| Stage | 数学的成果 | ワークフロー上の成果 |
| --- | --- | --- |
| 1: `R(3,4)` | `R(3,4)=9` — PROVEN × ACCEPTED | 研究と独立レビューを実施 |
| 2: `R(3,5)` | `R(3,5)=14` — PROVEN × ACCEPTED | Gitからのfresh-session研究開始を検証 |
| 3: `R(4,4)` | `R(4,4)=18` — PROVEN × ACCEPTED | PR-only運用、レビューと再現性検査を改善 |
| 4: `R(4,5)` | `R(4,5)≥24` — PROVEN × ACCEPTED、数学workloadはPARTIAL_PROGRESS | 未完了の2M checkpointを別fresh sessionへ引き継ぎ、10Mまでのexact-resume運用をPASS × ACCEPTED |

Stage 4の運用Goalが `SOLVED` であっても、`R(4,5)` の正確値を証明したことにはならない。全StageのDiscoveryは `CONTAMINATED` であり、未知の数学的Discoveryは未検証である。

## 成果物と検証

- [v1.0完成判断・対象範囲・未検証事項](results/v1-completion.md)
- [全Stage結果とClaim状態](results/benchmark-summary.md)
- [Stage 4 retrospective・再現検算](results/stage4-retrospective.md)
- [研究方法論](methodology.md)
- [Codex Goal実行プロトコル](prompts/codex-goal.md)
- [ChatGPT独立レビュープロトコル](prompts/chatgpt-review.md)
- 数学的成果物: [R(3,4)](benchmarks/r3-4/)、[R(3,5)](benchmarks/r3-5/)、[R(4,4)](benchmarks/r4-4/)、[R(4,5)](benchmarks/r4-5/)

実行時artifact、checkpoint、Claim・review原記録は当時の内容で保持する。v1.0完成は、個別Goalの数学的状態やDiscoveryタグを遡及変更しない。

## 再開方針

新しいStageを番号だけを理由に増設しない。未知問題のDiscovery、障害・異環境からのresume、実測モデル比較、単一sessionとの効率比較など、**具体的な意思決定に必要な新規仮説・統制条件・評価予算が定まった場合のみ**、新たなGoalとPRによって再開する。現時点ではStage 5は未定義・未実施。
