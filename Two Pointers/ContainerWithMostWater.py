class Solution:
    def maxArea(self, heights: List[int]) -> int:
      l = 0
      r = len(heights) - 1
      maxW = 0
      while l <= r:
        shorterW = min(heights[l], heights[r])
        maxW = max(maxW, shorterW*(r-l))
        if shorterW == heights[l]:
          l += 1
        elif shorterW == heights[r]:
          r -= 1
      return maxW
