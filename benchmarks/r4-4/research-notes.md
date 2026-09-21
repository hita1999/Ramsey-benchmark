# R(4,4) — 研究ノート

## 現在の状態

- Benchmark状態: `READY`。Stage 3初期化済み、研究は未開始。
- Stage 3 root: `ab5624e9c411afe50137875811c26b46ecf13551`。
- 現在定義済みGoal: `R44-G001`。
- 完了Goal: 0。
- 数学的Claim: まだなし。
- Discovery: `UNKNOWN`。研究開始前であり、想起が報告されていないことをCLEANとは扱わない。
- main PR policy: `PASS`。詳細は `results/stage3-pr-policy-verification.md`。
- fresh-session研究: 未実施。

## Stage 3初期化

2026-09-21、Stage 2 closure・retrospective・PR policy verification完了後に初期化した。

G001では正確な値をGoalへ埋め込まず、固定予算内で `K_4` も独立4集合も持たない証明書を構成する。
得られた最大頂点数は今回の探索予算内での結果であり、全グラフ中の最大性を意味しない。

研究担当は開始時に次を本書へ追記する。

- Goal execution base commit
- fresh sessionか
- 実際のmodel / reasoning effort
- 数値予算と計測方法
- 作業branchと明示的push先
- 研究開始時点のDiscovery
- 読んだGit内ファイルと追加で得た情報
- 利用前の既知情報想起があれば、その具体的内容とcheckpoint commit

## Claim台帳

まだ新規Claimはない。最初のClaim IDは `R44-C001` から開始する。

## 現在のフロンティア

最初の課題は `R44-G001`。固定予算内で下界証明書を構成し、certificate-only verifierと再現資材を保存する。

探索不成功は上界・不存在・最大性の根拠にしない。

## R44-G001 実行開始契約（2026-09-21）

- Goal execution base: `a0658a0fe5ca5e957b35f9460477fb6ebc089b95`（fetch後のmain HEAD）。
- 初期checkout: `e546714`。未コミット変更なし。originをfetchし、mainをfast-forwardして開始。
- fresh session: yes。ユーザー入力はrepository URLとGoalパスのみ。過去の研究会話を引き継いでいない。
- 読んだGit内文書: 本Goal、problem、research-notes、proof、verification、methodology、prompts/codex-goal、results/stage3-pr-policy-verification、results/benchmark-summary。
- 追加質問なし。外部数学情報源なし。Git取得は当該repositoryの状態取得のみ。
- PR開始条件: 保存済みpolicy verificationのPASS、active main ruleset、bypassなしを確認（新たなサーバー設定監査ではない）。
- researcher: Codex。実際の正確なmodel ID: `missing`、reasoning effort: `missing`。実行設定を確認できる取得元がないため、推奨値を実績として扱わない。
- 作業branch: `codex/r44-g001-lower-bound`（origin/mainをupstreamとしない）。
- 唯一のpush先: `git push -u origin HEAD:refs/heads/codex/r44-g001-lower-bound`。
- 全体wall-clock起点: 2026-09-21T11:51:05Z（goal createdAt、準備を含む）。上限30分、締切12:21:05Z。
- 探索候補上限: 10,000,000。候補1回は初期ランダムグラフの完全スコア評価、または単一辺反転候補の差分スコア評価1回。棄却候補も数える。検証・単体テストは探索候補と分離。
- 方針: n=4から1ずつ増やし、各nで独立なランダム初期化と単一辺反転の焼きなまし。既知値由来の頂点上限を設けない。seed・再始動周期・冷却規則は探索実行前にコードへ固定。
- 文書化・検査・commit用の時間を確保し、探索には全体締切より早い内部締切を設定する。
- 開始counter: `get_goal` 2026-09-21T11:51:12Z、tokensUsed=5295、timeUsedSeconds=7。契約読了時counter: 11:51:52Z、tokensUsed=20536、timeUsedSeconds=47。単位はtool counterであり生成token数・課金量ではない。
- 開始時Discovery: `CONTAMINATED`。既知内容の想起を認識した。次のnotes-only checkpointに具体的内容を保存してから研究を行う。
- この時点の探索評価数: 0。独立レビュー: 未実施。
