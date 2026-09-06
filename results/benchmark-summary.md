# Ramsey Benchmark — サマリー

このファイルではbenchmark単位の結果を管理する。対応するbenchmark成果物と検証記録がGit上に存在するまでは、確定結果をここへ記録しない。

| Benchmark | 状態 | 下界 | 上界 | 検証 | Goal | 備考 |
|---|---|---:|---:|---|---:|---|
| R(3,4) | INITIALIZED | — | — | 未開始 | 完了0件 | G001準備済み |
| R(3,5) | NOT_STARTED | — | — | — | 0 | — |
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