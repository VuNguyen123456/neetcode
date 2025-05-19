# class Solution:
#     def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
#         res = defaultdict(list)
#         for i in strs:
#             sortedString = ''.join(sorted(i))
#             res[sortedString].append(i)
        
#         return list(res.values())

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
      dic = {}
      result = []
      for i in strs:
        string = ''.join(sorted(i))
        if string not in dic:
          dic[string] = [i]
        else:
          dic[string].append(i)
      for i in dic:
        result.append(dic[i])
      return result
