# class Solution:
#     def goodNodes(self, root: TreeNode) -> int:
#         def dfs(node, maxVal): 
#             result = 0
#             if not node:
#                 return 0
#             if node.val >= maxVal:
#                 result += 1
#             maxVal = max(maxVal, node.val)
#             result += dfs(node.left, maxVal)
#             result += dfs(node.right, maxVal)
#             return result
#         return dfs(root, root.val)

class Solution:
    def goodNodes(self, root: TreeNode) -> int:
        result = 0
        q = deque()
        q.append((root,-float('inf')))
        while q:
            node, maxVal = q.popleft()
            if node.val >= maxVal:
                result += 1
            if node.left:
                q.append([node.left, max(maxVal, node.val)])
            if node.right:
                q.append([node.right, max(maxVal, node.val)])
        return result
