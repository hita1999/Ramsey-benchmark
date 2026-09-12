# R(3,5) — 研究ノート

## 現在の状態

Stage 2を初期化した。数学的な確定Claimはまだない。

- Benchmark状態: `INITIALIZED`
- 現在のGoal: `R35-G001`
- Discoveryタグ: `UNKNOWN`
- fresh-session再開評価: 未実施

## Goal実行記録

### R35-G001

研究開始前に `goals/G001.md` の契約に従って以下を埋める。

- Base commit:
- 作業ブランチ:
- 実際のmodel:
- 実際のreasoning effort:
- 開始時刻:
- 数値予算:
- token等の計測方法:
- fresh sessionか: `YES / NO`
- fresh sessionへ渡した入力commit:
- 最初に読んだファイル:
- 追加で要求した情報:
- Discoveryタグ: `UNKNOWN`

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

_現時点では未評価。_

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