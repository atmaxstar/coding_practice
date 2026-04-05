step1:
まず順番にノードを探索していって、head.valがhead.next.valと一致していればそれは重複したノードなのでそれらが消えるまでheadを進めていく。もしhead.valがhead.next.valでなければそれはdistinctなので答えで返すnodeとして追加するという方針で行く。しかし返すべき値をresとしてどのようにres自身に代入するか迷ったので、get_distinct_listという帰納関数を作りボトムアップでdistinctな連結リストを得て返すという方法を取った。

step2:
get_distinct_listがやっていることとdeleteDuplicatesがやってることが同じだと気づいたのでdeleteDuplicates内でのget_distinct_listの宣言をやめてdeleteDuplicatesの帰納的呼び出しを行うことにした。

step3:
duplicateだった場合に最後head = head.nextとやってるがそのままhead.nextを代入すればいいと気づいたのでhead = head.nextを消した。

## step1:
まず順番にノードを探索していって、head.valがhead.next.valと一致していればそれは重複したノードなのでそれらが消えるまでheadを進めていく。もしhead.valがhead.next.valでなければそれはdistinctなので答えで返すnodeとして追加するという方針で行く。しかし返すべき値をresとしてどのようにres自身に代入するか迷ったので、get_distinct_listという帰納関数を作りボトムアップでdistinctな連結リストを得て返すという方法を取った。

### code
```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        def get_distinct_list(head_arg):
            if not head_arg or not head_arg.next:
                return head_arg
            if head_arg.val == head_arg.next.val:
                while head_arg.next and head_arg.val == head_arg.next.val:
                    head_arg = head_arg.next
                head_arg = head_arg.next
                return get_distinct_list(head_arg)
            
            head_arg.next = get_distinct_list(head_arg.next)
            return head_arg

        return get_distinct_list(head)
```

## step2:
get_distinct_listがやっていることとdeleteDuplicatesがやってることが同じだと気づいたのでdeleteDuplicates内でのget_distinct_listの宣言をやめてdeleteDuplicatesの帰納的呼び出しを行うことにした。

### code
```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:

        if not head or not head.next:
            return head

        if head.val == head.next.val:
            while head.next and head.val == head.next.val:
                head = head.next
            head = head.next
            return self.deleteDuplicates(head)
        
        head.next = self.deleteDuplicates(head.next)
        return head

```


## step3:
duplicateだった場合に最後head = head.nextとやってるがそのままhead.nextを代入すればいいと気づいたのでhead = head.nextを消した。

### code
```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if not head or not head.next:
            return head
        
        if head.val == head.next.val:
            while head.next and head.val == head.next.val:
                head = head.next
            return self.deleteDuplicates(head.next)
        
        head.next = self.deleteDuplicates(head.next)
        return head

```