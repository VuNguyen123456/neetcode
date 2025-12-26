class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        # result = []
        # candidates.sort()
        # def dfs(i , curList, total):
        #     if total == target:
        #         result.append(curList.copy())
        #         return
        #     if total > target or i >= len(candidates):
        #         return
        #     curList.append(candidates[i])
        #     dfs(i + 1, curList, total + candidates[i])
        #     curList.pop()
        #     while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]:
        #         i += 1
        #     dfs(i+1,curList, total)
        # dfs(0, [], 0)
        # return result

        res = []
        combi = []
        candidates.sort()
        def dfs(i, curSum):
            if curSum == target: # Base case of returning nothing because this number is wrong
                res.append(combi.copy())
                return
            if i >= len(candidates) or curSum + candidates[i] > target:
                # return is wrong because we want to keep going and check not exist the entire path if 1 of them is wrong
                return

            # path 1: Include
            combi.append(candidates[i])
            dfs(i+1, curSum + candidates[i]) # i here because it's allow to use the same element 
            combi.pop() # backtracking

            # This part will skip repeated element because we don't allow duplicate
            # The second dfs is the exclude branch
            while i + 1 < len(candidates) and candidates[i] == candidates[i + 1]:
                i += 1
            dfs(i+1, curSum)
        
        dfs(0, 0)
        return res
