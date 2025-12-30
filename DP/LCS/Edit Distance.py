class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        if len(word1) < len(word2):
            word1, word2 = word2, word1
        # Last row initialization
        dp = [0 for i in range(len(word2) + 1)] # Init to all infinity
        for i in range(len(word2) + 1):
            dp[i] = len(word2) - i

        for i in range(len(word1) -1, -1, -1):
            nextDP = [0 for i in range(len(word2) + 1)]
            nextDP[len(word2)] = len(word1) - i 
            for j in range(len(word2)-1, -1, -1):
                if word1[i] == word2[j]:
                    nextDP[j] = dp[j + 1] # Diagonal
                else:
                    # 1 + minimum of right or down or diagonal
                    nextDP[j] = 1 + min(nextDP[j + 1], dp[j], dp[j + 1])
            dp = nextDP

        return dp[0]
