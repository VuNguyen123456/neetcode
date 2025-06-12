class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        result = []
        count = 0
        check = 1
        queue = deque()
        queue.append(root)
        
        while queue:
            lst = []
            for i in range(check):
                node = queue.popleft()
                lst.append(node.val)
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            result.append(lst)
            check = len(queue) # Always going to be the length of the next leveldue to queue now will only all node from that level 
        return result
