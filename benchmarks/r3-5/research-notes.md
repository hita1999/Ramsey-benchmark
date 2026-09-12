# R(3,5) — 研究ノート

## R35-G002: 利用前の追加汚染記録

2026-09-12T06:45Z、上界の証明本文の作成前に、一般的なRamsey上界の漸化式
`R(s,t) ≤ R(s−1,t) + R(s,t−1)` と、その近傍・非近傍による場合分けを想起した。
さらに小さい三角形回避問題を次数制約と握手補題の偶奇性で扱う方針も想起した。
この時点では、これらの記憶を正しさの根拠にせず、研究成果としても主張しない。
本記録のみを独立checkpoint commitへ保存した後、利用する命題をGit上の確定事項と
自足的な証明で根拠づける。既存の値・構成の汚染記録も引き継ぎ、Discoveryは
`CONTAMINATED` のままとする。外部の既知解検索は行っていない。

## 現在の状態

- Benchmark状態: `SOLVED`（数学的証明が保存済み。上界・等号の独立レビューは未実施）。
- 現在のGoal: `R35-G002`、終了分類 **`SOLVED`**。
- R35-G001の探索停止分類: `EXHAUSTED_BUDGET`、具体的理由 `CANDIDATE_LIMIT`。
- 確定した下界: **R(3,5) ≥ 14**、`PROVEN × ACCEPTED`。
- 新しい上界・等号: **R(3,5) ≤ 14、R(3,5) = 14**、`PROVEN × UNREVIEWED`。
- Discoveryタグ: `CONTAMINATED`。
- fresh-session開始評価: `PASS`。別fresh sessionによる探索全再実行は未実施。

## Goal実行記録

### R35-G002 — 開始設定

- Goal契約: `goals/G002.md`。
- Base commit: `c9dd76f32edf6d1f22c007ac7bb7afa39ff29256`（開始時の `git rev-parse HEAD`）。
- 作業ブランチ: `codex/r35-g002-upper-bound`。
- 実際のmodel/effort: **GPT-6 Astra / High（ユーザーが開始メッセージで明示）**。
  実行環境のモデルID・effortを返す独立した計測値は取得できず、ユーザー申告と環境による確認を区別する。
- 開始: `2026-09-12T06:43:34Z`（`get_goal.createdAt=1789195414`）。準備・Git取得を含める保守的起点。
- wall-clock上限: **1200秒**、期限 `2026-09-12T07:03:34Z`。証明・検査・Git保存も含める。
- 手段: 理論証明を第一選択とし、必要な場合のみ補助計算を実施する。
- 開始時計測: `get_goal`、`2026-09-12T06:43:42Z`相当、tokensUsed=0、timeUsedSeconds=8。
- 準備途中計測: `get_goal`、`2026-09-12T06:44:47Z`、tokensUsed=20734、timeUsedSeconds=73。
  いずれもツール由来の累積カウンタであり、生成token数や費用ではない。
- fresh session: `YES`。過去の研究会話の引継ぎなし。入力はリポジトリ、Goalのパス、ユーザー申告の実行設定。
- 当初checkout: `e546714`。対象ファイルがなかったため `git fetch origin` により上記baseを取得した。
- 読んだ資料: README、methodology、prompts/codex-goal、対象Goal、r3-5のproblem・research-notes・proof・verification、
  r3-4のproof・verification、results/benchmark-summary。全て対象Gitリポジトリ内。
- 追加情報: Gitリモート更新のみ。過去のタスク閲覧、Web・既知解検索、ユーザーへの追加質問なし。
- fresh-session開始評価: 研究側 `PASS`。独立ReviewerによるこのGoalの評価は未実施。
- Discovery: `CONTAMINATED`。追加汚染のみのcheckpoint: `00b886b`。本設定も証明本文作成前にGitへ保存する。

### R35-G002 — 結果と引継ぎ

- 開始設定checkpoint: `36215af`。
- 成果物commit: `07b809b37a556a85898b38194172f0f3b48ace83`。
- Goal完了時計測: `update_goal(status="complete")`、`2026-09-12T06:49:41Z`、
  tokensUsed=60968、timeUsedSeconds=367（**6分7秒**）。準備・証明・自己監査・成果物commitを含み、
  20分上限内。この最終カウンタ追記の保存操作は含まない。tokenはツール由来の累積指標。
