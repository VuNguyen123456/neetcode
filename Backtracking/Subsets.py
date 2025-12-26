class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res = []
        curSubset = []
        def dfs(i):
            if i >= len(nums): # We are at leaf
                res.append(curSubset.copy()) # just how list work in this situation
                return
            # Path 1 to add in (left side)
            curSubset.append(nums[i])
            dfs(i+1)
            curSubset.pop() # Rest so that the next path can be like add nothing 
            #because we just add somehtig so now remove it to seems like we add n othing

            # Path 2
            dfs(i+1)
            
        dfs(0)
        return res
