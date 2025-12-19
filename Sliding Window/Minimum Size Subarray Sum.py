class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        n = len(nums)
        curSum = 0
        curLen = 0
        minLen = float('inf')
        headOfArr = 0

        for i in range(n):
            curSum += nums[i]
            curLen += 1
            while(curSum >= target):
                minLen = min(minLen, curLen)
                curSum -= nums[headOfArr]
                headOfArr += 1
                curLen -= 1

        if minLen == float('inf'):
            return 0

        return minLen                
