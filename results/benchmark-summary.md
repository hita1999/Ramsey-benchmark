# Ramsey Benchmark — サマリー

このファイルではbenchmark単位の結果を管理する。対応するbenchmark成果物と検証記録がGit上に存在するまでは、確定結果をここへ記録しない。

| Benchmark | 状態 | 下界 | 上界 | 検証 | Goal | 備考 |
|---|---|---:|---:|---|---:|---|
| R(3,4) | SOLVED | ≥9 | ≤9 | C001〜C006 独立レビュー ACCEPTED | 完了2件 | R(3,4)=9独立検証済み、Discoveryは両GoalともCONTAMINATED |
| R(3,5) | SOLVED | ≥14 | ≤14 | R35-C001〜C004 PROVEN × ACCEPTED | 完了2件 | R(3,5)=14独立検証済み、Discovery CONTAMINATED |
| R(4,4) | SOLVED | ≥18 | ≤18 | R44-C001/C002/L001/C003/C004 PROVEN × ACCEPTED | 完了2件 | R(4,4)=18独立検証済み、Discovery CONTAMINATED |
| R(4,5) | PARTIAL_PROGRESS | ≥24 | — | R45-C001 PROVEN × ACCEPTED | H001-A PASS / H001-B SOLVED（独立受理済み） | cross-session handoff PASS × ACCEPTED、H001全体はoperationally SOLVED、Discovery CONTAMINATED |

## 収集する指標

各Goal完了時に、可能な範囲で次を記録する。

- 使用モデル
- reasoning effort
- wall-clock time
- token消費量またはその代替指標
- 研究結果の分類
- 追加・反証されたClaim
- review結果
- 必要となった修正回数
- fresh sessionがGitだけから研究を再開できたか

主要なprocess KPIは、Claim数そのものではなく、Gitに永続化され独立検証を通過した研究進捗とする。

## Stage 1 retrospective

[評価・根拠・改善事項](stage1-retrospective.md)を参照。数学的課題と研究・Git・独立レビューの実施は成功。未知問題でのDiscovery能力、モデル間の効率差、会話履歴なしの再開能力は未評価。

## Stage 2

R35-G001をfresh sessionから実施し、500万候補・探索約120.57秒で13頂点26辺の証明書を保存した。
研究側verifierは全286個の3集合・1287個の5集合を検査した。独立Reviewerは別実装で、全頂点次数4、各辺の両端の共通近傍0、独立数4を確認した。
従って `R(3,5) ≥ 14` は `PROVEN × ACCEPTED`。
G001の探索停止は候補数予算切れ、Goal分類は `SOLVED`。その時点では上界・正確な値は未確定だった。
成果物は `7a84bf9` 以降、独立レビュー資材は `review/` 配下。詳細は [研究ノート](../benchmarks/r3-5/research-notes.md) と [検証記録](../benchmarks/r3-5/verification.md)。

既知値・構成の想起を探索前の独立checkpoint `d74bedc` に記録したため、Discoveryは `CONTAMINATED`。
fresh sessionからGitだけでGoalを取得して研究開始できたことは確認済み。一方、別fresh sessionでの5,000,000候補探索全体の再実行は未実施。
G001の実際のモデルの正確なID・reasoning effortは環境から確認できず欠測とし、推奨設定で実行したとは断定しない。

