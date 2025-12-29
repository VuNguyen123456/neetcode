class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        # dp = [0] * (amount + 1)
        # dp[0] = 1
        # for i in range(len(coins) -1,-1,-1 ):
        #     nextDP = [0] * (amount + 1)
        #     nextDP[0] = 1
        #     for a in range(1, amount + 1):
        #         nextDP[a] = dp[a] # add directly bellow # unless 1st row then the 2 dp are the same and only look the right
        #         if a - coins[i] >= 0: # Not out of bound
        #             nextDP[a] += nextDP[a - coins[i]]
        #     dp = nextDP # change to next row to continue process next time # dp always behind nextDP
        # return dp[amount]

        dp = [0] * (amount + 1)
        dp[amount] = 1
        for i in range(len(coins) -1,-1,-1 ):
            nextDP = [0] * (amount + 1)
            nextDP[amount] = 1
            for a in range(amount - 1, -1, -1):
                nextDP[a] = dp[a] # add directly bellow # unless 1st row then the 2 dp are the same and only look the right
                if a + coins[i] <= amount: # Not out of bound
                    nextDP[a] += nextDP[a + coins[i]]
            dp = nextDP # change to next row to continue process next time # dp always behind nextDP
        return dp[0]
