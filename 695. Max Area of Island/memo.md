
## step1:
まずどこかlandに着いたら深さ優先探索でその島を探索し尽くそうと思い、dfs関数で上下左右で未探索かつlandである場所を探索していった。ここで、どうやって各島の面積を保存しようと思い悩み、関数に数値を保存するオブジェクトを渡してlandを見つけるたびに1づつ足していけばいいと考えた。そこで各島にラベルを付け、島を見つけるたびに各ラベルに1づつ足していき最後にそれらのmax値を返却した。

### code
```python
from collections import defaultdict
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        visited = [[0]*n for _ in range(m)]
        max_area = 0
        area_dict = defaultdict(int)
        label_max = 0

        def dfs(p, q, dict, label):
            nonlocal visited
            visited[p][q] = 1
            area_dict[label] += 1
            if p-1 >= 0 and visited[p-1][q] == 0 and grid[p-1][q] == 1:
                dfs(p-1, q, area_dict, label)
            if p+1 < m and visited[p+1][q] == 0 and grid[p+1][q] == 1:
                dfs(p+1, q, area_dict, label)
            if q-1 >= 0 and visited[p][q-1] == 0 and grid[p][q-1] == 1:
                dfs(p, q-1, area_dict, label)
            if q+1 < n and visited[p][q+1] == 0 and grid[p][q+1] == 1:
                dfs(p, q+1, area_dict, label) 
            
        for i in range(m):
            for j in range(n):
                if visited[i][j] == 0 and grid[i][j] == 1:
                    dfs(i, j, area_dict, label_max)
                    label_max += 1
                visited[i][j] = 1
        if len(area_dict.values()) == 0:
            return 0
        max_area = max(area_dict.values())
        return max_area
```

## step2:
最後のmax_areaを求めるところを、各島の面積を求めたところで判別できると感じたので削除した。

### code
```python
from collections import defaultdict
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        visited = [[0]*n for _ in range(m)]
        max_area = 0
        area_dict = defaultdict(int)
        label_max = 0

        def dfs(p, q, dict, label):
            nonlocal visited
            visited[p][q] = 1
            area_dict[label] += 1
            if p-1 >= 0 and visited[p-1][q] == 0 and grid[p-1][q] == 1:
                dfs(p-1, q, area_dict, label)
            if p+1 < m and visited[p+1][q] == 0 and grid[p+1][q] == 1:
                dfs(p+1, q, area_dict, label)
            if q-1 >= 0 and visited[p][q-1] == 0 and grid[p][q-1] == 1:
                dfs(p, q-1, area_dict, label)
            if q+1 < n and visited[p][q+1] == 0 and grid[p][q+1] == 1:
                dfs(p, q+1, area_dict, label) 
            
        for i in range(m):
            for j in range(n):
                if visited[i][j] == 0 and grid[i][j] == 1:
                    dfs(i, j, area_dict, label_max)
                    max_area = max(max_area, area_dict[label_max])
                    label_max += 1
                visited[i][j] = 1
        return max_area
```


## step3:

### code
```python
from collections import defaultdict
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        visited = [[0]*n for _ in range(m)]
        max_area = 0
        area_dict = defaultdict(int)
        max_label = 0

        def dfs(p, q, dict, label):
            visited[p][q] = 1
            dict[label] += 1
            if p-1 >= 0 and visited[p-1][q] == 0 and grid[p-1][q] == 1:
                dfs(p-1, q, dict, label)
            if p+1 < m and visited[p+1][q] == 0 and grid[p+1][q] == 1:
                dfs(p+1, q, dict, label)
            if q-1 >= 0 and visited[p][q-1] == 0 and grid[p][q-1] == 1:
                dfs(p, q-1, dict, label)
            if q+1 < n and visited[p][q+1] == 0 and grid[p][q+1] == 1:
                dfs(p, q+1, dict, label)
            
        for i in range(m):
            for j in range(n):
                if visited[i][j] == 0 and grid[i][j] == 1:
                    dfs(i, j, area_dict, max_label)
                    max_area = max(max_area, area_dict[max_label])
                    max_label += 1
                visited[i][j] = 1
        return max_area
```

## 他の方のコードを読んだ所感
https://github.com/hemispherium/LeetCode_Arai60/pull/18/changes
遷移先でgridの外に出てしまうか判断しているので、自分のコードのように何度もif文を書く必要がなくバグが出にくい。cppはintがimmutableでないのでそのままdfsの関数の引数に入れてインクリメントして大丈夫そうである。自分は今回visitedという配列を用いて訪問済みか判断していたが、この方はgridを0にしていて訪問済みのマークと同等の効果を出していて効果的だと感じた。

https://github.com/Manato110/LeetCode-arai60/pull/18/changes
この方はnum_rows, num_colsと名付けていたが問題文でm×nと定義されているのでm, nで定義した方が簡潔な気がする。あと関数をクラスの中の1つの関数としていたので、関数の中での関数として定義していた自分よりもテストがしやすい。
```python
if not (0 <= row < num_rows and 0 <= col < num_cols):
```
この条件式の書き方は参考にできる。0, 1は条件文でWATER, LANDとなっているが、この方はクラス内で改めてWATER = 0, LAND = 1と書いて条件式でself.WATERと書いているので非常に可読性が良い。visited判定もset()に訪れた座標を入れていて、setは確か内部的にハッシュテーブルを利用しているはずなのでO(1)でアクセスできる。よって自分の書いたvisited配列と同じメモリ計算量、時間計算量で利用できる。

## iterative dfsで解いてみた
```python
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        max_area = 0
        m, n = len(grid), len(grid[0])

        def get_area_starting_from(i, j):
            stack = []
            area = 0
            stack.append((i, j))
            while stack:
                y, x = stack.pop()
                if not (0 <= y < m and 0 <= x < n and grid[y][x]):
                    continue
                grid[y][x] = 0
                area += 1
                for col, row in [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]:
                    stack.append((col, row))
            return area

        for i in range(m):
            for j in range(n):
                if grid[i][j] == 1:
                    max_area = max(max_area, get_area_starting_from(i, j))
        
        return max_area
```

