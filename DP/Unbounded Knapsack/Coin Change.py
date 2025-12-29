class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount + 1] * (amount + 1) # dp[0.......amount] => check each one up until amount
        dp[0] = 0
        for i in range(1, amount+1): # Skipping base case and up until amount
            for coin in coins:
                if i >= coin:
                    dp[i] = min(dp[i], 1 + dp[i - coin]) # This work on if i == coin because dp[i-coint] will be 0 which is a base case set to 0 => it's 1 + 0 = 1
        return dp[amount] if dp[amount] != amount + 1 else - 1
