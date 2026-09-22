# Ramsey Benchmark — サマリー

このファイルではbenchmark単位の結果を管理する。対応するbenchmark成果物と検証記録がGit上に存在するまでは、確定結果をここへ記録しない。

| Benchmark | 状態 | 下界 | 上界 | 検証 | Goal | 備考 |
|---|---|---:|---:|---|---:|---|
| R(3,4) | SOLVED | ≥9 | ≤9 | C001〜C006 独立レビュー ACCEPTED | 完了2件 | R(3,4)=9独立検証済み、Discoveryは両GoalともCONTAMINATED |
| R(3,5) | SOLVED | ≥14 | ≤14 | R35-C001〜C004 PROVEN × ACCEPTED | 完了2件 | R(3,5)=14独立検証済み、Discovery CONTAMINATED |
| R(4,4) | SOLVED | ≥18 | ≤18 | R44-C001/C002/L001/C003/C004 PROVEN × ACCEPTED | 完了2件 | R(4,4)=18独立検証済み、Discovery CONTAMINATED |
| R(4,5) | HANDOFF_EXPERIMENT_READY | — | — | — | H001-A/B定義済み | Stage 4: 未完了checkpoint→別fresh session再開を一次KPIにする |

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
