# R(3,5) — 検証記録

## 現在の状態

R35-C001（証明書の回避条件）・R35-C002（下界）は **`PROVEN × ACCEPTED`**。
R35-C003（上界）・R35-C004（等号）は **`PROVEN × UNREVIEWED`**。

## R35-G002: 研究担当の自己監査・独立レビュー待ち

- 実施日: 2026-09-12。
- Researcher: Codex。実行設定はユーザー申告の GPT-6 Astra / High。
- Base commit: `c9dd76f32edf6d1f22c007ac7bb7afa39ff29256`。
- 対象: `proof.md` の上界の定義・補助Claim再掲・R35-C003/C004。
- 発見経路から独立しているか: **NO**。別Reviewerはまだ実施していない。
- 数学的状態: `PROVEN`。独立レビュー状態: `UNREVIEWED`。
- Discovery: `CONTAMINATED`。
- 数学的な未解決ギャップ: 自己監査ではなし。
- 計算依存: 上界はなし。補助計算・SAT・14頂点全探索を実施していない。

自己監査では次を確認した。

| 対象 | 確認した論理 |
|---|---|
| 三角形がある場合 | それだけで14頂点命題を満たす |
| 近傍の独立性 | 近傍内の辺と中心頂点は三角形になる |
| 次数境界 | 任意の整数次数は `d≥5` または `d≤4` の一方に属する |
| `d=4` の端点 | 非近傍は `14−1−4=9` 頂点で既存補題が適用可能 |
| `d<4` の場合 | 非近傍から任意の9頂点を取ればよい |
| 独立集合の拡張 | `S⊆M(v)` なので `v∉S` かつ全ての `v-s` が非辺 |
| 6頂点補題の再掲 | 次数3以上／2以下の全場合を扱う |
| 9頂点補題の再掲 | 回避を仮定した全頂点次数3と次数和27の奇偶矛盾 |
| 既存Claimの状態 | r3-4 C003〜C005の本文・独立レビューをbase commitで確認 |
| 下界との分離 | 上界R35-C003にR35-C001/C002や探索ログへの依存なし |
| 等号 | ACCEPTEDな下界とUNREVIEWEDな上界を結合し、等号もUNREVIEWED |

再確認には `proof.md` の理論証明を最初から読み、末尾の依存図を照合すればよい。
新たな実行環境やプログラムは不要。既存の下界再現コマンドは本書末尾に維持する。

独立Reviewerには、全ケースと端点、補題の再掲、依存方向、集合に追加する頂点の区別、
数学的状態とレビュー状態の分離を重点確認してもらう。
運用面では汚染checkpoint `00b886b` → 開始設定 `36215af` → 成果物commitの順序と、
研究ノートのfresh-session記録・計測記録を監査する。
成果物対象commit: `07b809b37a556a85898b38194172f0f3b48ace83`。

## R35-G001: 独立レビュー済みの記録

以下はG001レビュー時点の記録であり、「上界・正確な値は未確定」はその時点の判定を表す。

- 対象PR: #4
- Base commit: `1d9ef4ddad02e5a120dddee508bb9c33979d1b3d`
- 研究成果head: `f6ceaad1f5ec90ec7f577ab7ee8ed1b98c889fb3`
- Reviewer: ChatGPT / GPT-5.6 Sol
- 独立レビュー日: 2026-09-12
- Discovery: `CONTAMINATED`

研究担当自身の検査と、以下の独立Reviewer検査を区別する。

## 独立レビュー結果

### R35-C001

- Claim: 保存された13頂点26辺のグラフは三角形も独立5頂点集合も含まない。
- 数学的状態: `PROVEN`
- 独立レビュー状態: `ACCEPTED`
- 発見経路から独立しているか: `YES`
- 残っている数学的ギャップ: なし。

Reviewerは研究側の `verify.py` を証拠として前提にせず、隣接bitmaskによる別実装で `certificate.json` を直接検査した。再現資材は次に保存した。

```text
review/r35-g001-independent.py
review/r35-g001-independent-result.json
```

実行方法:

```sh
python3 benchmarks/r3-5/review/r35-g001-independent.py \
  benchmarks/r3-5/certificate.json \
  --output /tmp/r35-g001-independent-result.json
cmp benchmarks/r3-5/review/r35-g001-independent-result.json \
  /tmp/r35-g001-independent-result.json
```

独立検査では次を確認した。

- 頂点数: 13
- 辺数: 26
- 次数列: 13頂点すべて次数4
- 各辺の両端の共通近傍: 0件。従って三角形は存在しない。
- 全 `C(13,5)=1287` 個の5頂点集合について独立5集合: 0件
- 独立数: 4
- 例として独立4集合 `{0,1,2,4}` が存在

従って保存グラフは三角形を持たず、独立5頂点集合も持たない。

### R35-C002

- Claim: `R(3,5) >= 14`。
- 数学的状態: `PROVEN`
- 独立レビュー状態: `ACCEPTED`
- 依存: R35-C001
- 発見経路から独立しているか: `YES`
- 残っている数学的ギャップ: なし。

R35-C001の13頂点グラフの辺を赤、非辺を青に対応させると、赤三角形も青 `K5` も存在しない `K_13` の2彩色が得られる。Ramsey数の定義から `R(3,5)>13`、従って整数性より `R(3,5)>=14` である。

この判定は上界・正確な値を主張しない。

## 研究側verifierの監査

研究側の `verify.py` は証明書の形式を検査した後、全3頂点集合と全5頂点集合を `itertools.combinations` で列挙する。保存結果は

