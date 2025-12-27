class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        # sum of input arr cannot be odd 
        # Because there wouldn't be anyway to divide into 2 equal sum arr
        if sum(nums) % 2 != 0:
            return False
        
        dp = set()
        dp.add(0)
        target = sum(nums) // 2
        for i in range(len(nums)-1,-1,-1):
            nextDP = set() # Can't loop through dp and adding stuff to it at the same time
            for t in dp:
                if (t + nums[i]) == target: # return true if target archived
                    return True
                nextDP.add(t + nums[i]) # Add the new element in 
                # But also don't want to lose stuff that's already in dp before so
                nextDP.add(t) # Add old value back in to not lose it !!
            dp = nextDP
        return False
