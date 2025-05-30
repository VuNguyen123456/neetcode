class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        nums.sort()
        print(nums)
        for i in range(len(nums) - 1):
            # it's sorted so the same one will stand next to each other!!!
            if nums[i] == nums[i+1]:
                return nums[i]
        return -1
