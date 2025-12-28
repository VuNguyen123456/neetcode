class Solution:
    def findMaxForm(self, strs: List[str], m: int, n: int) -> int:
        # STEP 1:
        # count 0 and 1 for each string so: 10 became [1,1], 0001 = [3,1] 
        # arr = [[1,1],[3,1],[0,1]] So we can use it latter when processing
        arr = [[0,0] for _ in range(len(strs))]
        for i, s in enumerate(strs):
            for c in s:
                arr[i][ord(c) - ord('0')] += 1

        # STEP 2:
        # Init dp to all 0
        dp = [[0] * (n+1) for _ in range(m + 1)] # You want the 1st row and col to be all 0 as it need to handle the edge case of out of bound

        # STEP 3:
        # Steps through arr, each row and col bottom up and add in if that cell (budge) can handle the added element. 
        for zeros, ones in arr: # arr = [[1,1],[3,1],[0,1]]
            for j in range(m, zeros-1,-1): # Backward rows
                for k in range(n, ones - 1, -1): # Backward cols
                    dp[j][k] = max(dp[j][k], 1 + dp[j - zeros][k - ones]) # Stay as current budget or add one to diagonal left of it
        
        return dp[m][n]
        
