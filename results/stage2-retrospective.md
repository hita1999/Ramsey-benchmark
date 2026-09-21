# Stage 2 retrospective — R(3,5)

## 結論

Stage 2はG001/G002の2 Goalで **R(3,5)=14** に到達し、R35-C001〜C004の独立レビューまで完了した。
fresh sessionがGitから研究を開始するhandoffも機能した。一方、G002成果の `main` への直接push事故と、
独立レビュー後の状態同期漏れが発生した。数学的完了、レビュー受理、PR統合、状態同期は別の完了条件として管理する必要がある。

Stage 3では、専用ブランチと明示的なpush先に加え、GitHub側のPR必須ルールを開始条件にする。
本retrospectiveで固定するのは運用方針であり、サーバー側の保護が設定・検証済みであるとは主張しない。
両GoalのDiscoveryは `CONTAMINATED`。未知問題への発見能力やモデル間の優劣は本実験から結論しない。

本書は研究プロセスの振り返りであり、新たな独立数学レビューではない。Stage 3の研究は開始していない。

## 評価対象と根拠

評価日: 2026-09-21。基準commit: `a5b161e7144820659bba28424bc0f5537fd4ea1a`（closure PR #6マージ後）。
主な根拠は [研究ノート](../benchmarks/r3-5/research-notes.md)、[証明](../benchmarks/r3-5/proof.md)、
[検証記録](../benchmarks/r3-5/verification.md)、[G002レビュー](../benchmarks/r3-5/reviews/G002.md)、Git履歴である。
実行時の欠測値を今回の推定値で埋めない。

