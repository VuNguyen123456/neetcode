class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp = defaultdict(int) # current row we'll use
        dp[0] = 1

        for i in range(len(nums)):
            nextDP = defaultdict(int) # next row we'll modify into using after this loop
            for curSum, count in dp.items(): # Look though current row, with sum and way to reach that sum
                # Update next row
                nextDP[curSum + nums[i]] += count
                nextDP[curSum - nums[i]] += count
            dp = nextDP # Current dp update into next dp and we go to the next cycle using the new DP
        
        return dp[target] # We'll get the total way of getting into this target # We compute a bunch of way to get to a bunch of others number too but only want the target
