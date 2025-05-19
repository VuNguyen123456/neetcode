class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        l = 0
        r = 1
        maxP = 0
        while r < len(prices):
            if prices[l] > prices[r]:
                l = r
                r = l + 1
            elif maxP < prices[r] - prices[l]:
                maxP = prices[r] - prices[l]
                r += 1
            else:
                r += 1
        return maxP
