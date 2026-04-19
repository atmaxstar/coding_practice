
## step1:
これはbeginWordから文字の距離が小さい順から広さ優先探索した方がいいと思い、queueを使った。beginWordから始まり、すでに訪れていない&文字の距離が1であるものをqueueにプッシュしていき、もしendWordに一致するものが来たらそこが答えの距離である。最初queueでpop, appendしてれば勝手にキューの動作をすると思っていたがエラーが出てpopleftを使わなければならないことを知った。

### code
```python
from collections import deque
class Solution:
    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        q = deque()
        q.append([beginWord, 1])
        visited = set()
        visited.add(beginWord)

        def is_diff_one(word1, word2):
            if not len(word1) == len(word2):
                return False
            diff = 0
            for i in range(len(word1)):
                if word1[i] != word2[i]:
                    diff += 1
            return diff == 1
        
        while q:
            current, distance = q.popleft()
            for word in wordList:
                if not word in visited and is_diff_one(current, word):
                    if word == endWord:
                        return distance+1
                    visited.add(word)
                    q.append([word, distance+1])
        
        return 0
```

## step2:
leetcode上で実行速度が速い人のコードを見てみると"abcde..."各アルファベットをqueueでpopした文字のi番目にそれぞれ代入して、、wordList->set(wordList)にそれぞれが入っているかで判別していた。こうすると元々自分のコードでO(N*L, Nはlen(wordList), Lはwordの長さ)だったのが、O(26*L)とNのサイズが大きい場合に非常に有効な方法となっていた。なので一旦それで実装してみた。けど初見で解く場合は、step1でのコードを書いて面接官からもう少し早くできるか言われた場合にstep2のコードを書くのが自然ではないかと感じる。

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
            current, distance = q.popleft()
            for i in range(len(current)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    nextWord = current[:i] + c + current[i+1:]
                    if nextWord in wordSet and nextWord not in visited:
                        if nextWord == endWord:
                            return distance+1
                        visited.add(nextWord)
                        q.append([nextWord, distance+1])
        return 0
```


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