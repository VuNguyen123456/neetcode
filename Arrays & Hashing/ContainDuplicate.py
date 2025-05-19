class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        lst = []
        for i in range(len(nums)):
            if nums[i] in lst:
                return True
            else:
                lst.append(nums[i])
        return False
