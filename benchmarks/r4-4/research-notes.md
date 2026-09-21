# R(4,4) — 研究ノート

## 現在の状態

- Benchmark: 上下界と等号の数学的証明を保存済み。上界・等号は独立レビュー待ち。
- R44-G002: **SOLVED**（研究完了、独立レビュー・PR統合は別工程）。R44-L001/C003/C004は **PROVEN × UNREVIEWED**。
- R44-G001: **SOLVED**。独立レビュー受理済み。PR #10でmainへ統合済み（merge `4a459b19723dbe8f177c7ad07af75d23fa62dd79`）。
- G001の最大証明書: 17頂点68辺。n=4..17の全14証明書を保存。
- `R44-C001` / `R44-C002`: **PROVEN × ACCEPTED**。
- Discovery: **CONTAMINATED**。利用前checkpoint `8ca54fd7a4dbc751da870e658d5967185e90dfb2`。
- G001探索停止: `EXHAUSTED_BUDGET`（10,000,000候補、124.310935125秒）。G002では探索なし。
- fresh-session研究開始: 実施済み。詳細は実行契約・handoff評価。
- PR policy開始条件: 保存済みPASS確認。mainへの直接pushなし。

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

| ID | 正確な主張 | 数学的状態 | 独立レビュー | 根拠 | 依存 | 対象commit |
|---|---|---|---|---|---|---|
| R44-C001 | 保存した17頂点68辺のグラフにK4も独立4集合もない | PROVEN | ACCEPTED | run/certificate.json、研究側verifier、独立bitmask検査、proof.md | なし | `02b7fee706a2f569be8a9d1f3b5c7aa9324e5078` |
| R44-C002 | R(4,4)>=18 | PROVEN | ACCEPTED | proof.mdの定義と単調性、`reviews/G001.md` | R44-C001 | C001と同じ |
| R44-L001 | 9頂点以上の任意のグラフはK3または独立4集合を含み、かつK4または独立3集合を含む | PROVEN | UNREVIEWED | proof.mdの9頂点への制限と補グラフ変換 | Stage 1 C005（PROVEN × ACCEPTED） | G002数学成果commit（下記提出記録） |
| R44-C003 | 任意の18頂点グラフにK4または独立4集合がある。従ってR(4,4)<=18 | PROVEN | UNREVIEWED | proof.mdのd>=9 / d<=8の全場合 | R44-L001 | G002数学成果commit |
| R44-C004 | R(4,4)=18 | PROVEN | UNREVIEWED | 受理済み下界と本Goalの上界の結合 | R44-C002、R44-C003 | G002数学成果commit |

Discoveryは全ClaimともCONTAMINATED。証明書hashはproof.mdに固定。

## 現在のフロンティア

G001の独立レビューとmain統合は完了し、R44-C001/C002は `PROVEN × ACCEPTED`。
G002で上界R44-C003と等号R44-C004を証明した。数学的な未解決gapはない。
次の工程は独立ReviewerによるR44-L001/C003/C004の監査、4文書のclosure同期、PR統合。
G001の探索失敗・17頂点証明書の構造は上界に使用していない。


## R44-G001 独立レビューとclosure（2026-09-21）

- Reviewer: ChatGPT / GPT-5.6 Sol、reasoning effort High。
- 対象数学成果commit: `02b7fee706a2f569be8a9d1f3b5c7aa9324e5078`。
- レビュー開始時PR head: `1028ee0fa1b49df9c201c53c9a24970c11a6e297`。
- レビュー記録: `reviews/G001.md`。
- 独立計算: `review/r44-g001-independent.py` と `review/r44-g001-independent-result.json`。
- 判定: R44-C001 / R44-C002とも **PROVEN × ACCEPTED**。R44-G001の `SOLVED` を受理。
- Discovery: **CONTAMINATED** を維持。
- 独立計算では研究側verifierをimportせず、17頂点68辺、全次数8、全2,380個の4集合、K4=0、独立4集合=0を確認した。さらに三角形68個・独立3集合68個を確認し、clique numberとindependence numberがともに3であることを別経路で確認した。
- 10,000,000候補探索そのものの独立再実行はしていない。下界証明は保存証明書だけで完結するため、数学的受理には不要。
- fresh-session handoffは保存記録に基づく運用監査として整合的と判定したが、Reviewerが研究開始セッションを再演したものではない。
- 汚染checkpoint `8ca54fd` が探索実装 `abb6dfd` と成果 `02b7fee` より前に存在することをGit履歴で確認した。
- review closureとしてproof・research-notes・verification・benchmark-summaryの現在状態を同期した。研究提出時のUNREVIEWED記録は履歴として保持する。
- PR #10は2026-09-21にmerge `4a459b19723dbe8f177c7ad07af75d23fa62dd79` でmainへ統合された。

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

