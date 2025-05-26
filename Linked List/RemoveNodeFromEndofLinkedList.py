# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def removeNthFromEnd(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        checkLength = head
        length = 0

        while checkLength != None:
            checkLength = checkLength.next
            length += 1

        rmIndex = length -n
        curr = head
        prev = None
        for i in range(rmIndex):
            prev = curr
            curr = curr.next
        if prev is not None:
            prev.next = curr.next
            curr.next = None
        else:
            # if the head need to be remove
            head = curr.next
            curr.next = None
        return head
