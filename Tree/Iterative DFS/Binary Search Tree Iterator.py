# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class BSTIterator:
    # The making in order list and just have an index way
    # On time to make, O1 next and has next
    # On space
    def __init__(self, root: Optional[TreeNode]):
        self.arr = []
        self.itr = 0
        def dfs(node):
            if node is None:
                return None
            dfs(node.left)
            self.arr.append(node.val)
            dfs(node.right)
        dfs(root)

    def next(self) -> int:
        val = self.arr[self.itr] # in case last element
        self.itr += 1
        return val


    def hasNext(self) -> bool:
        # if self.itr < len(self.arr):
        #     return True
        # return False
        return self.itr < len(self.arr) # index is buffered up once because next of itr 0 is the 1st ele not the 2nd


    # The iterative DFS way
    # O1 average on next and hasnext (trade of time for mem)
    # Oh (height) on memory storing
    def __init__(self, root: Optional[TreeNode]):
        self.stack = []
        # first initilization (add everything in deep left (and itself))
        cur = root
        while cur:
            self.stack.append(cur)
            cur = cur.left

    def next(self) -> int:
        # pop node to return the next (node - 1st next return 1st one not second one so we start 1 step before start line)
        node = self.stack.pop()
        # Check right of it if itexist then you go into deep left and add in stack. 
        # Only need to check right because be previously before this go deep left so there's no way for anyleft to remain
        cur = node.right # Could be None athen nothing will even be execute
        while cur: # As long as left of that right node exist you go deep
            self.stack.append(cur) # 1st node append his time is that right node you just discover 
            cur = cur.left
        return node.val
    def hasNext(self) -> bool:
        if self.stack != []: # if it's not empty then there's a next
            return True
        return False

# Your BSTIterator object will be instantiated and called as such:
# obj = BSTIterator(root)
# param_1 = obj.next()
# param_2 = obj.hasNext()
