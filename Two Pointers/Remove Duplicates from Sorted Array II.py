class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        secondedTime = False
        l = 1
        for r in range(1, len(nums)):
            if nums[r-1] != nums[r]:    
                nums[l] = nums[r]
                l += 1
                secondedTime = False
            elif nums[r-1] == nums[r] and secondedTime == False:
                nums[l] = nums[r]
                l += 1
                secondedTime = True
        return l
