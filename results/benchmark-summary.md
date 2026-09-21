# Ramsey Benchmark — サマリー

このファイルではbenchmark単位の結果を管理する。対応するbenchmark成果物と検証記録がGit上に存在するまでは、確定結果をここへ記録しない。

| Benchmark | 状態 | 下界 | 上界 | 検証 | Goal | 備考 |
|---|---|---:|---:|---|---:|---|
| R(3,4) | SOLVED | ≥9 | ≤9 | C001〜C006 独立レビュー ACCEPTED | 完了2件 | R(3,4)=9独立検証済み、Discoveryは両GoalともCONTAMINATED |
| R(3,5) | SOLVED | ≥14 | ≤14 | R35-C001〜C004 PROVEN × ACCEPTED | 完了2件 | R(3,5)=14独立検証済み、Discovery CONTAMINATED |
| R(4,4) | PARTIAL_PROGRESS | ≥18 | — | R44-C001/C002 PROVEN × UNREVIEWED | 完了1件（G001 SOLVED） | 17頂点68辺、Discovery CONTAMINATED |

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
Stage 3はPR必須設定の有効性を証跡付きで確認してから開始する。サーバー設定は現時点で未確認。


## Stage 3 initialization

Stage 3 rootは `ab5624e9c411afe50137875811c26b46ecf13551`。PR必須rulesetのread-only検証を保存済み。
`benchmarks/r4-4/` を初期化し、最初のGoal `R44-G001` を定義した。

G001は正確な既知値を目標として与えず、固定予算内で `K_4` も独立4集合も持たない証明書を構成する。
研究はfresh Codex sessionで開始し、実際のGoal execution base・model/effort・Discovery・予算を開始前に記録する。


## Stage 3 — R44-G001研究成果

fresh sessionでbase `a0658a0fe5ca5e957b35f9460477fb6ebc089b95` から実行した。
17頂点68辺の証明書を構成し、全2,380個の4集合を検査してK4=0・独立4集合=0を確認。
従って下界 **R(4,4)>=18** は **PROVEN × UNREVIEWED**。
Benchmark全体は下界のみで `PARTIAL_PROGRESS`。上界・正確な値は未証明。

探索はn=4から順に増やすseed固定の焼きなましで、1,000万候補・124.310935125秒で候補予算終了。
n=18での探索不成功は不存在証明に使わない。全14証明書・verifier・7テスト・再現資材を保存した。
既知内容想起の利用前checkpointは `8ca54fd`、Discoveryは `CONTAMINATED`。
正確なmodel/effortは `missing`。Gitだけからのfresh-session開始を実施したが、別セッションでの全探索再実行は未実施。
Goal終了分類・PR提出記録・全体時間・counterは [研究ノート](../benchmarks/r4-4/research-notes.md) と `goal-measurements.json` を参照。
独立レビューとmainへのPR統合は後続工程。
