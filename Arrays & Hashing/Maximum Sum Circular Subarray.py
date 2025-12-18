class Solution:
    def maxSubarraySumCircular(self, nums: List[int]) -> int:
        globalMax, globalMin = nums[0], nums[0]
        curMax, curMin = 0,0
        total = 0
        for n in nums:
            curMax = max(curMax + n, n) # Handle when negative happend
            curMin = min(curMin + n, n) # Find the smallest subarray that's protentially in the middle to handle circular stuff
            total += n
            globalMax = max(globalMax, curMax)
            globalMin = min(globalMin, curMin)
        if globalMax < 0: # handle when array all negative because if that's the case the total - global min = 0 which is bigger than global max of a negative value
            return globalMax
        return max(globalMax, total - globalMin)
