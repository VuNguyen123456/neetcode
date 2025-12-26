class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        res = []
        combi = []

        def dfs(j, curSum):
            if curSum == target: # Base case of returning nothing because this number is wrong
                res.append(combi.copy())
                return
            for i in range(j, len(candidates)):
                if curSum + candidates[i] > target:
                    # return is wrong because we want to keep going and check not exist the entire path if 1 of them is wrong
                    continue
                combi.append(candidates[i])
                dfs(i, curSum + candidates[i]) # i here because it's allow to use the same element 
                combi.pop() # backtracking
        
        dfs(0, 0)
        return res
