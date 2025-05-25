class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        window = set()
        longestSetLength = 0
        l = 0
        for i in s:
            while i in window:
                window.remove(s[l])
                l += 1
            window.add(i)
            longestSetLength = max(longestSetLength, len(window))
        return longestSetLength
