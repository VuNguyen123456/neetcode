class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        length = len(prices)
        result = 0
        for i in range(length):
            biggestStock = 0
            check = 0
            for j in range(i+1, length):
                if prices[j] > prices[i] and biggestStock < prices[j]:
                    biggestStock = prices[j]
                    check = prices[j] - prices[i]
            if check > result:
                result = check

        return result