## 既知情報による汚染 — 利用前独立checkpoint

2026-09-21、契約読了時に、事前学習由来の `R(4,4)=18` という既知値と、17頂点のPaley graph（法17で平方剰余差を辺とする構成）が下界を与えるという内容を想起した。
この想起自体は証拠として採用せず、正誤の外部確認もしない。Discoveryは `CONTAMINATED`。
想起内容を目標頂点数、停止条件、search horizon、初期グラフ、証明根拠として使わない。
この追記だけを独立commitに保存する時点で探索評価数は0であり、探索コード・証明書はまだ作成していない。
使用する探索はn=4からの一般的なランダム局所探索であり、既知構成の辺集合・巡回対称性を入力しない。
記憶の影響が完全に排除されたと主張せず、数学的なcertificate検査とDiscovery評価を分離する。

## 実験結果と失敗した方向

- 実行コード固定commit: `abb6dfd55dcd3df2dc40846790f1f85b27192850`。
- seed=20260921、50,000提案/再始動、温度1.5から0.05。全nで一般的ランダム初期化、対称性・既知構成なし。
- n=4..17は各1初期化内で成功。17頂点は累積101,602候補、探索開始から約1.034秒で発見。
- n=18では198初期化（最後の周期は途中）を実行し、違反数の最良値9、停止時11。成功証明書なし。
- 初期グラフ評価212回、反転候補9,999,788回、合計10,000,000回。候補予算で停止し、600秒の内部探索時間上限には未到達。
- 焼きなましの単一辺反転で18頂点の違反を0にできなかったことだけが失敗結果。
  他の方式を試したという記録はなく、局所最適性・不存在・最大性の主張もない。
- ボトルネックは大きいnの局所探索で違反が残ること。別Goalで予算を与えるならSAT符号化や完全なケース探索を検討できるが、その完全性は別途証明が必要。
- 本Goalの候補予算を使い切ったので追加探索は行わない。

探索の開始・終了UTC、純粋な探索時間は `run/search-result.json`。
探索時間は `time.monotonic()`、UTCはOS wall-clock、Goal counterは別の取得元であり、時計差・計測区間差がある。
UTC差とmonotonic差を同一視しない。Goalの30分上限は準備から文書化・成果物commitまでを含めて管理した。
開始・途中・提出時の利用可能counterは `goal-measurements.json`。生成token数・費用の推定ではない。

## 手法と完全検査

候補1回の定義、seed、再始動規則、時間上限、再現コマンドは `search.py`、`run/search-config.json`、`reproduce.md` に固定。
探索スコアは全4集合内の辺数cについてc=0または6の件数。
辺追加時はその辺を含む4集合だけが変化し、c=0なら-1、c=5なら+1、それ以外0。
辺除去時はc=6なら-1、c=1なら+1、それ以外0。採用時のみ関連集合の辺数を更新する。
この探索最適化の正しさに依存せず、別のcertificate-only verifierで全証明書を検査した。
7テストと隔離実行成功を保存。研究担当の検算であり、独立レビュー未実施。

## fresh-session handoff評価

