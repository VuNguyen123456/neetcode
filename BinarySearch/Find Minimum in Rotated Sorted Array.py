class Solution:
  def findMin(self, nums: List[int]) -> int:
    l = 0
    r = len(nums) - 1
    result = nums[0]
    while l <= r:
      m = l + (r-l)//2
      if nums[l] < nums[r]: #if it's sorted => done now
        result = min(result, nums[l])
        break
      result = min(result, nums[m])
      if nums[m] < nums[l]:
        r = m -1
      else:
        l += 1
    return result
