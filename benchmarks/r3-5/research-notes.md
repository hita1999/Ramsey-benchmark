# R(3,5) — 研究ノート

## 現在の状態

Stage 2を初期化した。数学的な確定Claimはまだない。

- Benchmark状態: `INITIALIZED`
- 現在のGoal: `R35-G001`
- Discoveryタグ: `CONTAMINATED`
- fresh-session再開評価: 未実施

## Goal実行記録

### R35-G001

研究開始前に `goals/G001.md` の契約に従って以下を埋める。

- Base commit: `1d9ef4ddad02e5a120dddee508bb9c33979d1b3d`
- 作業ブランチ: `codex/r35-g001-lower-bound`
- 実際のmodel: システムが公開する名称は GPT-6 / Codex。正確なモデルIDは実行環境から確認できず欠測（推奨IDの使用は断定しない）。
- 実際のreasoning effort: 実行環境に公開されておらず欠測。推奨highと一致するかは未確認。
- 開始時刻: `2026-09-12T06:06:23Z`（goalカウンタcreatedAt。準備・Git取得も含める保守的起点）。
- 数値予算: wall-clock 1800秒、候補評価5,000,000回の早い方。成果物保存時間を含め30分以内とする。探索は最大1200秒とし残りを検証・保存に使う。候補評価は初期化・再始動時の目的関数計算、または1辺反転提案の差分評価各1回。
- token等の計測方法: `get_goal`。準備途中（2026-09-12T06:06:30Z相当）tokensUsed=6481/timeUsedSeconds=7、探索前（06:07:46Z相当）tokensUsed=44769/timeUsedSeconds=83。ツールが返す累積指標であり、純粋な研究出力token数ではない。
- fresh sessionか: `YES`。過去の研究会話の引継ぎなし。
- fresh sessionへ渡した入力commit: 当初checkoutは`e546714`で指定ファイルがなかった。`git fetch origin`によりGoalを含む`1d9ef4d`を取得して開始。
- 最初に読んだファイル: README、旧checkoutのprompts/codex-goal.md、methodology.md、results/benchmark-summary.md。その後origin/mainの指定Goal、r3-5の4文書、更新済みmethodologyとGoalプロトコル。
- 追加で要求した情報: ユーザーへの要求なし。Gitリモートからの更新取得のみ。Web・既知解検索なし。
- Discoveryタグ: `CONTAMINATED`

## Claim台帳

重要な主張ごとに次の形式で記録する。

### テンプレート

- Claim ID: `Cxxx`
- 命題:
- 数学的状態: `CONJECTURE | COMPUTATIONALLY VERIFIED | PROVEN | REFUTED`
- 独立レビュー状態: `UNREVIEWED | ACCEPTED | NEEDS_REVISION | REJECTED`
- 根拠:
- 依存するClaim:
- 対象commit:
- 導入したGoal:

## 確定した結果

_まだなし。_

## 計算によって確認された結果

_まだなし。_

## 予想・未検証の主張

_まだなし。_

## 反証された仮説・失敗した方針

_まだなし。_

## 既知情報による汚染

2026-09-12T06:07Z、探索コード作成・探索実行前に、事前学習から次を想起した。

- 既知値として `R(3,5)=14` という記憶。
- 13頂点の巡回グラフで差 `±1, ±5` を辺にする構成の記憶（正しさはこの時点では未検証）。

これらを証拠・探索目標・停止条件・初期グラフに利用しない。小さい頂点数からの汎用探索と、証明書の全列挙検査を用いる。想起自体があったため、本GoalとそのClaimのDiscoveryは `CONTAMINATED` とする。外部検索は実施していない。この記録だけを独立checkpoint commitに保存してから研究を開始する。

既知値・既知構成・既知証明方針・主要な既知補題を想起した場合は、その内容を利用する前にここへ具体的に記録し、独立したcheckpoint commitを作る。

## 現在のフロンティア

### 下界

独立レビュー済みの証明書はまだない。

### 上界

独立レビュー済みの証明はまだない。

## 現在のボトルネック

固定予算内で、三角形も独立な5頂点集合も持たない具体的グラフを探索し、再現可能な下界証明書としてGitへ保存する。

## 次のGoal

`R35-G001`: 既知値を停止条件にせず、固定予算内の探索で得られる最良の下界証明書を保存・検証し、fresh sessionからGitだけで再現可能な研究状態を作る。