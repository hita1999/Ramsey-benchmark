# Ramsey Benchmark — サマリー

このファイルではbenchmark単位の結果を管理する。対応するbenchmark成果物と検証記録がGit上に存在するまでは、確定結果をここへ記録しない。

| Benchmark | 状態 | 下界 | 上界 | 検証 | Goal | 備考 |
|---|---|---:|---:|---|---:|---|
| R(3,4) | SOLVED | ≥9 | ≤9 | C001〜C006 独立レビュー ACCEPTED | 完了2件 | R(3,4)=9独立検証済み、Discoveryは両GoalともCONTAMINATED |
| R(3,5) | SOLVED（上界レビュー待ち） | ≥14 | ≤14 | R35-C001/C002 ACCEPTED、C003/C004 UNREVIEWED（全てPROVEN） | 完了2件 | R(3,5)=14の証明を保存。Discovery CONTAMINATED |
| R(4,4) | NOT_STARTED | — | — | — | 0 | — |

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
`R35-C003: R(3,5)≤14` と `R35-C004: R(3,5)=14` は **`PROVEN × UNREVIEWED`**。
数学的証明は完成しているが、新しい上界・等号の独立レビューは次の工程である。
補助計算は不要だった。一般的なRamsey漸化式等の想起を証明作成前の独立checkpoint `00b886b` に記録し、
Discoveryは引き続き `CONTAMINATED` とした。
実行設定は **GPT-6 Astra / High（ユーザー申告）**。環境による独立確認は欠測。
fresh sessionからGitのみで研究を開始・完了したことを研究側で記録した。
20分予算・計測値・対象commit・Reviewerへの引継ぎは研究ノートを参照。
