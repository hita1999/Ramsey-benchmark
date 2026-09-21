# R(4,4) — 研究ノート

## 現在の状態

- Benchmark状態: `READY`。Stage 3初期化済み、研究は未開始。
- Stage 3 root: `ab5624e9c411afe50137875811c26b46ecf13551`。
- 現在定義済みGoal: `R44-G001`。
- 完了Goal: 0。
- 数学的Claim: まだなし。
- Discovery: `UNKNOWN`。研究開始前であり、想起が報告されていないことをCLEANとは扱わない。
- main PR policy: `PASS`。詳細は `results/stage3-pr-policy-verification.md`。
- fresh-session研究: 未実施。

## Stage 3初期化

2026-09-21、Stage 2 closure・retrospective・PR policy verification完了後に初期化した。

G001では正確な値をGoalへ埋め込まず、固定予算内で `K_4` も独立4集合も持たない証明書を構成する。
得られた最大頂点数は今回の探索予算内での結果であり、全グラフ中の最大性を意味しない。

研究担当は開始時に次を本書へ追記する。

- Goal execution base commit
- fresh sessionか
- 実際のmodel / reasoning effort
- 数値予算と計測方法
- 作業branchと明示的push先
- 研究開始時点のDiscovery
- 読んだGit内ファイルと追加で得た情報
- 利用前の既知情報想起があれば、その具体的内容とcheckpoint commit

## Claim台帳

まだ新規Claimはない。最初のClaim IDは `R44-C001` から開始する。

## 現在のフロンティア

最初の課題は `R44-G001`。固定予算内で下界証明書を構成し、certificate-only verifierと再現資材を保存する。

探索不成功は上界・不存在・最大性の根拠にしない。
