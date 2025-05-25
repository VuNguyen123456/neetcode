class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        numStack = []
        val = 0
        for i in tokens:
            if i not in "+-*/":
                numStack.append((int(i)))
            elif i == "+":
                val = numStack[-2] + numStack[-1]
                numStack.pop()
                numStack.pop()
                numStack.append(val)
            elif i == "-":
                val = numStack[-2] - numStack[-1]
                numStack.pop()
                numStack.pop()
                numStack.append(val)
            elif i == "*":
                val = int(numStack[-2] * numStack[-1])
                numStack.pop()
                numStack.pop()
                numStack.append(val)
            elif i == "/":
                val = int(numStack[-2] / numStack[-1])
                numStack.pop()
                numStack.pop()
                numStack.append(val)
        return int(round(numStack[0]))