ユーザーからrepository URLとGoalパスだけを受け取り、会話履歴なしでGit文書から開始・実行できた。
初期checkoutは古くGoalパスが存在しなかったためfetchとfast-forwardが必要だった。
追加の数学情報・既知値のユーザー提供は不要だった。想起した事前学習情報は別checkpointに記録した。
正確なmodel ID/effortは取得できず `missing`。推奨設定で実行したという主張はしない。

この評価は今回の研究開始handoffについての自己記録である。
別fresh sessionによる探索全体の再実行・独立レビュー・未知問題への転用性能の実証ではない。
次セッションはGoal、problem、research-notes、proof、verification、reproduce、run/search-result、
goal-measurements、およびPR記録から研究状態を復元できる。

## 研究提出時の独立レビューとclosureの引継ぎ（履歴）

以下は研究提出時点の引継ぎ記録であり、その後の独立レビューで解消した。

保存先 `reviews/G001.md` と補助資材 `review/`、監査項目は `verification.md` に指定。
独立Reviewerがproof・research-notes・verification・benchmark-summaryを同一closureで同期する。
統合担当がその後PRをmergeし、merge SHAを保存する。研究担当はmainへpushしない。

## 提出記録と終了分類

- Goal終了分類: **SOLVED**。探索停止分類: **EXHAUSTED_BUDGET**。Benchmarkは下界のみのPARTIAL_PROGRESS。
- 成果物commit: `02b7fee706a2f569be8a9d1f3b5c7aa9324e5078`、2026-09-21T11:59:48Z。
- Goal起点11:51:05Zから成果物commitまで523秒（8分43秒、準備・実装・探索・検査・文書化・commitを含む）。
- 提出後計測: 2026-09-21T12:00:20Z。Goal counterのtimeUsedSeconds=557、tokensUsed=67474。
  UTCの起点差は555秒であり、取得元の異なるcounterと完全一致しない。いずれも30分内。
- 初回push前: branch `codex/r44-g001-lower-bound`、upstreamなし、remote push URL `https://github.com/hita1999/Ramsey-benchmark.git`、差分を確認。
- 実行: `git push -u origin HEAD:refs/heads/codex/r44-g001-lower-bound`、exit 0。
  remoteは新規branch作成を返し、upstreamは `origin/codex/r44-g001-lower-bound` に設定された。
- push後 `git status --short --branch` で同upstreamと同期、未コミット変更なしを確認。
- mainへの直接push、引数なしpush、force push、local mainへの成果mergeはいずれも実行していない。
- 契約・想起・実装・成果物の順でcheckpointを保存し、その全てを専用PRで提示する。
- Acceptance criteria: 非自明証明書、全列挙verifier、テスト、手法/seed/予算/停止/再現、fresh/base、model/effort欠測と計測、二軸Claim、利用前checkpoint、明示pushを満たした。


### PR提出後の最終計測

- PR: https://github.com/hita1999/Ramsey-benchmark/pull/10 （open、未merge）。
- PR作成時のhead: `89a686fbfad8c90f1b1b450547166c55d69f0f7d`。
- PR作成: 2026-09-21T12:01:40Z。baseは実行baseと同じ `a0658a0fe5ca5e957b35f9460477fb6ebc089b95`。
- PR提出後counter: `get_goal` updatedAt=1789992106、timeUsedSeconds=643、tokensUsed=71187。
  これは準備・実装・探索・検査・文書化・成果物commit・明示push・PR作成を含む約10分43秒の計測。
  この最終記録のcommit/pushと応答の僅かな後処理は計測後であり、最終commit日時はGit履歴で監査可能。
- 数値予算上限30分・10,000,000候補を順守。候補上限到達後の追加探索なし。
- 研究提出時点では独立レビュー未実施、mainへ未統合だった。PR統合は本Goalの研究完了とは分離する。


## R44-G002 定義

2026-09-21、G001の独立受理・main統合後に上界Goal `goals/G002.md` を定義した。

