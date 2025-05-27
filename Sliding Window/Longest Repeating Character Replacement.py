class Solution:
  def characterReplacement(self, s: str, k: int) -> int:
    count = {}
    l = 0
    r = 0
    maxFrequency = 0
    result = 0
    for i in s:
      r += 1
      if i not in count:
        count[i] = 1
      else:
        count[i] += 1
      if count[i] > maxFrequency:
        maxFrequency = count[i]
      while (r-l) - maxFrequency > k:
        count[s[l]] -= 1
        l += 1
      if (r-l) > result:
        result = (r-l)
    return result
        
