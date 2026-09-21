# R44-G001 再現手順

Python 3.9以上、標準ライブラリのみ。repository rootで実行する。
実行環境は `environment.json`。保存証明書の検査に探索の再実行は不要。

```sh
python3 benchmarks/r4-4/verify.py benchmarks/r4-4/run/certificate.json
python3 -m unittest discover -s benchmarks/r4-4 -p 'test_*.py' -v
```

verifierはJSONをstdoutへ出力し、validならexit 0、それ以外はexit 1。
`--output /tmp/r44-verification.json` を追加すると結果をファイルへ保存できる。
検査対象は頂点0..n-1、各辺は昇順の整数ペアで、自己ループ・範囲外・重複辺を認めない。
全4集合を最後まで検査する。

## 全保存証明書の検査

```sh
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'benchmarks/r4-4')
from verify import verify
for p in sorted(Path('benchmarks/r4-4/run/certificates').glob('*.json')):
    result = verify(json.loads(p.read_text()))
    print(p.name, json.dumps(result, sort_keys=True))
    assert result['valid']
PY
```

## 探索の再実行（別途計算予算が必要）

出力ディレクトリは存在しないパスを指定する。保存成果物を上書きしない設計。

```sh
python3 benchmarks/r4-4/search.py --output /tmp/r44-replay --seed 20260921 --max-evaluations 10000000 --seconds 600 --restart-steps 50000
```

n=4から開始し、スコア0を見つけるごとにnを1増やす。頂点数による停止条件なし。
各nで最初および50,000反転候補ごとに、全辺を独立Bernoulli(1/2)で再初期化する。
PRNGは単一の `random.Random(20260921)`。n変更や再始動でreseedしない。
候補は一様に選んだ辺の有無の反転。スコアはK4数と独立4集合数の和。
改善・同点は常に採用、悪化差分dは `exp(-d/T)` の確率で採用。
Tは各再始動内のstep=0..49999で `1.5*(0.05/1.5)**(step/49999)`。
初期化のスコア評価を1、反転候補評価を採否によらず1と数える。
スコア0を検出したら辺リストを保存するだけで、追加の探索スコア評価は行わない。
4集合の列挙や差分更新そのものを別候補として重複計数しない。

停止は10,000,000候補または600秒の早い方。時間制限はグラフ初期化前・各候補前に判定するため、
最後の原子的処理・出力の実行時間分の小さな超過を許す。Goal全体の30分予算には十分な余裕を確保した。
同一Python環境と候補数で再実行すれば、時刻・経過時間以外の探索軌跡は決定的。
遅い環境で時間上限が先に来れば候補数・最終成果物は異なりうる。
本Goal内では探索全体の二度目の実行はしていない。

## verifierを探索資材から隔離する検査

```sh
r44_verify_dir=$(mktemp -d)
cp benchmarks/r4-4/verify.py "$r44_verify_dir/verify.py"
cp benchmarks/r4-4/run/certificate.json "$r44_verify_dir/certificate.json"
python3 -I "$r44_verify_dir/verify.py" "$r44_verify_dir/certificate.json"
```

保存結果は `isolated-verification.json`。これは研究担当によるコード依存性の確認であり、別Reviewerによる独立レビューではない。
