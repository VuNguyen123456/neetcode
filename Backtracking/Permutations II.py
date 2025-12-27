class Solution:
    def permuteUnique(self, nums: List[int]) -> List[List[int]]:
        res = []
        n = len(nums)
        nums.sort()
        def backtrack(index):
            if index == n:
                res.append(nums[:])
                return
            for i in range(index, n):
                # Before swapping, check if nums[i] has been used already at position index (you can use a set if you want)
                if i > index and nums[i] == nums[index]: # Only check when i >index because i == index the 1st time
                    continue  # ← Already tried this value!

                nums[i], nums[index] = nums[index], nums[i]
                backtrack(index + 1)
                # No immediate sawp back be cause we want to use the messed up index version consistenly in all of this loop to check for dup
            # only clean up after!
            for i in range(len(nums) - 1, index, -1):
                nums[index], nums[i] = nums[i], nums[index]
            
        backtrack(0)
        return res
