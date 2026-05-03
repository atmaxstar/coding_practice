
## step1:
nのParenthesesをn-1のParenthesesから生成するとなったとき、n-1での各文字列に対して左から右へ()を挿入していく場所を探していくと、
"("に当たった時はその"("を"()"で囲むか、"()("のように左に添える2パターンがあり、")"に当たった時は"())"のように置くパターンがあり、""に当たった時はそこに"()"をおけば良い。それを素直にコードにすると以下のようになる。
### code
```python
class Solution:
    # when facing (, put () or surround the ( with ()
    # when facing ), put () before )
    # when facing "", put ()
    def generateParenthesis(self, n: int) -> List[str]:
        answer = []
        def backtrack(parenthesis, m):
            if m == 0:
                return parenthesis
            next_parenthesis = set()
            for parenthe in parenthesis:
                for i in range(len(parenthe)+1):
                    if i < len(parenthe) and parenthe[i] == "(":
                        next_parenthesis.add(parenthe[:i] + "()" + parenthe[i:])
                        index_to_insert_closing = i + find_index_of_corresponding_symbol(parenthe[i:])
                        next_parenthesis.add(parenthe[:i] + "(" + parenthe[i:index_to_insert_closing] + ")" + parenthe[index_to_insert_closing:])
                    else:
                        next_parenthesis.add(parenthe[:i] + "()" + parenthe[i:])
            return backtrack(next_parenthesis, m - 1)

        def find_index_of_corresponding_symbol(part):
            opening = 0
            closing = 0
            for i in range(len(part)):
                if part[i] == "(":
                    opening += 1
                else:
                    closing += 1
                if opening == closing:
                    return i
            return -1
        
        return list(backtrack([""], n))
```
これでacceptされたが、geminiに読ませてみると以下の問題を言われた。
## 非効率な全探索（Setによる管理）
今のコードは、各ステップで「既存の文字列の全箇所に () を入れる」という操作を繰り返しています。これは計算量が非常に多くなり、n が大きくなると set への追加と文字列操作でパフォーマンスが劇的に悪化します。

## 「バックトラック」の一般的な解法との違い
通常、この問題（LeetCode 22. Generate Parentheses）をバックトラックで解く場合、**「空の状態から1文字ずつ ( か ) を足していく」**という手法をとります。

なのでこれをヒントに一回1から書いてみる。まず作りたいparenthesesは2*nの長さあり、それぞれに対してnこの(とnこの)をそれぞれ挿入していく。ここでwell-formedにするにはすでに(を配置した数分より大きい)を途中で置いてはいけない。この(と)の配置を全探索していくと答えにつながる。backtrackでも解けるがちょっと捻ってstackを使ったdfsで解いてみる。

```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        answer = []
        parentheses_and_open_and_close = []
        parentheses_and_open_and_close.append(["", n, n])
        while parentheses_and_open_and_close:
            parentheses, open_num, close_num = parentheses_and_open_and_close.pop()
            if open_num == close_num == 0:
                answer.append(parentheses)
                continue
            if open_num > 0:
                parentheses_and_open_and_close.append([parentheses + "(", open_num - 1, close_num])
            if close_num > 0 and close_num > open_num:
                parentheses_and_open_and_close.append([parentheses + ")", open_num, close_num - 1])
        return answer
```
これだと(と)に対してそれぞれの文字位置に対して置く、置かないを羅派しているのでset()で重複を省く必要がない。

## step2:
### code
```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        answer = []
        parentheses_and_open_and_close = []
        parentheses_and_open_and_close.append(["", n, n])
        while parentheses_and_open_and_close:
            parentheses, open_num, close_num = parentheses_and_open_and_close.pop()
            if open_num == close_num == 0:
                answer.append(parentheses)
                continue
            if open_num > 0:
                parentheses_and_open_and_close.append([parentheses + "(", open_num - 1, close_num])
            if close_num > 0 and close_num > open_num:
                parentheses_and_open_and_close.append([parentheses + ")", open_num, close_num - 1])
        return answer
```

## step3:
どうせなのでbacktrack, bfsで解いてみる。
### code
```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        answer = []

        def backtrack(parentheses, open_num, close_num):
            if open_num == close_num == 0:
                answer.append(parentheses)
            if open_num > 0:
                backtrack(parentheses + "(", open_num - 1, close_num)
            if close_num > 0 and close_num > open_num:
                backtrack(parentheses + ")", open_num, close_num - 1)
        
        backtrack("", n, n)
        return answer
```

```python
from collections import deque
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        answer = []
        parentheses_open_close = deque()
        parentheses_open_close.append(["", n, n])

        while parentheses_open_close:
            parentheses, open_num, close_num = parentheses_open_close.popleft()
            if open_num == close_num == 0:
                answer.append(parentheses)
                continue
            if open_num > 0:
                parentheses_open_close.append([parentheses + "(", open_num - 1, close_num])
            if close_num > 0 and open_num < close_num:
                parentheses_open_close.append([parentheses + ")", open_num, close_num - 1])
        
        return answer
```
