class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        sumArr = 0
        maxSub = nums[0]
        for i in range(len(nums)):
            if sumArr < 0:
                sumArr = 0
            sumArr += nums[i]
            maxSub = max(sumArr, maxSub)
        return maxSub
