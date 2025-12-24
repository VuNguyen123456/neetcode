# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        lst = []
        def dfs(node, path):
            if node is None:
                return None
            
            dfs(node.left,path)
            dfs(node.right,path)
            path.append(node.val)

        dfs(root, lst)
        return lst
