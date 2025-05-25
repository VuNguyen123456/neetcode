result = [0] * len(temperatures)  # final output array, initialized to 0
stack = []  # stack will store pairs: [temperature, index]

for i, t in enumerate(temperatures):
    # While the stack is not empty AND the current temperature is higher than the temperature at the top of the stack
    while stack and t > stack[-1][0]:
        stackT, stackInd = stack.pop()  # pop the colder day from the stack
        result[stackInd] = i - stackInd  # calculate the wait time for that day
    stack.append([t, i])  # push current day onto stack

return result
