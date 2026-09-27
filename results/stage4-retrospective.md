# Stage 4 retrospective — R(4,5) checkpoint-resume

## 結論

Stage 4は、未完了の探索状態をGitに保存して一度研究を停止し、別fresh sessionで残予算だけを再開する実験を完了した。
**H001-B = SOLVED、operational handoff = PASS × ACCEPTED、H001全体 = operationally SOLVED**。
Phase Aの2,000,000候補とPhase Bの8,000,000候補が、重複・欠落なしに `[0,10,000,000)` を構成することが独立受理された。
PR #17とpost-merge receiptのPR #18はともにmainへ統合済みである。

数学的成果は **R45-C001: R(4,5)>=24 = PROVEN × ACCEPTED**。Phase Bの新規証明書・新規数学Claimは0件。
数学的workloadは **PARTIAL_PROGRESS** のままで、n=24の最良score 4は不存在・上界の証明ではない。
一次KPIが数学的改善とは別に設定されていたため、証明書を改善できなくても引継ぎ実験は成功と評価できる。

Stage 3で未評価だった「未完了checkpointから別fresh sessionへの再開」は今回実施できた。
ただし単一の決定的探索・同じ実行環境・意図した停止境界での成功である。
突発停止の復旧、異環境での研究再開、長時間の証明発見、未知問題へのDiscovery、単一セッションに対する効率・信頼性の優越性は未評価。
Discoveryは引き続き **CONTAMINATED**。これらの限界を、正常再開の成功や証明書の正しさと混同しない。

## 評価範囲とGitHubの最新状態

- 評価日: 2026-09-27（Asia/Tokyo）。担当: Codex、H001-Bと同じタスク内の継続作業。本retrospectiveはfresh-session実験や新しい独立レビューではない。
- 初期checkout: `3503f0b03d4e4465a006b0cb6f3c52db19f6602f`。GitHubからfetchした評価base: `2cbdcd4e1f4758c5d4dc4b427bd408db8a526f3b`。
- 専用branch: `codex/stage4-retrospective`。Git内のレビュー・receipt・実測値を根拠とし、会話だけの情報で過去の欠測を補わない。
- GitHub APIからPR #14〜#18のmerge情報とPR #17の最新コメントを取得した。[取得snapshot](stage4-retrospective/github-snapshot.json)には取得UTC・PR本文・対象SHA・コメントを保存した。
- GitHub `merged_at` をmerge日時の取得元とする。Git commitのauthor/committer日時と同一とは仮定しない。

