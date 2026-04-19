
## step1:
これは二分探索で解いてもしnums[mid] == targetが見つかったらreturn midをすれば良い問題だと思ったが、せっかくなのでbisectのbisect_leftと同じ感じでtargetが複数個numsに存在する場合は一番左のところのインデックスを返す実装をするようにした。しかし、一旦この実装をしたもののtargetより小さい値のみのnumsに対して実行すると一番左のインデックスを返してしまう。
例；nums=[1,2,3,4], target=8の時に答えは4なのに3を返してしまう。
### code
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums) - 1
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid

        return left
```
実際にmidの流れを追っていくとleft == rightとなったときに終了してしまうがもしそこでもう一回ループが回るとleft = mid + 1となって目当てのインデックスへ行く。そこでwhile left <= rightにしてみたが普通にTime Limit Exceedとなってしまった。完全に行き詰まったのでbisect_leftの実装をClaudeに書いてもらう。そしたらなんとrightをlen(nums)から始めていた。割と直感から反している。
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid

        return right
```

## step2:
現在の形が一番綺麗だと感じるのでそのまま書く。
### code
```python
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            mid = (left + right) // 2
            if nums[mid] < target:
                left = mid + 1
            else:
                right = mid

        return right
```
正直全然理解できてないのでこちらのリンクを読んで自分なりに整理してみる。
https://github.com/Yoshiki-Iwasa/Arai60/pull/35#discussion_r1699552857
left, rightに対してleftを閉区間、rightを開区間とすると初期地点はleft=0, right=len(nums)となる。もしbisect_leftを求めたいのなら最終地点は[False, False, [)True, True]こうなっていてleftのインデックスを返せば良い。そのためwhile文はleft < rightにしてleftがtargetの値を超えないようにnums[mid] < targetの際はleft=mid+1へ、nums[mid] >= targetの際はright=midとなる。bisect_rightの場合は[False, False, True, True,[)False]これが最終地点で、となるとnums[mid]<=targetの場合にleft=mid+1, それ以外の場合はright=midで更新すると求まる。

↑から数日経ってまた解いてみたのだが、やはりいちいち考えてみたものの普通にミスしてわからなくなった。Claudeがテンプレートを覚えるのが一番良いといってくれたので、以下のテンプレートを覚えてみる。
### テンプレート選択（これだけ自問する）

> 「特定の値を見つけるか？」「境界 / 挿入位置を見つけるか？」

| 目的 | テンプレート | right | 条件式 | mid 更新 |
|------|------------|-------|--------|---------|
| 値の存在確認・取得 | ① 完全一致 | `len - 1` | `left <= right` | `mid + 1` / `mid - 1` |
| 最初 / 最後の境界・挿入位置 | ② 境界探索 | `len` | `left < right` | `left = mid + 1` / `right = mid` |

---

### 3つの変数の意味

**`right` — 探索空間の右端**
- `len - 1` → 最後の index も探索対象（範囲内）
- `len` → 番兵として「範囲外」を表す（全要素が条件を満たさないとき答えが len になりうる）

**条件式 — ループを続ける条件**
- `left <= right` → `left == right` でも 1 要素を確認してから終わる
- `left < right` → `left == right` になった瞬間が「境界が決まった」状態

**`mid` 更新 — 探索範囲をどう狭めるか**
- `mid + 1` / `mid - 1` → mid を除外（mid は答えでないと確定したとき）
- `right = mid` → mid を含めたまま狭める（mid が答えの候補かもしれないとき）

## step3:

### code
```python
from collections import deque
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        q = deque()
        q.append([beginWord, 1])
        visited = set()
        visited.add(beginWord)
        wordSet = set(wordList)

        while q:
            currentWord, distance = q.popleft()
            for i in range(len(currentWord)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nextWord = currentWord[:i] + c + currentWord[i+1:]
                    if nextWord not in visited and nextWord in wordSet:
                        visited.add(nextWord)
                        if nextWord == endWord:
                            return distance + 1
                        q.append([nextWord, distance + 1])
        
        return 0
```

## 他の方のコードを読んだ所感
https://github.com/hemispherium/LeetCode_Arai60/pull/19/changes/efa4e350aa9dd9220904e7b708ad2fac2c560209
step1にてqueueから出したwordをtempと名づけていてぱっと見これが何を意味しているのかわかりづらくなる原因となると思ったのでcurrentWordとかにした方が良いと感じた。この方は最初にendWordがwordListに存在するか判定しているが、私の方では確認していないのでif文の中にif文を書くネスト構造となってしまった。wordSetから訪問済みの値を消すことでvisitedと同等の働きをしているが、個人的には可読性が低くなってしまうのではと感じた。

https://github.com/Manato110/LeetCode-arai60/pull/19/changes
この方の最初に書いたコードはそれぞれのwordの差分を
```python
diff_count = sum(1 for a, b in zip(target_word, word) if a != b)
```
このように表現していてぱっと見わかりづらい。無理に1行にせずにfor文から始めた方が可読性が良いと思う。あとqueueとあるのにset()を使用している点がある。この最初のコードがacceptされない理由としてはendWordがwordListにない場合と、endWordに辿り着かない場合が考慮されていないからである。