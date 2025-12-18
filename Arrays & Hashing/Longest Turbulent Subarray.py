class Solution:
    def maxTurbulenceSize(self, arr: List[int]) -> int:
        longest = 1
        currLen = 1
        currSign = None # True means i-1 > i
        i = 1

        while i < len(arr):
            if arr[i-1] > arr[i] and currSign != True: # want to flip
                currSign = True
                currLen += 1
                # print(arr[i-1])
            elif arr[i-1] < arr[i] and currSign != False:
                currSign = False
                currLen += 1
                # print(arr[i-1])
            elif arr[i-1] == arr[i]:
                currSign = None
                currLen = 1
            else:
                currSign = None
                currLen = 1
                i -= 1
                # print("reset")
            longest = max(longest, currLen)
            i += 1
        
        return longest