```text
n=13
edges=26
triples_checked=286
five_sets_checked=1287
triangles=0
independent_fives=0
valid=true
ramsey_lower_bound=14
```

であり、独立Reviewerの別実装と一致する。保存結果は `verification-result.json` にある。

`test_verify.py` も監査した。完全・空グラフ、全1024個の5頂点ラベル付きグラフと隣接行列oracleとの照合、全列挙が最初の違反で停止しないこと、不正入力、CLI終了コードを対象にしており、verifierの用途に対して妥当なテストである。

## 探索ログ・予算の監査

`search.py` はseed付きの conflict-guided single-edge simulated annealing であり、候補評価の定義をコード冒頭に固定している。

保存された `search-result.json` では:

- seed: `35001`
- max evaluations: `5,000,000`
- time limit: `1200` 秒
- 実際の探索時間: 約 `120.568` 秒
- stop reason: `CANDIDATE_LIMIT`
- search stop classification: `EXHAUSTED_BUDGET`
- best_n: `13`
- n=13発見: 累積 `3,660` 評価
- n=14: `4,996,340` 評価、best_score=4、未解決

となっている。

探索コードは n=5 から開始し、score=0 の証明書を得た場合だけ nを増やす。初期グラフは各辺を確率0.35で生成する一般的ランダムグラフであり、保存済み証明書や記憶した構成を初期値として読み込む処理はない。

重要な区別として、Reviewerは今回5,000,000候補の探索全体を別fresh sessionで再実行していない。そのため、**探索ログの決定的再現性は「再現コマンドあり・独立再実行未実施」** とする。これはR35-C001/C002の数学的受理には影響しない。証明は保存された有限証明書だけで完結する。

また、n=14で見つからなかったことやbest_score=4を、最大性・不存在・上界の根拠として使っていないことを確認した。

## 汚染checkpointの監査

コミット順を監査した。

1. Base: `1d9ef4d`
2. `d74bedc` — `Record R35-G001 knowledge contamination before research`
3. `29a2663` — `Fix R35-G001 execution budget and fresh-session provenance`
4. `7a84bf9` — `Save R35-G001 fixed-budget certificate and exhaustive verification`
5. 後続の研究状態・計測更新

`d74bedc` では研究ノートだけに、探索前に想起した既知値 `R(3,5)=14` と13頂点巡回構成の記憶を記録している。探索成果物のcommitより前に独立checkpointが存在するため、Stage 1で不足していた「汚染記録のGit上の時間順序」は今回は監査可能である。

ただし、既知情報を想起した以上Discovery評価は `CONTAMINATED` のままとする。証明の正しさとDiscovery成功を混同しない。

## fresh-session実験の監査

研究記録によれば:

- 過去のRamsey会話は引き継がれていない。
- ユーザーから渡されたのはリポジトリと `benchmarks/r3-5/goals/G001.md` の場所。
- 最初のcheckoutは古い `e546714` でGoalが存在しなかった。
- `git fetch origin` により `1d9ef4d` を取得して研究を開始した。
- ユーザーへの追加質問は不要だった。

したがって **「fresh sessionからGitだけでGoalを理解して研究開始できた」** という運用実験は `PASS` と判定する。ただし「別fresh sessionによる探索再実行」は未実施であり、別の評価項目として残す。

## G001 Acceptance criteria監査

- 非自明な回避グラフを保存: `PASS`
- verifierが全3集合・全5集合を検査: `PASS`
- verifierが探索コードから独立実行可能: `PASS`
- 再現コマンド・環境を保存: `PASS`
- 予算・停止理由を保存: `PASS`
- fresh session開始記録: `PASS`
- Claim二軸状態: `PASS`
- 汚染時checkpoint規約: `PASS`

従って探索停止は `EXHAUSTED_BUDGET` だが、Goal終了分類 `SOLVED` は契約に適合する。

## 独立レビュー総合判定

- R35-C001: `PROVEN × ACCEPTED`
- R35-C002: `PROVEN × ACCEPTED`
- 確定下界: `R(3,5) >= 14`
- R35-G001 Acceptance criteria: 全項目 `PASS`
- Goal終了分類: `SOLVED` を受理
- Discovery: `CONTAMINATED`
- fresh-session研究開始: `PASS`
- 別fresh sessionでの探索全再実行: `UNTESTED`
- 上界・正確な値: 未確定

---

## 研究担当が保存した再現情報

### 入力・環境

- `certificate.json`: 頂点 `0,...,12` と26辺。
- `certificates/n05.json` ～ `certificates/n13.json`: 実行中に得た全9証明書。
- Python 3.9.6、標準ライブラリのみ、macOS 13.7.4 arm64で実行。
- `verify.py` は探索コードもログもimport・参照しない。

### 証明書の再検査

```sh
python3 benchmarks/r3-5/verify.py benchmarks/r3-5/certificate.json
python3 -m unittest discover -s benchmarks/r3-5 -p 'test_*.py' -v
```

### 探索の再実行

```sh
python3 -u benchmarks/r3-5/search.py --output /tmp/r35-g001-replay --seed 35001 --max-evaluations 5000000 --seconds 1200 --restart-interval 10000
python3 benchmarks/r3-5/verify.py /tmp/r35-g001-replay/certificate.json
cmp benchmarks/r3-5/certificate.json /tmp/r35-g001-replay/certificate.json
```

低速な環境では時間上限が先に来る可能性があるため、5,000,000評価到達そのものを比較する場合は十分な実行速度を確保する必要がある。
