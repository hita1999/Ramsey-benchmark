# Stage 3 retrospective — R(4,4)

## 結論

Stage 3はG001/G002の2 Goalで **R(4,4)=18** に到達し、R44-C001/C002/L001/C003/C004の
**PROVEN × ACCEPTED**、レビュー時の4文書同期、PR経由のmain統合まで完了した。
Stage 2の直接push事故とClaimレビュー状態の同期漏れは、今回の履歴には再発していない。
保存済みの研究側・Reviewer側verifierは今回ともに再実行できた。

一方、両GoalのDiscoveryは **CONTAMINATED**。上界は受理済みStage 1補題の短い応用で閉じ、
Stage 3で予定した本格的な構造分類、長時間の停滞・中断復帰、未知問題への発見能力は検証できなかった。
3段階で確認できたのは、既知の小規模問題について研究・Git・別担当レビューを接続する運用である。
単一セッションより効率・信頼性が高いという中心仮説には、比較対象と同条件の計測がまだない。

今後は単に問題サイズを増やすより、未評価の能力を測る境界付き実験を設計する。
本書ではその設計条件までを引き継ぎ、新しい数学Goalは作成・実行しない。

## 評価対象と根拠

- 評価日: 2026-09-22（Asia/Tokyo）。担当: Codex、R44-G002と同じタスクでの継続作業。
- 基準commit: `17aece27b5d16331ac2e8a067fb930b1694bdc62`（PR #12マージ後）。
- 初期checkout: `daabf7b3c16458aad282a507db120ad8ea51eca1`。fetchで独立レビューとmain統合を取得し、
  `codex/stage3-retrospective` を最新origin/mainからupstreamなしで作成した。
- source of truth: Git。会話にだけ残る最終counterや設定は、過去のGit計測の欠測補完に使わない。
- 本書はプロセス監査と保存コードの再現確認であり、新たな独立数学レビュー・fresh-session研究実験ではない。

主要根拠は [研究ノート](../benchmarks/r4-4/research-notes.md)、[証明](../benchmarks/r4-4/proof.md)、
[検証記録](../benchmarks/r4-4/verification.md)、[G001レビュー](../benchmarks/r4-4/reviews/G001.md)、
[G002レビュー](../benchmarks/r4-4/reviews/G002.md)、
[G001計測](../benchmarks/r4-4/goal-measurements.json)、[探索ログ](../benchmarks/r4-4/run/search-result.json)。

