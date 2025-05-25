class Solution:
    def isValid(self, s: str) -> bool:
        stack = []
        if len(s) % 2 != 0:
            return False
        for i in s:
            if i in "[({":
                stack.append(i)
            elif not stack:
                return False
            elif i == ']' and stack.pop() != '[':
                return False
            elif i == ')' and stack.pop() != '(':
                return False
            elif i == '}' and stack.pop() != '{':
                return False
        if stack:
            return False
        return True