- 終了分類: **`SOLVED`**。理論証明を `proof.md` に保存した。
- 上界 `R35-C003` は既存Stage 1 `C005` の上界方向のみを利用する。
  Stage 1 `C003 → C004 → C005` の証明を再掲し、新しい非自明な補助命題の未証明引用を避けた。
- 等号 `R35-C004` は `R35-C002` と `R35-C003` を結合する。
- 証明本文保存後の途中計測: `get_goal`、`2026-09-12T06:46:58Z`、tokensUsed=43709、timeUsedSeconds=204。
- 終了直前計測: `get_goal`、`2026-09-12T06:49:20Z`、tokensUsed=53195、timeUsedSeconds=346（5分46秒）。
  準備・証明・自己監査・文書更新を含む。直後のGit保存と最終カウンタ追記はこの値に含めない。
- 文書検査: `git diff --check` 通過。変更は証明・研究ノート・検証記録・サマリーのみ。
- 数学的探索・補助計算: 未実施。上界の証明は理論のみ。コード・証明書の変更なし。
- 失敗した方針: なし。最初の近傍・非近傍による場合分けで証明が閉じた。
  追加のSAT・全探索・構造分類は必要にならなかった。
- 反証された仮説: なし。未解決の数学的ギャップ・残存ケース: なし。
- 自己監査: 三角形の有無、整数次数 `d≥5` / `d≤4` の被覆、非近傍数 `13−d≥9`、
  誘導部分グラフへの継承、頂点の追加、Stage 1の偶奇性と依存方向を確認。詳細は `verification.md`。
- fresh-sessionからGitだけで開始・完了できたか: 研究側 `PASS`。追加質問なし。
- 現在のボトルネック: 新しい上界と等号の独立レビューが未実施。
- Reviewerの重点: 9頂点補題の再掲、14頂点の全場合被覆、独立4集合に加える頂点が集合外か、
  上界に下界が混入しないか、Claim依存と汚染checkpointの順序。

### R35-G001

探索前に設定を記録し、`29a2663` でGitへ固定した。

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

### 実行結果・計測

- 汚染のみの独立checkpoint: `d74bedc`。実行設定checkpoint: `29a2663`。
- 成果物commit: `7a84bf9`。
- seed: `35001`。探索方式: 禁止集合を優先する1辺反転のsimulated annealing。
- 探索開始: `2026-09-12T06:09:57.026483Z`。
- 探索終了: `2026-09-12T06:11:57.594143Z`。
- 探索wall-clock: `120.568091375` 秒（Python `time.monotonic`）。
- 探索候補評価: **5,000,000**、上限ちょうど。実験は1回。
- 13頂点証明書の発見: 累積3,660評価、探索開始から約0.113秒。
- 14頂点で4,996,340評価、初期化500回、最小目的関数4、回避グラフ未発見。
- 途中計測: `get_goal`、2026-09-12T06:13:03Z、tokensUsed=70176、timeUsedSeconds=400。
- 検査: 証明書全9個が通過、verifierの6テストが通過。証明書とverifierだけを一時ディレクトリへコピーして単独実行し、保存出力との一致も確認。
- 最終状態の記録時刻: `2026-09-12T06:15:41.068568+00:00`。保守的開始時刻から約558.1秒（準備・実装・探索・検査・文書化を含む）。この後のGit保存を除く。30分上限内。
- Goal完了時計測: `update_goal(status="complete")`、2026-09-12T06:15:45Z、tokensUsed=81995、timeUsedSeconds=562（9分22秒）。ツール由来の累積値。この追記保存の操作は含まない。
- 終了直前計測: `get_goal`、2026-09-12T06:15:22Z、tokensUsed=80455、timeUsedSeconds=539。記録取得後の保存操作のtokenはこの値に含まれない。
- 独立レビュー: 2026-09-12、R35-C001/C002 `ACCEPTED`。詳細は `verification.md`。
- 探索再実行: 研究セッションでは未実施。独立Reviewerも5,000,000候補の探索全再実行は実施していない。再現コマンドは保存済み。