| 工程 | 記録commit | PR / merge |
|---|---|---|
| PR必須化の事前確認 | `b163b68` | [#8](https://github.com/hita1999/Ramsey-benchmark/pull/8) / `ab5624e` |
| Stage 3・G001初期化 | `40da372` | [#9](https://github.com/hita1999/Ramsey-benchmark/pull/9) / `a0658a0` |
| G001研究→レビュー・closure | 成果 `02b7fee`、提出記録 `1028ee0`、review `c67a0e8` | [#10](https://github.com/hita1999/Ramsey-benchmark/pull/10) / `4a459b1` |
| G002定義 | `7ed7a68` | [#11](https://github.com/hita1999/Ramsey-benchmark/pull/11) / `89b05a1` |
| G002研究→レビュー・closure | 成果 `1265d2f`、提出記録 `daabf7b`、review `ab97b7e` | [#12](https://github.com/hita1999/Ramsey-benchmark/pull/12) / `17aece2` |

## G001/G002の時間・counter・成果

| 指標 | R44-G001 | R44-G002 |
|---|---|---|
| 実行base | `a0658a0` | `89b05a1` |
| Researcher model ID / effort | missing / missing | missing / missing |
| 推奨設定 | gpt-6-astra / high（実績とは別） | gpt-6-astra / high（実績とは別） |
| 予算 | 全体30分・10,000,000候補、探索内部上限600秒 | 全体20分 |
| Goal開始UTC | 2026-09-21 11:51:05 | 2026-09-21 12:27:04 |
| 数学成果commitまでのUTC差 | 523秒（8分43秒） | 350秒（5分50秒） |
| Gitに保存された最後のGoal counter | PR提出後643秒（10分43秒） | PR提出後398秒（6分38秒） |
| 同時点のtoken counter | 71,187 | 76,884 |
| 純粋な探索 | 124.310935125秒・10,000,000候補 | なし |
| 成果 | 17頂点68辺、下界≥18 | 理論上界≤18、等号18 |
| Goal / 探索の停止 | SOLVED / EXHAUSTED_BUDGET | SOLVED / 探索なし |
| 独立Reviewer | ChatGPT / GPT-5.6 Sol / High | ChatGPT / GPT-5.6 Sol / High |
| 数学的修正要求 | 保存レビューに記録なし | 保存レビューに記録なし |

時間・tokenの最後の値は `get_goal` のPR提出後snapshotであり、`update_goal(complete)` の最終値ではない。
最後の記録commit・push・応答、独立レビュー、closure、本retrospectiveを含まない。
単純合計は **1,041秒（17分21秒）・148,071カウンタ単位**。Stage 3の全運用コストではない。
token counterは新規生成token数・課金量ではない。Reviewerの作業時間・token、設定確認作業の工数は欠測。
G002のsnapshotのUTC差399秒とcounter398秒は取得元が異なる。G001探索ログでもUTC差とmonotonic時間は一致しない。
測定区間・時計の異なる値を同じ指標に補正したり、欠測をcommit間隔から推定したりしない。

G001は17頂点証明書を累積101,602候補・探索開始から約1.034秒で発見した。
残り **9,898,398候補（約98.98%）** は18頂点で費やし、違反数の最良値9で終わった。
これは固定予算契約内の探索であり、失敗から不存在を導いていない。
既知値を知った後で18頂点を探索すべきでなかったと評価すると、情報制約を遡って変えてしまう。
次回の効率改善では、停滞時の再始動・別手法への切替・checkpoint条件を実行前に固定し、既知値に依存させない。

上界はStage 1 C005の9頂点補題を近傍と非近傍へ適用して閉じた。
17頂点証明書の特殊構造が上界の発見を導いたという記録はない。

## Stage 1・2との比較と評価限界

| 評価軸 | Stage 1 | Stage 2 | Stage 3 |
|---|---|---|---|
| Correctness | R(3,4)=9、2 Goal受理 | R(3,5)=14、2 Goal受理 | R(4,4)=18、2 Goal受理 |
| Discovery | 両Goal CONTAMINATED | 両Goal CONTAMINATED | 両Goal CONTAMINATED、Git summaryからの流入も記録 |
| fresh-session | G002は同じ会話 | 両GoalのGitからの研究開始を記録 | 両Goalの開始とReviewerによる記録整合性監査 |
| 再現資材 | 上界Reviewerの補助計算コード欠落 | 下界Reviewerコード保存、手元Pythonで再実行失敗 | Reviewer環境も保存、今回両verifier再実行成功 |
| 状態同期 | 受理後の同期漏れ | 同期漏れ再発、別closure PR | 両レビューcommitで4文書のClaim状態を同期 |
| Git運用 | PRで成果保存 | main直接push事故、revert・PR復旧 | 事前保護確認、対象範囲のmain変更はPR merge |
| 効率の比較可能性 | 全体最終計測に欠測 | 完了時counter合計929秒・142,963単位 | PR提出後snapshot合計1,041秒・148,071単位 |

最後の行は終点、問題、探索予算、モデル設定が揃っていないため、速度・費用の優劣を示さない。
Stage 3はより大きい頂点数を扱ったが、難しい構造分類を必要としなかった。
短い既存補題の応用を閉じたことを、長時間の研究能力の検証へ読み替えない。
また受理後の証明変更はレビュー状態・検証説明の更新であり、数学的な修正要求は両レビューに記録されていない。
誤証明を検出して修正させる能力が測れたという意味ではない。

## Discoveryと入力範囲

| Goal | 内容 | Git上の順序 |
|---|---|---|
| G001 | 既知値18と17頂点Paley構成の想起 | 契約 `fb43335` → 汚染 `8ca54fd` → 実装 `abb6dfd` → 成果 `02b7fee` |
| G002 | 一般Ramsey recurrence、9/8の近傍分割ルートの想起。summary内のStage 2経路も流入 | 契約 `fbd9075` → 汚染 `9dd3fcb` → 成果 `1265d2f` |

利用前checkpointは両Goalで独立commitとなっている。想起の正しさを証拠にせず、証明書の検査や直接証明を用いた。
これは数学的受理の根拠であり、DiscoveryがCLEANだった証拠ではない。
G002はStage 2の研究ノート・proof・Goalを直接読まなくても、横断サマリーから経路を得た。
方針を独立に検討する段階の入力制限は、ファイル名だけでなく要約の内容にも適用する必要がある。

次回は研究開始時の必読集合をGoal・problem・対象benchmarkの必要記録・運用文書に限定し、
全Stageのbenchmark-summaryを最初から必読にしない。
受理済みClaimへの依存確認は、必要になった後に対象statement・証明・reviewを読む手順として残す。
出典と取得時点を記録し、具体的strategyが流入したら引き続き利用前checkpointを作る。
過去の汚染を後から取り消す対応ではない。

## fresh-session handoff

両Goalともrepository URLとGoal pathから開始し、古いcheckoutをfetchして実行baseへ移行したと記録されている。
初期checkoutはG001 `e546714`、G002 `a0658a0`。追加ユーザー質問・外部数学情報取得は0件という記録である。
Reviewerは両方について保存資料の整合性を監査したが、研究開始セッションを再演したわけではない。

未評価なのは、未完了Goalの途中checkpointからの履歴なし再開、長時間の文脈管理、探索全体の別セッション再実行である。
今回のretrospectiveはG002と同じタスクなので、新しいfresh-session成功例に数えない。

## 保存コードの再現確認

2026-09-22にPython 3.9.6 / macOS 13.7.4 arm64で、研究側verifier、既存7テスト、Reviewer別実装を実行した。
コード・証明書は基準commitのまま。結果は次の通り。

- 研究側: 17頂点68辺、全2,380四頂点集合、K4=0、独立4集合=0、valid=true。
- 既存テスト: 7件成功。保存14証明書、小さい全グラフとの照合、不正入力、探索スコア差分等の既存検査を再実行。
- Reviewer側: 証明書hash一致、数学的全フィールドが保存JSONと一致。各次数8、三角形68、独立3集合68も一致。
- 保存JSONとのバイト一致: **不一致**。相違キーは `python` と `platform` だけ。
  Reviewer当時はPython 3.13.5 / Linuxであり、今回の環境情報をそのまま別の実行結果へ保存した。

[再実行スクリプト](stage3-retrospective/reproduce.py)、[結果・入力hash・実行コマンド](stage3-retrospective/run/report.json)、
[テストログ](stage3-retrospective/run/existing-tests.stderr.txt)、[Reviewer再実行結果](stage3-retrospective/run/reviewer-result.json)を保存した。

```sh
# repository root。出力先はまだ存在しないディレクトリを指定する。
python3 results/stage3-retrospective/reproduce.py --output /tmp/r44-stage3-replay
```

比較は `python` と `platform` だけを事前に除外し、残りの全キーと値を照合する。
元JSON・環境情報・byte_equal=falseも残すため、都合のよい数学フィールドだけを抜き出した比較ではない。
従来のreview手順の単純な `cmp` は環境が違うと失敗する。旧記録は保持し、reproduce.mdにこの注意と手順を追加した。
今回成功したのは保存実装の再実行であり、第三の独立実装の新規検証ではない。
1,000万候補の探索全体は再実行しておらず、その軌跡一致は未確認のまま。
Stage 2で失敗した別コードの再現性も、本結果によって解消したとは扱わない。

## PR運用と状態同期

[事前確認](stage3-pr-policy-verification.md)には、2026-09-21時点でmain rulesetがactive、PR必須、
bypass actorsなし、current user can bypass=neverと記録されている。
今回GitHub側の設定を再取得したわけではなく、当時の開始条件とGit履歴を照合した。
`70ca639..17aece2` のmain first-parentはPR #8〜#12のmerge commitだけであり、
当該範囲でStage 2のような直接成果commitの取り込みは見られない。
履歴と保存された明示push記録の範囲の評価であり、全push試行や現在の保護設定を監査したという主張ではない。

G001の `c67a0e8`、G002の `ab97b7e` は、それぞれreview artifactと同時に4文書のClaim状態を同期した。
`git diff --exit-code ab97b7e 17aece2` は終了コード0で、G002レビュー済みツリーがそのまま統合されている。
この点でStage 2の改善手順は機能した。

ただしマージ後の研究ノートとサマリーには「PR #12統合待ち」が残り、サマリー・methodologyには
古い「Stage 3の保護は現時点で未確認」という記述も残っていた。
これは数学的Claimの同期漏れとは異なる、統合結果・時点の更新漏れである。
本変更でPR #12のmerge SHAと日時を同期し、古い保護状態はStage 2当時の記述として明示した。
将来はレビュー時のclosureと、マージ後にSHAを記録する統合担当の作業を分ける。
後者も次の文書PRへまとめるなどPR経由で保存し、merge直後のmainへ直接追記しない。

## 今回の運用改善と次の実験の条件

| 課題 | 今回の反映 | 次回確認する担当・条件 |
|---|---|---|
| summary経由のstrategy流入 | Goalプロトコルへ入力範囲と依存確認の順序を追記 | Goal設計担当が必読集合を固定、研究担当が流入を記録 |
| 異環境JSON比較 | 数学結果と環境メタデータを分けて比較、raw出力も保存 | Reviewer / 再現確認担当が比較除外キーを事前指定 |
| マージ後の状態・SHA漏れ | 現在地を同期、統合receiptの担当を明記 | 統合担当がmerge SHA・日時・保存先を次のPRへ残す |
| 最終counterのGit保存不足 | 計測終点の区別をGoalプロトコルへ追記 | 終了counterを取得できた担当が追記。取得不能なら最終snapshotと残区間を明記 |
| 汎用reviewテンプレートのK3/K4固定 | R(s,t)の赤K_s / 青K_tに一般化 | Reviewerが各problemの禁止構造とverifierを照合 |
| Stage 3本来の難しい能力が未評価 | 次実験の受理条件を下記へ固定 | 統括担当が境界付きGoalを設計 |

次の実験では、対象問題を決める前に何を測るかを明示する。

1. 受理済みの短い上界補題の直適用だけでは閉じない局所補題・分類・証明書探索を一つ選ぶ。
   未知問題へ進む場合も、正確なRamsey数の決定を無制限のGoalにしない。
2. 数値予算、停滞時の方針変更条件、成功・部分進捗・予算切れの定義を事前に保存する。
   複数手法の比較をするなら入力・seed群・予算を揃え、今回の単発記録を比較実験の代用にしない。
3. 未完了checkpointを意図的に一度作り、別fresh sessionへGitのみで引き継ぐ。
   再開に必要な追加情報、重複探索、未証明仮定の保持、残予算の理解を記録する。
4. Reviewerの反証能力を測る場合は、研究成果とは別の監査用課題で検出対象と採点方法を事前に固定する。
   正しい証明へのACCEPTEDだけを誤り検出率としない。
5. 単一セッションとの比較を行うなら、入力と予算を固定した対照実験を別に設計し、
   研究・レビュー・closureを含む同じ終点で時間とcounterを収集する。

Stage 1〜3の終了と運用改善は次の設計へ進む根拠になる。
未知問題の発見能力、難しい構造分類、モデル間の優劣、複数担当方式の優越性は未評価として引き継ぐ。
