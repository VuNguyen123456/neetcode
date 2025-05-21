class Solution:
    def isPalindrome(self, s: str) -> bool:
        l = 0
        r = len(s)-1
        while l < r:
            # If left side is not a num skip the char
            if s[l].isalnum() == False:
                l += 1
                continue
            # If right side is not a num skip the char
            if s[r].isalnum() == False:
                r -= 1
                continue
            # If left side and right side differ => it's not palin => false
            if s[l].lower() != s[r].lower():
                return False
            # move closer
            l+= 1
            r -= 1
        return True