`search-result.json` は各頂点数の評価数・最小目的関数・時間を記録する。
5から13までの9証明書が保存され、最大のものが `certificate.json` と一致する。
候補評価数は発見時の整合性再計算や証明書の再検査を含まない。定義・再現条件は `search.py` と `verification.md` を参照。

## Claim台帳

### R35-C001

- 命題: 保存された13頂点26辺のグラフは三角形も独立5頂点集合も含まない。
- 数学的状態: `PROVEN`。
- 独立レビュー状態: `ACCEPTED`。
- Discovery: `CONTAMINATED`。
- 根拠: `certificate.json`、`verify.py`、`verification-result.json`、`proof.md` の全列挙の完全性説明。独立Reviewerは `review/r35-g001-independent.py` の別実装でも確認。
- 依存するClaim: なし。
- 研究成果対象commit: `7a84bf9`。
- 独立レビュー: `verification.md` 参照。
- 導入したGoal: `R35-G001`。

### R35-C002

- 命題: `R(3,5) ≥ 14`。
- 数学的状態: `PROVEN`。
- 独立レビュー状態: `ACCEPTED`。
- Discovery: `CONTAMINATED`。
- 根拠: `proof.md`。13頂点回避グラフの辺を赤、非辺を青とする彩色と定義。
- 依存するClaim: `R35-C001`。
- 研究成果対象commit: `7a84bf9`。
- 独立レビュー: `verification.md` 参照。
- 導入したGoal: `R35-G001`。

### R35-C003

- 命題: 14頂点の任意の単純グラフは三角形または独立5集合を持つ。従って `R(3,5) ≤ 14`。
- 数学的状態: `PROVEN`。
- 独立レビュー状態: `UNREVIEWED`。
- Discovery: `CONTAMINATED`。
- 根拠: `proof.md` の次数による2場合と、同書に再掲した9頂点補題の証明。
- 依存するClaim: Stage 1 `C005`（推移的に `C004`、`C003`）。
  `benchmarks/r3-4/proof.md` および `verification.md`、base `c9dd76f` で `PROVEN × ACCEPTED`。
- 研究成果対象commit: `07b809b37a556a85898b38194172f0f3b48ace83`。
- 導入したGoal: `R35-G002`。

### R35-C004

- 命題: `R(3,5) = 14`。
- 数学的状態: `PROVEN`。
- 独立レビュー状態: `UNREVIEWED`。
- Discovery: `CONTAMINATED`。
- 根拠: `proof.md` の下界と上界の結合。
- 依存するClaim: `R35-C002`、`R35-C003`。
- 研究成果対象commit: R35-C003と同じ成果物commit。
- 導入したGoal: `R35-G002`。

## R35-G002 Acceptance criteriaの自己確認

| 条件 | 保存根拠・判定 |
|---|---|
| 任意の14頂点グラフ | `proof.md` R35-C003、三角形あり／なし — PASS |
| 独立5集合と上界の導出 | 次数5以上の近傍／次数4以下の非近傍 — PASS |
| 補助補題に未証明の穴なし | Stage 1 C003〜C005の自足的証明を再掲 — PASS |
| 全ケース・端点の被覆 | 整数次数、非近傍が最小9頂点 — PASS |
| 依存関係の正確さと非循環性 | `proof.md` の依存図 — PASS |
| G001の探索不成功に非依存 | 上界証明が理論のみで完結 — PASS |
| proof.md単独で主要論理を追跡 | 定義・6頂点補題・9頂点補題を収録 — PASS |
| 終了状態と再開情報をGitへ保存 | 成果物commitと後続の計測記録 — PASS |

独立レビュー状態は本自己確認によって変更しない。

## 確定した結果

R35-G002で上界 `R35-C003` と等号 `R35-C004` の自足的証明を保存した。
両者は `PROVEN × UNREVIEWED` であり、以下のG001に対する独立受理とは区別する。

R35-C001、R35-C002は独立レビュー `ACCEPTED`。
保存証明書について研究側verifierは全286個の3集合と全1287個の5集合を検査した。
独立Reviewerは別のbitmask実装で、全頂点次数4、各辺の両端の共通近傍0、独立数4を確認した。
従ってこのリポジトリでは `R(3,5) ≥ 14` を独立検証済みの下界として扱う。

## 計算によって確認された結果

