class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        dic = {0 : 1}
        res = 0
        prefix = 0
        for i in range(len(nums)):
            prefix += nums[i]
            target = prefix - k
            if target in dic:
                res += dic[target]
                print(i)
            if prefix in dic:
                dic[prefix] += 1
            else:
                dic[prefix] = 1
        return res
