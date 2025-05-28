class Solution:
  def minEatingSpeed(self, piles: List[int], h: int) -> int:
    biggestP = max(piles)
    l = 1
    r = biggestP
    result = r
    while l <= r:
      m = l+(r-l)//2
      totalTime = 0
      for i in piles:
        totalTime += math.ceil(i/m)
      if totalTime <= h:
        result = min(result, m)
        r = m-1
      else: 
        l = m+1
    return result
