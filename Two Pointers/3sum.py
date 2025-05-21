class Solution:
  def threeSum(self, nums: List[int]) -> List[List[int]]:
    length = len(nums)
    result = []
    nums.sort()
    for i in range(length):
      l = i + 1
      r = length - 1
      while l < r:
        if nums[i] + nums[l] + nums[r] > 0:
          r -= 1
          continue
        elif nums[i] + nums[l] + nums[r] < 0:
          l += 1
          continue
        elif [nums[i], nums[l], nums[r]] not in result:
          result.append([nums[i], nums[l], nums[r]])
        r -= 1
        l += 1
    return result
