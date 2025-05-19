class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        dic = {}
        lst = []
        for i in nums:
            if i in dic:
                dic[i] += 1
            else:
                dic[i] = 1
        for i in range(k):
            #find the key with the largest value in the dictionary, append it to the result list and mark the key as done
            val = max(dic, key=dic.get)
            lst.append(val)
            dic[val] = 0
        return lst
