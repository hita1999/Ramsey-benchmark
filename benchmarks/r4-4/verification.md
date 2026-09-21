# R(4,4) — 検証記録

## 現在の状態

Stage 3初期化済み。独立レビュー対象となる新しい数学的Claimはまだない。

- 完了Claim: なし
- 独立レビュー: 未実施
- Discovery: `UNKNOWN`
- main PR policy: 検証済み。 `results/stage3-pr-policy-verification.md` 参照。

## Reviewer運用

Stage 3では、研究成果のレビューartifact保存と現在状態の同期を同じreview closureの一部として扱う。

Reviewerは少なくとも次を記録する。

- 対象Goal・研究commit・base commit
- Reviewer model / reasoning effort（確認不能なら欠測）
- 日付
- 独立性
- 数学的判定
- Discovery監査
- 補助計算を使った場合の環境・コード・コマンド・結果
- proof / research-notes / verification / benchmark-summary の同期状況

補助計算コードを保存しただけで再現成功とは扱わない。実際に再実行した場合は、その環境と成功・失敗を記録する。