5〜13頂点で回避グラフを発見した。14頂点では今回の実験に限り未発見。
後者は探索ログの観測であり、数学的な不存在・最大性・上界のClaimではない。
探索中の最小目的関数4について、到達グラフ自体は保存していないので構造的Claimの根拠にしない。

## 予想・未検証の主張

上界・正確な値の新しいClaimは証明済みだが独立レビュー未実施である。
探索ログの決定的再現性については再現コマンドがあるが、別fresh sessionでの5,000,000候補全再実行は未実施。

## 反証された仮説・失敗した方針

- 同じ温度範囲・10,000提案の再始動を14頂点で繰り返しても、本予算では目的関数0に到達しなかった。
- 禁止構造数4の停滞が続いたが、その最適性も不存在も示していない。
- 数学的仮説を反証した記録はない。SAT・DFS等は未実施であり、失敗した方式には数えない。

## 既知情報による汚染

2026-09-12T06:07Z、探索コード作成・探索実行前に、事前学習から次を想起した。

- 既知値として `R(3,5)=14` という記憶。
- 13頂点の巡回グラフで差 `±1, ±5` を辺にする構成の記憶（正しさはこの時点では未検証）。

これらを証拠・探索目標・停止条件・初期グラフに利用しない。小さい頂点数からの汎用探索と、証明書の全列挙検査を用いる。想起自体があったため、本GoalとそのClaimのDiscoveryは `CONTAMINATED` とする。外部検索は実施していない。この記録だけを独立checkpoint commitに保存してから研究を開始する。

記録は `d74bedc` に研究ノートのみを変更する独立commitとして保存済み。
探索コード・初期グラフ・頂点数の進め方・停止判定には想起した値や構成を埋め込んでいない。
独立Reviewerはcommit順を確認し、汚染checkpointが成果物commitより前に存在することを監査した。
ただし想起による影響を完全には除去できないため、DiscoveryをCLEANへ変更しない。

## R35-G001 Acceptance criteriaの確認

| 条件 | 保存根拠・判定 |
|---|---|
| 非自明な回避グラフがGitにある | `7a84bf9` の `certificate.json`（13頂点） — PASS |
| 全3集合・全5集合の検査 | `verify.py`、列挙数286/1287 — PASS |
| verifierが探索から独立して実行可能 | 標準ライブラリのみ、証明書1ファイルを入力 — PASS |
| 再現コマンドと必要環境 | `verification.md` — PASS |
| 予算と停止理由 | 本書・`search-result.json` — PASS |
| fresh sessionでの研究開始記録 | 開始checkpoint `29a2663`、`verification.md` — PASS |
| Claim二軸状態 | R35-C001・R35-C002は `PROVEN × ACCEPTED` — PASS |
| 想起時の独立checkpoint | `d74bedc`、探索コード作成前 — PASS |

探索の予算切れとGoal成功を区別する契約に従い、Goal `SOLVED` は独立Reviewerにも受理された。

## 現在のフロンティアとボトルネック

- 下界: `R(3,5) ≥ 14`、`PROVEN × ACCEPTED`。
- 上界・等号: `R(3,5) ≤ 14`、`R(3,5) = 14`、`PROVEN × UNREVIEWED`。
- Discovery評価: `CONTAMINATED`。既知情報を想起せず発見できたという実験ではない。
- fresh-session研究開始: `PASS`。
- 別fresh sessionでの探索全再実行: `UNTESTED`。
- モデル比較: G001の設定は欠測、G002はユーザー申告があるが環境での独立確認は欠測。
  この2実験だけでモデル間の効率差を評価しない。

## 次に行う具体的な作業

1. `goals/G002.md` と `proof.md` を別Reviewerへ渡し、R35-C003/C004を独立に監査する。
   判定後に本書・verification・サマリーのレビュー状態を同期する。
2. 探索再現性自体を評価したい場合は、別fresh sessionで `verification.md` の5,000,000候補再実行を行い、研究Goalとは分離して記録する。
3. 独立レビュー後、Stage 2の効率・Discovery・fresh-session運用を振り返って次のGoalを設計する。

再開時は `goals/G002.md`、本書、`proof.md`、`verification.md` を読む。
既知情報の記録を見た後のセッションでもDiscovery汚染を明示し、既知値を証拠や停止条件にしない。