| 工程 | 成果・根拠 | 統合 |
|---|---|---|
| G001 | 証明書 `7a84bf9`、最終計測 `f6ceaad`、レビュー記録 `27441b3`、状態同期 `c1d8193` | [PR #4](https://github.com/hita1999/Ramsey-benchmark/pull/4)、`1158d49` |
| G002 | 原成果 `07b809b`、最終計測 `5e9cc34`、復元後 `44ab7d1`、レビュー `752dd54` | [PR #5](https://github.com/hita1999/Ramsey-benchmark/pull/5)、`f40915a` |
| G002 closure | 4文書の状態同期 `d6b7fb9` | [PR #6](https://github.com/hita1999/Ramsey-benchmark/pull/6)、`a5b161e` |

## G001/G002の時間・token・成果

| 指標 | R35-G001 | R35-G002 |
|---|---|---|
| 契約 | 下界証明書の構成 | 任意の14頂点グラフについて上界を証明 |
| Researcher設定 | Codex / GPT-6。正確なmodel ID・effortは欠測 | GPT-6 Astra / Highはユーザー申告。環境による独立確認は欠測 |
| 予算 | wall-clock 1800秒、候補5,000,000回の早い方。探索は最大1200秒 | wall-clock 1200秒 |
| Goal開始 | 2026-09-12 06:06:23 UTC | 2026-09-12 06:43:34 UTC |
| Goal完了時計測 | 06:15:45 UTC、562秒（9分22秒） | 06:49:41 UTC、367秒（6分7秒） |
| 最終tokenカウンタ | 81,995 | 60,968 |
| 計算 | 探索120.568091375秒、5,000,000候補、seed 35001 | 理論のみ。研究時の補助計算なし |
| 得た成果 | 13頂点26辺の証明書、`R(3,5)≥14` | 自足的上界 `R(3,5)≤14`、上下界の結合で等号 |
| Goal終了 | SOLVED。探索停止はEXHAUSTED_BUDGET / CANDIDATE_LIMIT | SOLVED |
| 独立レビュー | R35-C001/C002 ACCEPTED | R35-C003/C004 ACCEPTED |

時間・tokenは研究ノートに保存された `update_goal(status="complete")` の累積カウンタである。
時間は準備・研究・自己検査・成果物保存を含むが、その後の最終カウンタ追記、独立レビュー、事故復旧、closureは含まない。
tokenは新規生成token数・API課金量ではない。単純合計は929秒（15分29秒）、142,963カウンタ単位だが、
Stage 2の全運用コストではない。レビュー・復旧・closureそれぞれの作業時間とtokenは欠測である。

G001は13頂点証明書を累積3,660評価・探索開始から約0.113秒で発見した後、14頂点に4,996,340評価を費やした。
最小目的関数4で停止した観測は、上界・不存在・最大性の根拠にしていない。
G002はStage 1の9頂点補題を使い、次数5以上／4以下の場合分けで閉じた。
計算で得た未知の構造が上界証明を導いたとは言えず、大規模分類・長時間停滞からの回復能力も未評価である。

## Discovery contamination

| Goal | 利用前に記録した想起 | 汚染checkpoint → 開始設定 → 成果 |
|---|---|---|
| G001 | 既知値14、13頂点巡回構成の差 `±1, ±5` | `d74bedc` → `29a2663` → `7a84bf9` |
| G002 | Ramsey上界の漸化式、近傍・非近傍による場合分け、次数と偶奇性の方針 | `00b886b` → `36215af` → `07b809b` |

Stage 1で不足した「利用前」の順序が独立commitによって監査可能になった。
G001は汎用探索と証明書の全列挙、G002は既存の受理済みClaimと自足的証明を根拠にした。
記憶の正しさ自体を証拠にしていないことと、記憶の影響を排除できたことは別である。
両Goalとも `CONTAMINATED` を維持し、数学的な `PROVEN × ACCEPTED` と両立させる。
既知解の外部検索は研究記録上実施していない。今回参照した外部資料はGitHubの運用仕様のみである。

## fresh-session handoff

両研究は過去の研究会話を引き継がず、リポジトリとGoalパスから開始したと記録されている。
G002には実行設定のユーザー申告も渡された。両者とも当初checkout `e546714` が古く、対象Goalがなかったため、
Gitリモートを取得してG001は `1d9ef4d`、G002は `c9dd76f` を開始baseにした。
Goal理解のための追加ユーザー質問は両者とも0件と記録されている。

- G001: 研究側の開始評価PASSを、独立Reviewerも保存資料に基づきPASSと判定した。
- G002: 研究側はGitのみで開始・完了したことをPASSと記録した。独立レビューは数学・依存・汚染順序を受理しているが、fresh-session運用への個別のPASS判定は記録していない。
- 未実施: 別fresh sessionでの5,000,000候補探索全体の再実行。これをhandoff成功から推定しない。
- 本retrospectiveとclosure: 元のタスクでの継続作業であり、追加のfresh-session実験には数えない。

したがって「Gitで研究状態を渡せた」は観測された成功である。ただし独立した探索再現、長時間Goalの中断復帰、
未知問題への汎化まで成功したとは評価しない。Stage 3では開始commitと必須ファイルを入力契約に固定する。

## 独立review artifactと再現性

G001は [別実装](../benchmarks/r3-5/review/r35-g001-independent.py) と
[保存結果](../benchmarks/r3-5/review/r35-g001-independent-result.json) を保存した。
研究側verifierをimportせず、辺の共通近傍と頂点集合bitmaskから検査し、独立数4も確認している。
Stage 1の「補助計算を報告したがコードがない」という欠落は改善した。
G002は [対象commit付きの論理監査](../benchmarks/r3-5/reviews/G002.md) を保存し、追加計算は報告していない。
両ReviewerはChatGPT / GPT-5.6 Solと記録されているが、effortは未記録なので補完しない。

ただし今回、保存されたG001独立検査を手元のPython 3.9.6で再実行すると環境の不足を検出した。

```sh
python3 --version
python3 benchmarks/r3-5/review/r35-g001-independent.py \
  benchmarks/r3-5/certificate.json \
  --output /tmp/stage2-retrospective-review-result.json
```

結果: `AttributeError: 'int' object has no attribute 'bit_count'`（別実装の次数計算行）。
研究側環境のPython 3.9.6をReviewer実装の動作環境と見なすことはできない。
今回の再実行は失敗であり、成功した再現試験に数えない。コード・保存結果の存在と、環境を含む再現手順の完備を区別する。
これは保存済みの数学的受理を覆す反例ではなく、再現環境記録の不足である。
次の整備では別実装が動作するPython環境を明記し、保存JSONとの一致を確認する。過去のレビュー実行環境を推定で書き換えない。

## 状態同期漏れ

`752dd54` でG002レビューを保存し、PR #5をマージした時点でも、proof・research-notes・verification・サマリーは
上界・等号をUNREVIEWED／レビュー待ちと記載していた。Stage 1で同じ問題に対する手順を追加した後にも再発した。
規約の存在だけでは、レビュー担当から同期担当への引継ぎを担保できていなかった。

`d6b7fb9` が4文書を同期し、PR #6の `a5b161e` で統合した。原証明・実行計測・Discoveryタグは維持した。
過去の自己監査のUNREVIEWEDは時点を明示して残しており、現在の判定と混同しない。
Stage 3ではレビュー提出者が同期まで担当するか、PR内にclosure担当を明記する。
レビューartifactだけで運用上の完了とせず、マージ前に4文書の現在のClaim状態と対象commitを照合する。

## accidental direct push → revert → PR復旧

| 順序 | Gitで確認できる事実 |
|---|---|
| 1. 直接統合 | `main` のfirst-parent履歴に `00b886b`、`36215af`、`07b809b`、`5e9cc34` がPRマージなしで入った。事故であることはG002レビューにも明記 |
| 2. revert | `b4625cf` がG002変更を取り消し、研究前 `c9dd76f` と完全に同じツリーへ戻した。履歴は残した |
| 3. PR再構成 | `37d0055`、`e9f93e1`、`6397ba8`、`44ab7d1` で変更を再構成。`44ab7d1` のツリーは原完了 `5e9cc34` と同一 |
| 4. review・マージ | `752dd54` で独立レビューを追加し、PR #5を `f40915a` でマージ |
| 5. closure | 残った状態同期を `d6b7fb9`、PR #6の `a5b161e` で完了 |

今回、次の比較が全て終了コード0になることを確認した。

```sh
git diff --exit-code c9dd76f b4625cf
git diff --exit-code 5e9cc34 44ab7d1
git diff --exit-code d6b7fb9 a5b161e
git log --first-parent --oneline a5b161e
```

ツリーの同一性は証明内容を変更せず復旧できたことを示すが、初回からPRを守ったことにはならない。
commitとレビュー記録だけでは、事故時の具体的なpushコマンド、認証主体、当時のGitHub保護設定は確定できない。
今回のローカル設定には `codex/r35-g002-upper-bound` のupstreamが `origin/main` として残っていた。
これは注意点だが、事故の直接原因と断定できない。機能ブランチ名だけでは送信先の安全性を保証しない。

## Stage 3のPR必須化

### サーバーで強制する開始条件

管理担当はStage 3の最初の研究Goalを開始する前に、`main` に適用されるGitHub rulesetを有効化し、
次の設定と確認日・確認者・取得方法をGitへ保存する。現時点の適用状況は **未確認**。

- 対象は `refs/heads/main`、状態はActive、`Require a pull request before merging` を有効にする。
- 管理者・利用するAppを含め、直接pushを許すbypassを設定しない。force pushと削除も禁止する。
- rulesetが利用できない場合は同等のbranch protectionを設定し、管理者にも適用する。
  同等の強制を用意できなければ、その不足を記録してStage 3の開始条件を満たしたとは扱わない。
- GitHubの承認数は数学レビューとは別に決める。独立した承認可能アカウントを確保した場合は1件以上を必須にする。
  単独アカウント運用ではPR必須とGit内の数学レビューartifactを組み合わせ、架空のGitHub承認を要求・報告しない。

PR必須ルールと承認数は別設定である。GitHub公式の
[ruleset仕様](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets#require-a-pull-request-before-merging) と
[bypass設定](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/creating-rulesets-for-a-repository#granting-bypass-permissions-for-your-branch-or-tag-ruleset) を参照。
branch protectionの代替を使う場合は [管理者への適用](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches#do-not-allow-bypassing-the-above-settings) も確認する。

設定の証跡は `results/stage3-pr-policy-verification.md` に保存する運用とする（本変更では未作成・未検証）。
有効な対象ルール・bypass・通常使用する主体の権限をread-onlyで確認し、必要な拒否試験は同じ条件のテスト用ブランチで行う。
本番 `main` への試験pushはしない。`git push --dry-run` やローカルhookだけをサーバー拒否の証明にしない。

### 研究・レビュー担当の手順

1. 最新の `origin/main` から `git switch --no-track -c codex/<goal> origin/main` で専用ブランチを作る。
   base commitとbranchを記録し、upstreamが `origin/main` を指していないことを確認する。
2. push前にbranch・remote・差分を確認する。pushが許可された作業では
   `git push -u origin HEAD:refs/heads/codex/<goal>` のように送信先を明示する。
   引数なしpush、`HEAD:main`、`--all`、`--mirror`、mainへのforce pushを使わない。
3. 成果・checkpoint・レビュー・closure・文書更新・事故復旧もPR経由にする。ローカルmainへmergeしてpushしない。
4. PRにbase/result commit、Goal状態、Claim状態、Discovery、検証、残課題を明記する。
   SOLVEDと独立ACCEPTEDは別軸のまま保つ。研究checkpointはUNREVIEWEDと明示してPRに保存できる。
5. レビュー担当はartifactと補助計算資材を保存し、4文書を同期する。担当を引き継ぐ場合はclosure責任者を明示する。
6. 統合担当が現在の状態・対象commit・未解決項目を照合してGitHub上でmergeし、merge SHAを引継ぎに残す。

文書での禁止とローカルでの事前確認は補助策であり、サーバー設定の代替ではない。
今回の新規ブランチも作成直後に継承した `origin/main` upstreamを解除した。
事故時は送信を止め、履歴・ref・影響を保存し、revertと再適用の差分を確認して復旧PRを作る。
今回実施したmainへの直接revertを、Stage 3の通常の復旧手順として繰り返さない。

## Stage 3への引継ぎ

| 項目 | 現状 | 担当・次の完了条件 |
|---|---|---|
| 数学的結果・closure | 完了、全4 Claim ACCEPTED | 統括担当がStage 2終了を前提に次Goalを設計 |
| fresh-session入力 | 研究開始handoffは機能 | Goal設計担当がbase・契約・必読ファイルを固定 |
| Discovery・計測 | 汚染順序と最終カウンタを保存 | 研究担当は同手順を継続。欠測を推測で埋めない |
| Reviewer環境 | 別実装は保存済み、Python 3.9.6再実行は失敗 | 再現確認担当が動作環境を明記し、保存JSONとの一致を確認 |
| 状態同期 | PR #6で解消 | Reviewer／明示したclosure担当が同一PR内で同期を完了 |
| main保護 | 設定・有効性は未確認 | 管理担当が上記設定の証跡を保存。Stage 3開始前の必須条件 |

本変更はretrospectiveと運用プロトコルの固定までであり、GitHub設定の変更、Stage 3のGoal作成・実行は含まない。
