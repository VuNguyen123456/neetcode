class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
        queue = deque()
        queue.append(root)
        result = []
        check = 1
        while queue:
            if queue:
                result.append(queue[-1].val)
            for i in range(check):
                node = queue.popleft()
                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)
            check = len(queue)
        return result