R35-G002では、任意の14頂点の三角形なしグラフについて、次数5以上なら近傍から独立5集合を取り、
次数4以下なら非近傍の9頂点にStage 1の上界補題を適用する自足的証明を保存した。
`R35-C003: R(3,5)≤14` と `R35-C004: R(3,5)=14` は **`PROVEN × ACCEPTED`**。
2026-09-12にChatGPT / GPT-5.6 Solが上界・等号とG002の `SOLVED` を独立に受理した。
根拠は [G002独立レビュー記録](../benchmarks/r3-5/reviews/G002.md)（PR #5、commit `752dd54`）。
2026-09-21に4文書のレビュー状態を同期し、数学的結果の独立レビューまで完了した。
補助計算は不要だった。一般的なRamsey漸化式等の想起を証明作成前の独立checkpoint `00b886b` に記録し、
Discoveryは引き続き `CONTAMINATED` とした。
実行設定は **GPT-6 Astra / High（ユーザー申告）**。環境による独立確認は欠測。
fresh sessionからGitのみで研究を開始・完了したことを研究側で記録した。
20分予算・計測値・対象commit・Reviewerへの引継ぎは研究ノートを参照。

### Stage 2 retrospective

[評価・事故復旧・Stage 3への引継ぎ](stage2-retrospective.md) に詳細を保存した。
G001/G002の完了時計測は562秒・81,995カウンタ単位／367秒・60,968カウンタ単位。
fresh-sessionの研究開始handoffは機能した一方、mainへの直接push事故とレビュー後の同期漏れが発生した。
revert→PR #5で成果を復旧し、closure PR #6（`a5b161e`）で4文書の同期まで統合済み。
独立計算コードは保存されたが、今回のPython 3.9.6での再実行は `int.bit_count` で失敗し、Reviewer環境の記録不足が残る。
Stage 2 retrospective当時はサーバー設定未確認だった。その後、Stage 3開始前に[PR必須設定の確認](stage3-pr-policy-verification.md)を保存した。

## Stage 3 initialization

Stage 3 rootは `ab5624e9c411afe50137875811c26b46ecf13551`。PR必須rulesetのread-only検証を保存済み。
`benchmarks/r4-4/` を初期化し、最初のGoal `R44-G001` を定義した。

G001は正確な既知値を目標として与えず、固定予算内で `K_4` も独立4集合も持たない証明書を構成する。
研究はfresh Codex sessionで開始し、実際のGoal execution base・model/effort・Discovery・予算を開始前に記録する。

## Stage 3 — R44-G001研究成果

fresh sessionでbase `a0658a0fe5ca5e957b35f9460477fb6ebc089b95` から実行した。
17頂点68辺の証明書を構成し、全2,380個の4集合を検査してK4=0・独立4集合=0を確認。
従って下界 **R(4,4)>=18** は **PROVEN × ACCEPTED**。独立Reviewerが研究側と別のbitmask実装で全2,380個の4集合を再検査した。
G001終了時点ではBenchmark全体は下界のみで `PARTIAL_PROGRESS` だった。現在の上界・等号は末尾のG002成果参照。

探索はn=4から順に増やすseed固定の焼きなましで、1,000万候補・124.310935125秒で候補予算終了。
n=18での探索不成功は不存在証明に使わない。全14証明書・verifier・7テスト・再現資材を保存した。
既知内容想起の利用前checkpointは `8ca54fd`、Discoveryは `CONTAMINATED`。
正確なmodel/effortは `missing`。Gitだけからのfresh-session開始を実施したが、別セッションでの全探索再実行は未実施。
Goal終了分類・PR提出記録・全体時間・counterは [研究ノート](../benchmarks/r4-4/research-notes.md) と `goal-measurements.json` を参照。
独立レビューは2026-09-21に完了し、PR #10はmerge `4a459b1` でmainへ統合済み。

