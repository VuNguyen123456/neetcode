class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        windowSize = len(s1)
        l = 0
        r = windowSize - 1
        compareWith = sorted(s1)
        while r < len(s2):
            if compareWith == sorted(s2[l:r+1]):
                return True
            l += 1
            r += 1
        return False
