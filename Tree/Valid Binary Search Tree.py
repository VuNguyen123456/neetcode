####################################### BFS #######################################
class Solution:
  def isValidBST(self, root: Optional[TreeNode]) -> bool:
    q = deque()
    # val, lower bound, upperbound
    q.append([root, float("-inf"), float("inf")])
    while q:
      node, lower, upper = q.popleft()
      if not (lower < node.val < upper):
        return False
      if node.left:
        # if left, then lower bound is parent lower bound, upperbound is node.val
        q.append(node.left, lower, node.val)
      if node.right:
        # if node right, lower bound is node.val, upperbound is parent upperbound
        q.append(node.right, node.val, upper)
    return True

####################################### DFS #######################################
class Solution:
  def isValidBST(self, root: Optional[TreeNode]) -> bool:
    def dfs(node, lower, upper):
      # if root empty or left/right of leaves node
      if not node:
        return True
      if not (lower < node.val < upper):
        return False
      return dfs(node.left, lower, node.val) and dfs(node.right, node.val, upper)
    return dfs(root, float("-inf"), float("inf"))
