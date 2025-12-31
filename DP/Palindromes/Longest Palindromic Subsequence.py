class Solution:
    def longestPalindromeSubseq(self, s: str) -> int:
        # Going to do LCS on s and revert of S => always correct

        s2 = s[::-1]
        dp = [0 for i in range(len(s2) + 1)] # init to all 0 in last row
        
        for i in range(len(s)-1,-1,-1):
            nextDP = [0 for i in range(len(s2) + 1)]
            for j in range(len(s2)-1,-1,-1):
                if s[i] == s2[j]: # the 2 match.
                    #Add 1 diagonally
                    nextDP[j] = 1 + dp[j+1]
                else: # Look for max of bot or right
                    nextDP[j] = max(nextDP[j + 1], dp[j])
            dp = nextDP
        return dp[0]
