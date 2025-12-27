class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        # Go through and count each color:
        reds = 0
        whites = 0
        # blues = 0

        for i in nums:
            if i == 0:
                reds += 1
            elif i == 1:
                whites += 1
            # elif i == 2:
            #     blues += 1
        
        for i in range(len(nums)):
            if reds != 0:
                nums[i] = 0
                reds -= 1
            elif whites != 0:
                nums[i] = 1
                whites -= 1
            else:
                nums[i] = 2
