# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def pairSum(self, head: Optional[ListNode]) -> int:
        slow, fast = head, head
        p1 = head 
        # find middle point
        while fast and fast.next:
            slow = slow.next # ended up as head of 2nd half
            fast = fast.next.next

        # reverse 2nd half of linked list:
        p2 = None
        cur = slow
        while cur:
            temp = cur
            cur = cur.next # Null at the end
            temp.next = p2
            p2 = temp # Head of 2nd LL at the end
        
        #compare sum
        res = 0
        while p2:
            res = max(res, p1.val + p2.val)
            p2 = p2.next
            p1 = p1.next
        return  res