| 工程 | PR | merge commit | GitHub merge日時（UTC） |
|---|---|---|---|
| Stage 4契約 | [#14](https://github.com/hita1999/Ramsey-benchmark/pull/14) | `6031a203` | 2026-09-22 07:46:07 |
| Phase A研究・独立レビュー | [#15](https://github.com/hita1999/Ramsey-benchmark/pull/15) | `5f061f2d` | 2026-09-22 08:33:35 |
| Phase A統合receipt | [#16](https://github.com/hita1999/Ramsey-benchmark/pull/16) | `e1299901` | 2026-09-22 08:44:01 |
| Phase B研究・独立レビュー・同期修正 | [#17](https://github.com/hita1999/Ramsey-benchmark/pull/17) | `fc823302` | 2026-09-26 05:46:48 |
| Phase B統合receipt・closure | [#18](https://github.com/hita1999/Ramsey-benchmark/pull/18) | `2cbdcd4e` | 2026-09-26 06:00:43 |

[Phase Aレビュー](../benchmarks/r4-5/reviews/H001-A.md)、[Phase Bレビュー](../benchmarks/r4-5/reviews/H001-B.md)、
[A統合receipt](r45-h001-a-integration-receipt.md)、[B統合receipt](r45-h001-b-integration-receipt.md)が受理・統合の根拠。
全5 mergeの親SHAがGitHub metadataと一致し、各merge treeはPR head treeと同一だった。
Stage 4 root `63e8067..2cbdcd4` のfirst-parentはこの5件のみ。対象範囲では成果のmain直接取り込みは見られない。
全push試行やGitHubの現在の保護設定を監査したという意味ではなく、2026-09-21の保護設定記録を現在の保証へ読み替えない。

## Handoffの達成内容と根拠

| 条件 | 観測結果・証拠 |
|---|---|
| 意図した未完了停止 | Aは `[0,2000000)` でMANDATORY_HANDOFF_CHECKPOINT。B開始前にPR #15・#16を統合 |
| Gitだけからの再構築 | B実行base `e1299901...`、入力ファイル・hash・追加質問0を起動監査へ保存 |
| 再開前の完全性確認 | A manifest 26成果物、checkpoint/schema、過去のcode/config、状態とcounterの検証がPASS |
| 最初のresearch候補 | `first-candidate.json` がstep entryのindex 2,000,000と全入力状態digestを記録 |
| 連続した残予算の消費 | 80個の100,000候補progress block、最終next index 10,000,000、gap/重複0 |
| 意味の連続性 | search.py・verify.py・configのbytes一致。PRNG・graph・score・restart・iterationを復元 |
| 分割実行同値 | 111+157、1+1、7+1の事前登録テストで全semantic field・canonical bytes一致 |
| 最終成果物 | final checkpoint、best-so-far、19証明書、検証記録、hash manifestを保存 |
| 独立判定と統合 | H001-B PASS × ACCEPTED、通常merge、code commitの到達可能性とreceipt保存 |

Phase Aから引き継いだ状態はn=24、score 40、best score 4、restart 152、iteration 2439。
Phase B終了時はn=24、score 27、best score 4、restart 952、iteration 2439。
完了targetの評価477,561と現targetの9,522,439（952×10,000+2,439）の和は10,000,000。
全体の95.22439%がn=24での探索に費やされたが、Phase Bには手法切替の権限も条件も登録されていなかった。
停滞を見て勝手に戦略変更しなかったことは、このexact-resume契約では遵守事項である。
既知値に照らして探索を止めるべきだったと後から採点基準を変えない。

最初のstep入口を観測するrunpy/profiling launcherは、起動監査とともに研究前commit `d1c5cdf7...` に固定された。
全状態digestを確認し、state/PRNGを変更せずprofilingを解除してからstep本体へ進む。
記録された時刻は「step関数へのentry」であり、score計算の最初の命令の時刻ではない。
重複0の根拠は、この入口、変更のない単調counter遷移、progressと最終状態の整合性である。
別の10M連続軌跡との完全比較や全候補ごとの外部ログを実施したとは主張しない。

Git-only/fresh-sessionは保存されたセッション申告と入力記録に基づく。Gitは状態復元の証拠を保持するが、
隠れた会話が一切なかったことを暗号学的に証明するものではない。この限界は独立レビューにも明記されている。

## 計測・成果・欠測

| 指標 | H001-A | H001-B |
|---|---|---|
| 実行base | `6031a203...` | `e1299901...` |
| 予算 | 全体25分、2,000,000 research候補 | 全体30分、8,000,000 research候補 |
| 実際のmodel ID / effort | missing / missing | missing / missing |
| 推奨model / effort | gpt-6-astra / high（実測ではない） | 同左 |
| 研究区間 | [0,2,000,000) | [2,000,000,10,000,000) |
| 探索＋最終保存・検証 | 46.253464292秒 | 107.658952708秒 |
| 開始→初回resume候補 | 対象外 | 310.815747秒 |
| 研究時の別枠test transitions | 556 | 556 |
| 研究時の別枠delta比較 | 11,136 | 11,136 |
| 新規証明書 | n=5..23、19件 | 0件（19件をそのまま継承） |
| 最後の保存済みsession計測 | phase-stopまでの上限926.957099秒 | Goal完了counter 751秒 |
| token counter | missing | 完了97,618単位 |
| 終了分類 | PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT | operational Goal SOLVED / 固定区間完了 |

出典: [A run](../benchmarks/r4-5/h001-a/run/run-result.json)、[B run](../benchmarks/r4-5/h001-b/run/run-result.json)、
[A提出計測](../benchmarks/r4-5/h001-a/submission-record.json)、[B提出・完了計測](../benchmarks/r4-5/h001-b/submission-record.json)。

Aの開始は分単位の保守的下限07:46:00Zで、最初の正確な時計取得は07:47:25Z。
926.957099秒は08:01:26.957099Zのphase-stop snapshotまでの上限であり、正確な開始からの実測値ではない。
その後の記録commit/pushを含まない。Aのtoken/costをBやcommit数から推定しない。

Bはgoal-serviceの秒単位開始08:45:00Zを用い、成果commit前590秒・81,663単位、PR提出後703秒・95,989単位、
Goal完了751秒・97,618単位を別々に保存した。最終記録pushの確認はPR本文で08:58:03Z（783秒）と報告され、今回のGitHub snapshotにも残る。
751秒には独立レビュー、後日のclosure修正、merge/receipt、本retrospectiveを含めない。
token counterは生成token数・課金量ではない。Reviewer・統合担当の作業時間/tokenと全体費用は欠測。
PR提出からmergeまでの暦時間を人間・AIの作業時間として足さない。

比較可能なrun内の探索＋保存/検証時間の合計は **153.912417秒**、研究候補合計10,000,000。
A/Bのsession時間は始点の精度・終点が異なり、Stage全体の実測総時間として合算しない。
同条件の連続実行や別方式との対照がないので、分割方式の速度・費用優位やresume overheadの純増を算定しない。

## Stage 3の改善が機能した点・再発した点

| Stage 3までの課題 | Stage 4での観測 | 判断 |
|---|---|---|
| 未完了状態からの別session再開が未評価 | Aの意図的停止→merge→別fresh Bで実行 | 登録した一次KPIを達成 |
| merge後のSHA・状態保存漏れ | A/Bともreceiptを別PRで保存、code ancestry維持 | 改善が機能 |
| 最終counterの保存不足 | Bは成果・PR・完了を別記録、Aはtoken欠測 | 一部改善、全体計測は未完 |
| 4文書のレビュー状態同期漏れ | Bの3文書とreviewだけ先に受理、summaryがUNREVIEWEDのまま | 再発。merge前コメントで検出・修正 |
| 横断summary・methodologyからのstrategy流入 | 両Phaseで流入を開示、Bでは探索仕様を変更せず | 利用前記録は機能、CLEAN discoveryではない |
| 異環境の出力比較 | Reviewer出力のpython/platformだけを除外して再現成功 | メタデータと数学出力の分離が有効 |

2026-09-22の[PR #17レビューコメント](https://github.com/hita1999/Ramsey-benchmark/pull/17#pullrequestreview-5277325229)は、
数学・handoff evidenceを受理しつつsummary同期をmerge前のblocking pointとした。
`3503f0b` が同期し、2026-09-26の[再確認コメント](https://github.com/hita1999/Ramsey-benchmark/pull/17#issuecomment-5843596704)で解消を確認した。
誤った数学や不正なcheckpointを発見した事例ではなく、**同じ状態を複数の現在地文書へ反映する工程の漏れ**である。

同コメントはPR本文のUNREVIEWED/pending表示も非blockingとして指摘した。2026-09-27のAPI取得時にも本文は古いままだった。
現在の受理状態はGit内のreviewとreceiptで判断し、古いPR本文をそれより優先しない。
本retrospectiveは旧提出artifactやレビュー原記録を遡って書き換えず、snapshotとして残す。
将来のPRは本文の冒頭を現在地とし、提出時点の状態を時点付き履歴へ分離する。

通常mergeは単なる好みではなく、checkpointのcode_commitを`git show`で検証する設計の前提になっている。
`5cabb7e2...` と `d1c5cdf7...` の両方が最新mainから到達可能で、今回も検証が成功した。
履歴依存を減らす設計を将来採る場合は、先にソースの保存・検証方式とschemaを変更した新Goalで評価する。
既存実験へ後付けでsquash/rebaseを適用しない。

## 保存コードの再現確認

2026-09-27にPython 3.9.6 / macOS 13.7.4 arm64で実施した。
[スクリプト](stage4-retrospective/reproduce.py)は固定baseのGit archiveを一時ディレクトリへ展開し、
書き込みを伴うPhase B auditをそこで実行する。元の履歴・成果物を編集しない。
過去のcode bytesの照会だけは元repositoryのGit object databaseへ向ける。

- A manifest 26件、B manifest 36件のhash一致。
- A/B監査はPASS。事前指定の`checked_at_utc`だけを除いた全フィールドが保存出力と一致。
- 既存testは全JSON fieldが一致。追加556 TEST/REPLAY transitions、11,136 delta比較を**今回のretrospective分**として保存。
  当初研究時のA/B合計1,112 test transitions、22,272 delta比較とは別会計で、研究counterは0増分。
- 研究側監査が全19証明書を検査。保存Reviewer実装もn=23・114辺、8,855四集合・33,649五集合、K4=0・独立5集合=0を再確認。
- Reviewer出力は`python`と`platform`のみ異なり、その他全フィールドが一致。raw bytesは不一致のまま記録。
- PR #14〜#18のmerge parents/tree、first-parent範囲、2つのcode commitの到達可能性を照合。

[結果・入力hash・コマンド](stage4-retrospective/run/report.json)と各raw stdout/stderrを保存した。
再現手順（出力先は未作成のディレクトリを指定）:

```sh
python3 results/stage4-retrospective/reproduce.py --output /tmp/r45-stage4-retrospective-recheck
```

これは保存実装の再現確認で、新規の独立実装・独立数学レビューでも、fresh-sessionの再演でもない。
2M/8M/10M research trajectoryの再実行は行っていない。
Phase B auditの出力には当時の自己評価UNREVIEWEDとpendingの文言が残るが、それは凍結した実行時recordの再現であり、
現在の独立受理状態をUNREVIEWEDへ戻すものではない。

## 運用改善と次実験の条件

今回の変更は本書・再現資材・summary現在地と、methodologyおよび両運用プロトコルへの追記に限定する。
過去のGoal契約・探索コード・checkpoint・数学Claim・独立レビュー判定を変更せず、新しい研究も開始しない。

| 改善 | 担当と実施条件 |
|---|---|
| 状態の分離 | Goal設計者が数学Claim×独立レビュー、operational判定×独立レビュー、統合状態を別に定義。運用SOLVEDを数学SOLVEDへ転記しない |
| closureの取りこぼし対策 | Reviewer/closure担当が実際の4文書現在地を一覧照合。統合担当は最新headのdiffとPR本文を確認し、未同期ならmerge前に直す |
| 履歴と現在地の区別 | 実行時JSONは凍結。現在地には最新review/receiptへのリンクを置く。保存audit再実行は別出力先で行う |
| resume証拠の固定 | checkpoint/hash、最初の候補、残予算、全semantic state、observer有無を研究前に記録。code/config修復は新version/Goalへ分離 |
| 測定の揃え方 | 研究・test・再現検算を別counterにし、Phase開始・停止・完了・後処理・review/closureを区別。欠測を推定で埋めない |

次に測るなら、**障害を含むhandoff**を優先候補とする。正常再開は1例確認できたため、
安全に止まる能力と意図した境界以外の復旧を別の境界付きGoalで評価する意義がある。
これは次Goalの提案で、Stage 5や追加探索の実行指示ではない。

1. 正常checkpoint、hash不一致、欠落semantic field、到達不能code履歴などの入力条件と期待判定を事前登録する。
   不正入力では最初のresearch評価前に停止できるか、追加質問・重複・必要な修復を測る。
   既存tamper単体テストはあるが、それだけでfresh-session全体の障害対応を測れたとはしない。
2. 突発停止も評価する場合は、永続checkpoint頻度・atomic write・復旧点・再評価をresearch/replayのどちらに数えるかを先に固定する。
   現行searchはprogressを100kごとに書くが、live checkpointはloop終了後に保存する。途中progressは再開可能checkpointの代用にならない。
   現行resume CLIはAの2M境界専用で、任意の中断点からの復旧を実装・評価したものではない。
3. 異環境移行を測るならPython/OS等を計画的に変え、整数semantic state全体の一致とメタデータ差を別に記録する。
   今回Reviewer検算の環境差を、探索resumeの異環境成功へ読み替えない。
4. 効率比較を行う場合は同じcode/config/seed群・research予算で単一sessionと分割sessionを比較し、
   起動・監査・レビュー・closureを含む同じ終点で測る。1件の成功率や処理速度から一般化しない。
5. 未知数学の発見・長い証明の引継ぎを測る場合は、未証明仮定・依存Claim・失敗方針の保持を別の採点対象にする。
   今回は既に固定された有限状態機械の再開であり、証明方針の創造や変更を伴う引継ぎではない。

Stage 4はGitを介した意図的checkpoint-resumeの実行可能性を示した。
中心仮説である複数担当方式の優越性を結論するには、引き続き対照条件と揃った計測が必要である。
