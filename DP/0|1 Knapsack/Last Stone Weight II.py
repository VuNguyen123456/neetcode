class Solution:
    def lastStoneWeightII(self, stones: List[int]) -> int:
        # # Top down
        # stoneSum = sum(stones)
        # target = math.ceil(stoneSum / 2) # u want to ound up here

        # dp = {}

        # def dfs(i, total):
        #     if i == len(stones) or total >= target:
        #         return abs(total - (stoneSum - total)) # This is why we take the min between adding and not adding in the value 
        #         #because we want the smallest diff between
        #     if (i, total) in dp:
        #         return dp[i, total]
        #     # path 1: Include
        #     # path 2: Exclude 
        #     # Want to take the minimum of them
        #     dp[(i, total)] = min(dfs(i + 1, total + stones[i]), dfs(i + 1, total))

        #     return dp[(i, total)]
        # return dfs(0, 0)


        stoneSum = sum(stones)
        target = stoneSum // 2
        dp = [0] * (target + 1)

        for stone in stones:
            for t in range(target, stone - 1, -1):
                dp[t] = max(dp[t], dp[t - stone] + stone)

        return stoneSum - 2 * dp[target]
