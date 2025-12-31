class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False

        if len(s1) < len(s2): 
            s1, s2 = s2, s1
        # Init last row (last ele is True because out of bound => form string of "" which always match "" of s3)
        dp = [False for i in range(len(s2) + 1)]
        dp[len(s2)] = True

        # not len(s1) - 1 because we also need to do the stuff for the out of bound too, so base case is not fixed here
        for i in range(len(s1), -1,-1): 
            nextDP = [False for i in range(len(s2) + 1)]
            # Handle base case on the right => Init it to true if this is the last row 
            #(due to dp and nextDP being the same at first) and we need to make sure when dp update to this cur one the bottom right is True
            if i == len(s1):
                nextDP[len(s2)] = True
            for j in range(len(s2), -1, -1):
                # If s1 match s3 => check directly bellow if true then it's true
                if i < len(s1) and s1[i] == s3[i+j] and dp[j]:
                    nextDP[j] = True
                # If s2 match s3 => check directly to the right if true then it's true
                if j < len(s2) and s2[j] == s3[i+j] and nextDP[j+1]:
                    nextDP[j] = True

            dp = nextDP 
        
        return dp[0]
