class Solution:
    def pivotIndex(self, nums: List[int]) -> int:
        # # NONE OPTIMAL: NO NEED TO PREP IT BEFORE AND STORE IT CAN JUST DO IT ON THE GOOOOOOOOOOOOOOOOOOO
        # pivot = -1
        # prefixSumArr = [0] # 1t index is 0, last index is also 0
        # temp = 0
        # # Prep prefix sum
        # for i in range(len(nums)):
        #     temp += nums[i]
        #     prefixSumArr.append(temp)     

        # prefixSumArr.append(0) #last index is also 0
        # print(prefixSumArr)
        # # Find pivot:
        # for i in range(1, len(nums)+1):
        #     if prefixSumArr[i-1] == prefixSumArr[-2] - prefixSumArr[i]: #prefixSum array has 0 on head and tail for edge case so need to + 1
        #         pivot = i-1
        #         break
        # return pivot

        sumArr = sum(nums)
        leftSum = 0
        for i in range(len(nums)):
            rightSum = sumArr - (leftSum + nums[i]) # right side sum = total sum - to the left and pivot index sum
            if leftSum == rightSum:
                return i
            leftSum += nums[i]
        return -1
