# Stage 3 PR policy verification

## 結論

Stage 3開始前のGitHub側PR必須化をread-onlyで確認した。

- 判定: **PASS**
- 確認日: 2026-09-21
- 対象repository: `hita1999/Ramsey-benchmark`
- 対象branch: `refs/heads/main`
- 確認時のmain: `70ca639e96979bd0b6475cdbb0d1d85866785881`
- 確認方法: GitHub REST APIのrulesetおよびbranch metadataのread-only取得
- 本番 `main` への試験push: **未実施**。保護確認のために本番branchへ破壊的・不要なpushは行っていない。

この確認により、Stage 2 retrospectiveで定めた「mainへのPR必須ルールとbypass制限をStage 3開始前に確認する」という開始条件を満たす。

## Ruleset確認

GitHub repository ruleset:

- Ruleset ID: `22387974`
- Name: `main`
- Target: `branch`
- Enforcement: `active`
- Include: `refs/heads/main`
- Exclude: なし
- Bypass actors: `[]`
- Current user can bypass: `never`

有効なrule:

1. `deletion`
2. `non_fast_forward`
3. `pull_request`

`pull_request` ruleの主要parameter:

- Required approving review count: `0`
- Dismiss stale reviews on push: `false`
- Required reviewers: `[]`
- Require code owner review: `false`
- Require last push approval: `false`
- Require review thread resolution: `false`
- Require extra approval for unattributed changes: `true`
- Allowed merge methods: `merge`, `squash`, `rebase`

したがって、`main` への通常の変更はnon-target branch上で作成し、pull request経由で統合することがGitHub側rulesetで要求されている。

Required approvalsを0とすることは、本benchmarkの数学的独立レビューをGitHub上のAPPROVE操作と同一視しない運用に対応する。単独アカウントで自分のPRを正式承認できないことを理由に、架空のGitHub approvalを要求・記録しない。数学的レビューはGit内のreview artifactとClaimの独立レビュー状態で管理する。

## main branch metadata

GitHubのbranch metadataでは、確認時点の `main` は:

- Head: `70ca639e96979bd0b6475cdbb0d1d85866785881`
- `protected: true`

だった。

同じレスポンス内のlegacy branch protection用 `protection.enabled` は `false` だが、本repositoryではRepository Rulesetにより保護しているため、rulesetの `enforcement=active` および `main` 対象条件と矛盾しない。

## Bypass監査

rulesetの `bypass_actors` は空であり、read-only API上の `current_user_can_bypass` は `never` だった。

よって、通常利用している現在の認証主体について、rulesetを迂回して直接 `main` へ統合できるbypass権限は確認されなかった。

この記録はread-only設定監査であり、直接pushの拒否を実際に本番 `main` で試験した記録ではない。将来設定が変わった場合は、Stage 3の継続前に再確認する。

## Stage 3への引継ぎ

この文書を含むPRが `main` にマージされた後、その**merge commit SHA**をStage 3のimmutable baseとして扱う。

Stage 3の研究担当は、そのbaseから専用branchを作成し、成果・checkpoint・review・closureをPR経由で統合する。

開始時には少なくとも以下を記録する。

- immutable base commit
- Goal path
- researcher model / reasoning effort（確認不能なら欠測）
- fresh-sessionか
- Discovery tag
- 数値予算
- 作業branch
- 明示的なpush先

本確認はGitHub側PR policyの開始条件だけを扱う。R(4,4)のGoal作成・研究そのものはまだ開始していない。
