class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        # dp = [[0 for j in range(len(text2)+1)] for i in range(len(text1) + 1)] # Initialize a 2d grid with all 0 that's + 1 dimention bigger than normal
        
        # for i in range(len(text1)-1,-1,-1):
        #     for j in range(len(text2)-1,-1,-1):
        #         if text1[i] == text2[j]:
        #             dp[i][j] = 1 + dp[i+1][j+1] # = diagonal
        #         else:
        #             dp[i][j] = max(dp[i][j+1],dp[i+1][j])

        # return dp[0][0]

        if len(text1) < len(text2):
            text1, text2 = text2, text1
            
        dp = [0 for j in range(len(text2)+1)] # init dp as last row (not col) 
        # - in 2 grid term this is is always dp[i+1][....]

        # i is verical: dp is already i + 1 compare to nextDP
        # j is horizontal

        for i in range(len(text1)-1,-1,-1): # Go through each element in col
            nextDP = [0 for j in range(len(text2)+1)]
            for j in range(len(text2)-1,-1,-1): # Go through each element in current row
                if text1[i] == text2[j]:
                    # dp[i][j] = 1 + dp[i+1][j+1] # = diagonal
                    nextDP[j] = 1 + dp[j + 1]
                else:
                    # dp[i][j] = max(dp[i][j+1],dp[i+1][j])
                    nextDP[j] = max(dp[j], nextDP[j + 1]) # bellow and to the right
            dp = nextDP
        return dp[0]
