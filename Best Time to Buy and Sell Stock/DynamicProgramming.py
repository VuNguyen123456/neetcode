class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxP = 0
        minBuy = prices[0]
        for sell in prices:
            maxP = max(maxP, sell - minBuy)
            minBuy = min(sell, minBuy) # sell will always be afterminBuy in the array of stock
        return maxP
