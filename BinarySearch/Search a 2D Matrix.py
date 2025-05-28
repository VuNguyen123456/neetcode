class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        l = 0
        r = len(matrix) - 1
        theOne = 0
        while l <= r:
            m = l + (r-l)//2
            if matrix[m][0] == target:
                return True
            elif matrix[m][-1] == target:
                return True
            if matrix[m][0] > target:
                r = m-1
            elif matrix[m][-1] < target:
                l = m+1
            else:
                theOne = m
                break
        l = 0
        r = len(matrix[theOne]) - 1
        while l <= r:
            m = l + (r-l)//2
            if matrix[theOne][m] == target:
                return True
            if matrix[theOne][m] > target:
                r = m-1
            else:
                l = m+1
        return False
