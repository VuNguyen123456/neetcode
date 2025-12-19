class Solution:
    def numOfSubarrays(self, arr: List[int], k: int, threshold: int) -> int:
        totalSub = 0
        numSub = 0

        for i in range(len(arr)):
            if i < k:
                totalSub += arr[i]
                continue
            
            if totalSub/k >= threshold:
                numSub += 1
                print(totalSub)
            
            totalSub -= arr[i - k]
            totalSub += arr[i]

        if totalSub/k >= threshold:
                numSub += 1

        return numSub
