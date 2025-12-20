class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l = 1
        for r in range(1, len(nums)):
            if nums[r] != nums[r-1]: # if no duplicate move forward
                nums[l] = nums[r] # This is so that ultimately in the end the array will the no duplicate at least in the front 
                l += 1
        return l
