# R(4,4) — 研究ノート

## 現在の状態

- Benchmark: `PARTIAL_PROGRESS`（下界のみ、上界・正確な値は未証明）。
- R44-G001: **SOLVED**。独立レビュー受理済み。PR #10でmainへ統合済み（merge `4a459b19723dbe8f177c7ad07af75d23fa62dd79`）。
- 今回の最大証明書: 17頂点68辺。n=4..17の全14証明書を保存。
- `R44-C001` / `R44-C002`: **PROVEN × ACCEPTED**。
- Discovery: **CONTAMINATED**。利用前checkpoint `8ca54fd7a4dbc751da870e658d5967185e90dfb2`。
- 探索停止: `EXHAUSTED_BUDGET`（10,000,000候補、124.310935125秒）。
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

Discoveryは両ClaimともCONTAMINATED。証明書hashはproof.mdに固定。

## 現在のフロンティア

G001の独立レビューとmain統合は完了し、R44-C001/C002は `PROVEN × ACCEPTED`。
次の研究Goalは `R44-G002`。任意の18頂点グラフにK4または独立4集合があることを自足的に証明し、`R(4,4)<=18` を狙う。
G002の証明ルートはGoalに埋め込まず、G001の18頂点探索失敗は上界・不存在・最大性の根拠にしない。


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
