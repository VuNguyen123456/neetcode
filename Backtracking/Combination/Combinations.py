class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []
        combi = []
        def dfs(i):
             # Base case so that I cannot be number that's bigger than n
            if len(combi) == k: # So that all subset must be of length k not higher or lower
                res.append(combi.copy())
                return
            if i > n:
                return
                
           
            # The rest is similar to all possible combination problem
            # Path 1: Include
            combi.append(i)
            dfs(i + 1)
            combi.pop() # backtrack so exclude path include nothing new

            # Path 2: Exclude
            dfs(i + 1)
        
        dfs(1)
        return res
