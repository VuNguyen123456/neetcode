class Solution:
    def containsNearbyDuplicate(self, nums: List[int], k: int) -> bool:
        # if k == 0:
        #     return False
        window = set()
        for i in range(len(nums)):
            if len(window) >= k+1:
                window.remove(nums[i-k-1])
            if nums[i] in window:
                return True
            window.add(nums[i])
        return False
