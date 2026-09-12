# Codex Goal プロトコル

この文書は、Gitに保存された状態から境界付きの研究タスクを開始するために用いる。source of truthはGitリポジトリであり、会話履歴は任意で、再開に必須であってはならない。

## Goal契約

各Goalでは、少なくとも次を明示する。

- Goal ID
- 対象benchmark
- Base commit
- 研究課題
- 許可する手段
- 禁止する情報
- 必須成果物
- 達成条件
- Token / 計算予算
- Checkpoint方針
- 停止条件

Goalの完了時または中断時には、Gitへ次を保存する。

1. 新たに確定したClaim
2. 計算でのみ確認された事項
3. 反証された仮説・失敗した方針
4. 残っているケース
5. 現在のボトルネック
6. 次に試すべき具体的な方針
7. 新しいセッションが研究を再開するために十分な情報

予算切れを数学的成功として報告してはならない。

---

# G001 — R(3,4) の下界証明書を構成する

## 対象benchmark

`benchmarks/r3-4/problem.md`

## 研究課題

外部の既知解を参照せず、赤い三角形も青い `K_4` も含まない赤青彩色（同値にグラフ）を、可能な限り多くの頂点上で具体的に構成する。

このGoalの直接の目的は、Ramsey数の正確な値を決定することではない。最初の再現可能かつ独立に検査可能な下界証明書を作成することを目的とする。

## 許可する手段

- 直接的な数学的構成
- Pythonによる探索
- 実行可能な範囲でのbrute force
- local search / randomized search
- SAT/SMTその他の有限制約充足
- 対称性による簡約

## 禁止する情報

- Web検索
- 論文、OEIS、データベース、benchmark repository、reference implementation
- 記憶している既知の正確な値、既知critical graph、既知証明を意図的に利用すること

事前知識を意図せず想起した場合は、`research-notes.md` の「既知情報による汚染」に記録し、その情報自体を根拠として利用しない。

## 必須成果物

最低限、次を残す。

1. 明示的な証明書（edge list、adjacency表現、彩色表現など）
2. 証明書が2種類の禁止構造を含まないことを検査するverifier
3. 検証を再現するための手順
4. Claim IDと正確な状態を記録した `research-notes.md` の更新
5. fresh sessionが同じ失敗を繰り返さないために必要な、失敗した探索方針の簡潔な記録

コードと証明書は `benchmarks/r3-4/` 配下の分かりやすいファイルまたはサブディレクトリに置く。

## 達成条件

次の全てを満たす場合に限り、このGoalを `SOLVED` とする。

- 具体的な証明書がGitに保存されている。
- verifierが決定的に、主張された回避条件を確認する。
- その証明書から主張する下界が直接導かれる。
- 別セッションが何を確定したのか正確に把握できるよう `research-notes.md` が更新されている。

独立検証はG001完了の必須条件ではない。これは別のreview工程で行う。reviewを通過するまでは、結果を「独立検証済み」と表現しない。

## 予算

研究実行には明確な上限を設ける。最初のbenchmarkでは、複雑な基盤を作るより、単純で監査しやすい計算を優先する。

Tokenまたは計算予算の上限が近づいた場合、根拠の弱い結論へ圧縮するのではなく、途中成果をcheckpointとしてGitへ保存する。

## 停止条件

終了時には、研究結果を必ず次のいずれか1つに分類する。

- `SOLVED`
- `PARTIAL_PROGRESS`
- `EXHAUSTED_BUDGET`
- `BLOCKED`
- `NO_PROGRESS`

どの分類で終了しても、停止前に再開可能な研究状態をGitへ保存する。
---

## Stage 1 retrospective後の運用追記（以後のGoalに適用）

- 研究開始前に、Goalごとの契約・base commit・実際のmodel/effort・数値の計算または時間予算をGitへ保存する。推奨設定と実際の設定を区別し、確認できない項目は不明と記録する。
- 既知情報を想起したら、具体的内容と対象Goalを研究ノートへ記録し、独立したcheckpoint commitを作ってから研究を続ける。後から時間順序を推定して埋めない。
- 計測は開始/終了/途中の別、単位、取得元、探索時間/研究時間/レビュー時間の別を記録する。tokenカウンタを生成token数や費用と同一視しない。最終計測を取得できた場合は追記コミットで保存する。
- 履歴なしの再開を評価するGoalでは、会話履歴を引き継がず、渡した入力commit・ファイル一覧と追加で必要になった情報を保存する。同じ会話で再開した場合はその事実を記録する。

背景と残る評価限界は `results/stage1-retrospective.md` を参照する。G001/G002の当時の契約を遡及的に変更するものではない。

### Claim記録の形式

以後のClaim台帳は `methodology.md` §6に従い、数学的状態（CONJECTURE / COMPUTATIONALLY VERIFIED / PROVEN / REFUTED）と独立レビュー状態（UNREVIEWED / ACCEPTED / NEEDS_REVISION / REJECTED）を別フィールドにする。根拠、依存Claim、対象commitを併記する。Discoveryタグ（CLEAN / CONTAMINATED / UNKNOWN）は別管理し、旧UNVERIFIEDを数学的状態として新規使用しない。
