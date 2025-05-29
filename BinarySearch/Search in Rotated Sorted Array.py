class Solution:
  def search(self, nums: List[int], target: int) -> int:
    l = 0
    r = len(nums) - 1
    chosenIn = 0
    while l <= r:
      m = l + (r-l)//2
      if nums[l] < nums[r]: #if it's sorted => done now
        if nums[chosenIn] > nums[l]:
          chosenIn = l
          break
      if nums[chosenIn] > nums[m]:
          chosenIn = m
      if nums[m] < nums[l]:
        r = m -1
      else:
        l += 1

    print(chosenIn)
    if chosenIn == 0:
      l = 0
      r = len(nums) - 1
    elif target > nums[len(nums) - 1]:
      l = 0
      r = chosenIn - 1
    else:
      l = chosenIn
      r = len(nums) - 1
    while l <= r:
      m = l + (r-l)//2
      print(m)
      if nums[m] == target:
        return m
      if nums[m] > target:
        r = m-1
      else:
        l = m+1
    return -1
