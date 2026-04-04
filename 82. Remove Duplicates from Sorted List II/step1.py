# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
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