G001は `SOLVED` として [PR #10](https://github.com/hita1999/Ramsey-benchmark/pull/10) に提出済み。
成果物commitまで523秒、PR提出後counterは643秒・71,187単位（生成token数・課金量ではない）。
専用branchへの明示pushとPR-only統合を完了。レビュー記録は `benchmarks/r4-4/reviews/G001.md`、R44-C001/C002は `PROVEN × ACCEPTED`。

## Stage 3 — R44-G002定義

G001統合後、上界Goal `benchmarks/r4-4/goals/G002.md` を定義した。
G002は任意の18頂点グラフにK4または独立4集合が存在することを自足的に証明し、`R(4,4)<=18` を確立することを目的とする。

具体的な証明ルートはGoalへ与えていない。Git上で既に `PROVEN × ACCEPTED` のClaimは利用可能だが、未確定の一般公式・補題はGoal内で証明する必要がある。
G001の18頂点heuristic探索失敗は上界の根拠として使用禁止。fresh Codex session、20分予算、専用branch/PR運用で実施する。

## Stage 3 — R44-G002研究成果

base `89b05a18ecd69baa2d01c815c7e350bfa7c39841` からfresh sessionで実行し、研究を **SOLVED** とした。
任意の18頂点グラフで選んだ頂点の近傍か非近傍が9頂点以上になることから、
受理済みStage 1 C005とその補グラフでの向きを適用し、上界 **R(4,4)<=18** を理論的に証明した。
独立受理済み下界との結合により **R(4,4)=18**。
R44-L001/C003/C004は独立レビューにより **PROVEN × ACCEPTED**。下界R44-C001/C002も **PROVEN × ACCEPTED**。従って **R(4,4)=18** を独立受理した。

補助計算なし。一般再帰式・近傍分割の想起とGit summary経由のStage 2証明経路の流入を、
利用前checkpoint `9dd3fcbd2b7d5f5b7c8978be6970429d09a64cd4` に保存した。Discoveryは **CONTAMINATED**。
正確なmodel ID/effortは `missing`。20分予算、fresh-session評価、counter、成果commit、明示pushとPRの記録は
[研究ノート](../benchmarks/r4-4/research-notes.md)を参照。
独立レビューと4文書のclosure同期は2026-09-21に完了。
[PR #12](https://github.com/hita1999/Ramsey-benchmark/pull/12)も同日12:43:02Zにmerge `17aece27b5d16331ac2e8a067fb930b1694bdc62` でmainへ統合済み。数学的な未解決gapはない。

### Stage 3 retrospective

[評価・再現確認・次実験への引継ぎ](stage3-retrospective.md)に保存した。
両GoalはSOLVED、全ClaimはPROVEN × ACCEPTED、DiscoveryはCONTAMINATED。
PR-only運用とレビュー時の4文書同期は機能し、保存した両verifierと既存7テストの再実行も成功した。
異環境のReviewer結果は数学的全フィールドが一致し、Python/OSメタデータのみ異なる。
Git保存のPR提出後snapshot合計は1,041秒・148,071counter単位であり、全運用工数・生成token数・費用ではない。
本格的な構造分類、長時間checkpointからの再開、未知問題へのDiscovery、単一セッションに対する優越性は未評価。

## Stage 4 — checkpoint-resume experiment

Stage 4 rootは `63e8067f72b607fdc38c533e39b29e9b135cadf5`。対象workloadは `R(4,5)` の下界certificate探索だが、一次KPIは数学的な正確値ではなく **未完了checkpointを別fresh sessionへGitだけで引き継げるか** とする。

H001-Aはresearch candidate interval `[0,2,000,000)` だけを実行して必ず停止し、portableなcheckpoint・handoff manifest・split/resume equivalence testを保存する。H001-BはAのcheckpoint PRがmainへmergeされた後、別fresh sessionで `[2,000,000,10,000,000)` をexact resumeする。

成功条件には、最初の再開candidate indexが2,000,000であること、Phase A候補の重複が0であること、code/config/checkpoint integrity、追加のsemantic user instruction不要、分割実行と連続実行の状態同値性を含む。数学的certificateの発見は副次成果として通常のClaim状態で扱う。

### H001-A checkpoint outcome and independent review (historical submission state)

H001-Aは execution base `6031a203863a71cae5a34793c5d87dbc9b24479b` からfresh sessionで実行し、research interval `[0,2,000,000)` を正確に消費して **PARTIAL_PROGRESS / MANDATORY_HANDOFF_CHECKPOINT** で停止した。next candidate indexは2,000,000、残りは `[2,000,000,10,000,000)`。Phase Bは未実行。

検索はn=5からn=23まで回避グラフを保存した。最強の23頂点114辺certificateは全8,855個の4集合と33,649個の5集合について、K4=0・独立5集合=0を独立Reviewerが別実装で再確認した。従って **R45-C001: R(4,5)>=24 = PROVEN × ACCEPTED**。Discoveryは **CONTAMINATED**。

checkpoint raw SHA-256は `fd295fd8595c2eff2e4800f2862e7bc61ca54d72c3d7c421a61688f26e43b3a3`。current target n=24、current score 40、best score 4であり、score 4はcertificateでも不存在証明でもない。small split/resume testsとcheckpoint mechanismはPhase A acceptanceとしてPASSしたが、実際の別fresh sessionによるcross-session handoffは未評価であり、H001全体は **PARTIAL_PROGRESS** のまま。

PR #15の統合ではcheckpointが参照する immutable `code_commit=5cabb7e2ea0f9ccbd237674666031d7d9f67ae3c` を履歴に保持する必要があるため、**squash/rebaseではなく通常のmerge commitを使用する**。merge後にintegration receiptをPR経由で保存し、その後H001-Bを別fresh sessionで開始する。

### H001-B fresh-session continuation

Phase A PR #15はnormal merge `5f061f2` で統合され、receiptもPR #16経由で統合済み。H001-Bは最新main `e1299901c3533ce1f6843c425ff8c458b834facc` から別fresh sessionでGitだけを使って再構築した。上記H001-A節の未実行・統合待ちは当時の履歴であり、現在はこの節を参照。

H001-Bは **SOLVED（独立受理済み）**、operational handoff **PASS × ACCEPTED**。H001全体のcheckpoint-resume実験は **operationally SOLVED / PASS accepted**。最初の候補2,000,000と全入力状態の一致を直接記録し、残り8,000,000候補を実行して最終index 10,000,000に到達した。連結区間 [0,10,000,000)、重複・欠落0、追加質問0、曖昧/欠測semantic field 0、code/config変更0。小規模split/resumeテストは全状態一致でPASS。2026-09-22にChatGPT / GPT-5.6 Sol（High）が独立レビューで受理した。根拠は [H001-B独立レビュー記録](../benchmarks/r4-5/reviews/H001-B.md)（レビュー対象head `7a2330f5df9498f168cba32275c2ececf7c66805`）。Phase B PR #17の統合は未完了。

初回候補まで310.815747秒、探索と最終保存/検証107.658952708秒。別枠test/replayは556候補、delta比較11,136件。Phase Aの研究軌跡や10M連続実行全体は再計算していない。model/effort欠測、Discovery CONTAMINATED。新規certificateはなく、n=23/114辺の受理済み下界 **R45-C001: R(4,5)>=24, PROVEN × ACCEPTED** を維持。n=24の最良score 4は上界・不存在証明ではない。

実行時の根拠と計測は [H001-B再現・引継ぎ文書](../benchmarks/r4-5/h001-b/reproduce.md) と `benchmarks/r4-5/h001-b/submission-record.json`、現在の受理状態と統合要件は [H001-B独立レビュー記録](../benchmarks/r4-5/reviews/H001-B.md) を参照。実行時artifactのUNREVIEWEDは提出時点の履歴として保持する。R(4,5)数学的workloadの状態は引き続き **PARTIAL_PROGRESS** であり、operational Goal完了とは区別する。

残作業はPR #17の **normal merge commit** による統合と、統合担当によるPR経由の `results/r45-h001-b-integration-receipt.md` 保存。final checkpointが参照する `code_commit=d1c5cdf7...` とhistorical bytesの監査を維持するため、squash/rebaseは使用しない。receiptにはmerge SHA/日時、同commitの到達可能性、final checkpoint SHA、受理済みoperational verdictを記録する。
