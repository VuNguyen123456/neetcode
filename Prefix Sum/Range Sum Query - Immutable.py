class NumArray:

    def __init__(self, nums: List[int]):
        self.NumArray = []
        self.SumTillIndex = []
        tempSum = 0
        for i in range(len(nums)):
            tempSum += nums[i]
            self.NumArray.append(nums[i])
            self.SumTillIndex.append(tempSum)
        # print(self.NumArray)
        # print(self.SumTillIndex)

    def sumRange(self, left: int, right: int) -> int:
        return (self.SumTillIndex[right] - self.SumTillIndex[left]) + self.NumArray[left]

# Your NumArray object will be instantiated and called as such:
# obj = NumArray(nums)
# param_1 = obj.sumRange(left,right)
