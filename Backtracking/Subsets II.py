class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        res = []
        curSubset = []
        nums.sort() # Because the aray is not unique anymore
        def dfs(i):
            if i >= len(nums): # We are at leaf
                res.append(curSubset.copy()) # just how list work in this situation
                return
            # Path 1 to add in (left side)
            curSubset.append(nums[i])

            # print(i)
            dfs(i + 1)
            
            curSubset.pop() # Rest so that the next path can be like add nothing 
            #because we just add somehtig so now remove it to seems like we add n othing

            # Path 2
            # Only skip here because one 1 INCLUDE or EXCLUDE BRACNH can skip without result in missing so this one skip
            while i + 1 < len(nums) and nums[i] == nums[i+1]: # if the next one is exactly the same as the previous one we skip because that would cause
                i += 1
            dfs(i+1)
            
        dfs(0)
        return res
