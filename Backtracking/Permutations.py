class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        res = []
        n = len(nums)
        def backtrack(index):
            if n == index: # Compare index because if index = len(nums) => at the last possible element and ret
                res.append(nums[:])
                return

            for i in range(index , n):
                nums[i], nums[index] = nums[index], nums[i]
                backtrack(index + 1)
                nums[index], nums[i] = nums[i], nums[index]


        backtrack(0)
        return res

# permute([1,2,3])
# ├── pick 1 → permute([2,3])
# │   ├── pick 2 → permute([3]) → [3] → append 2 → [3,2]
# │   └── pick 3 → permute([2]) → [2] → append 3 → [2,3]
# │   → add 1 → [3,2,1], [2,3,1]
# ├── pick 2 → permute([1,3])
# │   → [3,1] → [3,1,2], [1,3,2]
# ├── pick 3 → permute([1,2])
# │   → [2,1], [1,2] → [2,1,3], [1,2,3]
