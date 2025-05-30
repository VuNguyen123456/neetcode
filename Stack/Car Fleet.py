class Solution:
  def carFleet(self, target: int, position: List[int], speed: List[int]) -> int:
    dic = {}
    stack = []
    for i in range(len(position)):
      dic[position[i]] = speed[i]
    sorted_dic = dict(sorted(dic.items(), reverse = True))
    for car_position in sorted_dic:
      time = (target - car_position) / sorted_dic[car_position]
      stack.append(time)
      if len(stack) >= 2 and stack[-1] <= stack[-2]:
        stack.pop()
    return len(stack)
    
    
