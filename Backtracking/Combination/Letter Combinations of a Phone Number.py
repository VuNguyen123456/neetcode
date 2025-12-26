class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        n = len(digits)
        dic = {"2":"abc","3":"def","4":"ghi","5":"jkl","6":"mno","7":"pqrs","8":"tuv","9":"wxyz"}

        def dfs(i, curS):
            if len(curS) == n:
                res.append(curS)
                return
            # No need this because I will never become more than n due to the loop it cannot exceed n
            # if i > n:
            #     return
            # Go through each possible char of each letter in the number given
            # for each of then call the other number and all their posibility 
            for char in dic[digits[i]]:
                dfs(i + 1, curS + char) # Go to next letter and thorugh each posibility of that, also addd this curent one in
        
        if digits:
            dfs(0, "")
        return res
