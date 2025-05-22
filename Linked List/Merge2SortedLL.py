class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        head = ListNode()
        if list1 and list2:
            if list1.val < list2.val:
                head = list1
                list1 = list1.next
            else:
                head = list2
                list2 = list2.next
        else:
            if list1:
                return list1
            elif list2:
                return list2
            else:
                return None
        curr = head
        while list1 and list2: #is not empty
            if list1.val < list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next
            # 1 of the list will be empty after the loop and left out something so this is to handle it
            curr = curr.next
        if list1:
            curr.next = list1
        elif list2:
            curr.next = list2
        return head
