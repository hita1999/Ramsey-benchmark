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

## Stage 2 retrospective後のPR・handoff手順

背景とサーバー側の必須設定は [Stage 2 retrospective](../results/stage2-retrospective.md) を参照する。

- Stage 3の研究開始前に、管理担当が保存した `results/stage3-pr-policy-verification.md` で、
  mainのPR必須設定・bypass制限・確認主体と日付を確認する。証跡がなければ開始条件未達として記録する。
- fresh sessionにはbase commit、Goalパス、必読ファイルを渡す。古いcheckoutからfetchした場合は、
  当初commitと実際に開始したcommit、追加質問・情報源を記録する。
- 作業は `git switch --no-track -c codex/<goal> origin/main` などで作る専用ブランチで行う。
  push前にbranch・remote・upstream・差分を確認する。mainをupstreamにしたまま送信しない。
- pushが許可された作業では `git push -u origin HEAD:refs/heads/codex/<goal>` と送信先を明示する。
  引数なしpush、mainへの直接push・force push、`--all`、`--mirror`、ローカルmainへのmerge後のpushは行わない。
- 成果・checkpoint・運用文書・レビュー・closure・事故復旧はPR経由で統合する。
  PRにはbase/result commit、Goal状態、Claim状態、Discovery、検証、残課題を保存する。
  数学的にSOLVEDでもレビュー前はUNREVIEWED。未完了checkpointも状態を明示して保存できる。
- Reviewerへの引継ぎでレビューartifactの保存先と4文書の同期担当を指定する。
  統合担当は状態同期を確認してGitHub上でmergeし、merge SHAを記録する。
- 事故時は送信を止め、refと履歴・影響を保存する。revertと再適用は差分を確認して復旧PRで行い、履歴を消して事故を隠さない。

## Stage 3 retrospective後の入力・計測・統合記録

[Stage 3 retrospective](../results/stage3-retrospective.md)に基づき、以後は次も明記する。

- Goal設計担当は研究開始時の必読ファイル集合を固定する。独立に方針を考える段階では、
  他Stageの具体的な証明経路を含む横断サマリーを一律に必読にしない。
  受理済みClaimの利用が必要になったらstatement・証明・reviewを確認し、出典と時点を記録する。
  偶発的なstrategy流入はファイル名にかかわらず、利用前に独立checkpointへ記録する。
- 成果commit時・PR提出時・Goal完了時のcounterを別のphaseとして保存する。
  最終counter取得後の記録commit/pushは後処理として区別する。取得不能なら最後のsnapshotと未計測区間を明示し、
  PR提出時counterをGoal完了時counterと呼ばない。研究・レビュー・closureの工数を合算する際も同じ終点を確認する。
- 統合担当はmerge後のSHA・日時・残工程を保存する担当と保存先を明示する。
  次の文書PRへまとめて記録してよいが、mainへ直接追記しない。現在地の「統合待ち」はその記録で更新し、
  提出時点の未統合記録は履歴として残す。
- 停滞時の切替・checkpoint条件は実行前に固定する。未知問題向けの次実験では、
  未完了checkpointから別fresh sessionへ引き継ぐ能力を、完成済み成果の再現とは別に評価する。