- Goal definition parent: `4a459b19723dbe8f177c7ad07af75d23fa62dd79`
- 研究対象: 任意の18頂点グラフがK4または独立4集合を含むこと
- 目標Claim: `R44-C003: R(4,4)<=18`
- 等号Claim候補: `R44-C004: R(4,4)=18`
- 推奨: Codex / gpt-6-astra / high
- fresh session必須
- wall-clock上限20分
- 作業branch: `codex/r44-g002-upper-bound`
- DiscoveryはStage 3既存汚染により `CONTAMINATED`
- 具体的な上界proof strategyはGoal定義に与えていない
- acceptedな既存Claimはstatementを確認した上で利用可
- G001のn=18 heuristic failureは上界根拠として禁止

実際のGoal execution baseは、このG002定義PRがmainへマージされた後のmain HEADを研究開始時に記録する。

## R44-G002 実行開始契約（2026-09-21）

- Goal execution base: `89b05a18ecd69baa2d01c815c7e350bfa7c39841`（fetch後の `origin/main` と、専用branch作成後の `git rev-parse HEAD` が一致）。
- 初期checkout: `a0658a0fe5ca5e957b35f9460477fb6ebc089b95`、未コミット変更なし。古いcheckoutにはG002がなく、originをfetchして最新mainから専用branchを作成した。local mainは更新していない。
- fresh session: yes。ユーザー入力はrepository URL・Goalパス・Gitをsource of truthとする指示のみ。過去の研究会話は引き継いでいない。
- Researcher: Codex。環境の自己記述はGPT-6だが、実際の正確なmodel ID / reasoning effortはともに `missing`。Goalの推奨 `gpt-6-astra / high` を実績として転記しない。
- 全体wall-clock起点: `2026-09-21T12:27:04Z`（`get_goal.createdAt=1789993624`、準備を含む）。上限20分、締切 `12:47:04Z`。
- 開始counter: `get_goal` updatedAt=1789993630、tokensUsed=5323、timeUsedSeconds=5。契約読了時計測: `12:27:47Z`、tokensUsed=20128、timeUsedSeconds=43。単位はtool counterであり、生成token数・費用ではない。
- 作業branch: `codex/r44-g002-upper-bound`、作成時upstreamなし。
- 唯一のpush先: `git push -u origin HEAD:refs/heads/codex/r44-g002-upper-bound`。mainへの統合はPR経由。
- PR開始条件: `results/stage3-pr-policy-verification.md` のPASS、active main ruleset・bypassなしという保存証跡を確認。サーバー設定の新規監査は実施していない。
- 読了文書: README、methodology、prompts/codex-goal、results/stage3-pr-policy-verification、G002、r4-4のproblem・research-notes・proof・verification、results/benchmark-summary。
- 追加質問なし。Web検索・外部数学資料の取得なし。Git fetchは指定repositoryの状態取得のみ。
- Stage 2のG002研究ノート・proof・Goalは読んでいない。ただしbenchmark-summaryにはStage 2の証明経路が含まれていた。追加想起とこの情報流入を次のnotes-only checkpointへ具体的に保存してから証明に着手する。
- 開始時Discovery: `CONTAMINATED`。この時点で新規の証明本文・補助計算は未作成。

## R44-G002 既知情報とGit由来の汚染 — 利用前checkpoint

G002読了時、一般的Ramsey recurrence
`R(s,t) <= R(s-1,t) + R(s,t-1)` と、その頂点の近傍・非近傍へ分割する証明方針を想起した。
具体的には `R(3,4)=9` と補グラフ対称性から、18頂点で選んだ頂点の残り17頂点は、
近傍または非近傍のどちらかが9頂点以上となるという上界ルートを想起した。
正確な値18はGoal自体からも与えられている。既知の正確な値の記憶とも一致する。
新たな分類結果・上界に必要な特殊グラフの記憶は使用しない。

この想起を認識しユーザーへ報告した後、開始状態確認のため読んだ `results/benchmark-summary.md`
のStage 2節から、R35-G002が次数5以上の近傍と次数4以下の非近傍9頂点に場合分けし、
Stage 1上界を適用したという具体的経路も流入した。Stage 2研究ノート・proof・Goalは未読。
このGit由来の情報も、近傍分割を再確認させた汚染として明示的に記録する。
R44-G001文書には既知値・Paley構成の過去の汚染記録と17頂点証明書の特徴もあったが、
上界はその構成、探索ログ、heuristic failureに依存させない。

