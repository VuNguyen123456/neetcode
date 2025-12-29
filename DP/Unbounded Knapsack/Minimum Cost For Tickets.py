class Solution:
    def mincostTickets(self, days: List[int], costs: List[int]) -> int:
        dp = [0] * (len(days) + 1)
        for i in range(len(days)-1,-1,-1):
            j = i
            dp[i] = float("inf") # Try yo find min
            for cost, duration in zip(costs, [1,7,30]):
                while j < len(days) and days[j] < days[i] + duration:
                    j += 1
                dp[i] = min(dp[i], cost + dp[j]) # dp[j] is already assigned, remembered bc this is dp
        
        return dp[0]