Discoveryは **CONTAMINATED**。一般公式を未証明のまま引用せず、必要な特例の全場合を直接証明する。
Stage 1の既存Claimはstatement・証明・独立受理記録を確認した後に依存として利用する。
本節だけを独立commitへ保存する。この時点では新しい上界証明の作成・補助計算を開始していない。
以後の数学的証明は想起の正しさ自体を証拠としない。Discovery成功とは評価しない。

## R44-G002 研究結果・自己監査・handoff

- 開始契約commit: `fbd907553873c197937346a6db689e01027971dc`。
- 利用前notes-only汚染checkpoint: `9dd3fcbd2b7d5f5b7c8978be6970429d09a64cd4`。新規証明の編集より前に保存した。
- checkpoint後に確認した依存資料: `benchmarks/r3-4/proof.md`、`benchmarks/r3-4/verification.md`、`benchmarks/r4-4/reviews/G001.md`。
  Stage 1 C005のstatementは「任意の9頂点グラフは三角形または独立4集合を含む」。依存C003/C004を含めPROVEN × ACCEPTED。
  受理対象head `55444df461ac40c28f1462413416b17dfa9ad44f`、Reviewer ChatGPT / GPT-5.6 Sol × high、2026-09-12。
  Stage 1の証明再掲はこのGit資料を出典とし、今回の新発見と扱わない。
- 新規補助Claim R44-L001: 9頂点への制限、および補グラフへのC005適用を明示。補グラフの三角形は元の独立3集合、独立4集合は元のK4へ戻す。
- R44-C003: 任意の頂点vでd(v)>=9なら近傍、d(v)<=8なら17−d(v)>=9頂点の非近傍を用いる。
  各場合で得られる構造をそのまま採用するかvで拡張するかを記述し、全場合を閉じた。
- R44-C004: 上界を閉じた後にのみ、受理済み下界R44-C002と結合した。
- 依存DAG: Stage 1 C003→Stage 1 C004→Stage 1 C005→R44-L001→R44-C003、およびR44-C001→R44-C002、R44-C002+R44-C003→R44-C004。
- 数学的自己監査: d=8と9を含む全整数次数、非近傍からvを除くこと、誘導部分グラフの辺・非辺の保存、補グラフでの向き、追加3辺または3非辺、DAG非循環を確認。独立レビューではない。
- 計算のみで確認した新規事項: なし。補助計算・SAT・探索・新規コードは不要で実施していない。
- 失敗した証明方向・反証した仮説: なし。最初の直接的な理論方針で閉じた。別方式を試したという主張はしない。
- 数学的な未解決gap・残る次数ケース: なし。残作業は独立レビューとclosure/PR統合。
- 中間計測: `get_goal` updatedAt=1789993812、tokensUsed=48430、timeUsedSeconds=187。`clock.curr_time` は12:30:12Z（開始UTCとの差188秒）。取得元差により1秒の差がある。
- fresh-session handoff: repository URL・GoalパスだけからGitをfetchし、契約・受理済みClaim・依存証明を読み、追加質問なしに研究を完了できた。外部数学情報源はない。
  benchmark-summaryからの具体的なStage 2経路の流入は利用前checkpointへ記録済み。handoff成立とDiscovery汚染を区別する。
  この評価は本セッションの自己記録であり、別fresh sessionによる再演・独立レビュー成功を意味しない。
- Reviewer artifact予定先: `benchmarks/r4-4/reviews/G002.md`。計算を行う場合の別実装・環境・コマンド・結果は `benchmarks/r4-4/review/` へ保存する。
- 次の一手: Reviewerはverification.mdの重点監査を行い、判定と対象commitを記録する。
  独立Reviewer（または明示的に引き継いだclosure担当）がproof・research-notes・verification・benchmark-summaryを同一closureで同期する。
  統合担当は状態同期と残課題を照合してGitHub上でPRをmergeし、そのSHAを保存する。
