# class LRUCache:
#     def __init__(self, capacity: int):
#         self.cap = capacity
#         self.leastUse = []  # List of keys, left = least recently used
#         self.dic = {}       # Key-value map

#     def get(self, key: int) -> int:
#         if key in self.dic:
#             # Move key to most recently used
#             self.leastUse.remove(key)
#             self.leastUse.append(key)
#             return self.dic[key]
#         return -1

#     def put(self, key: int, value: int) -> None:
#         if key in self.dic:
#             # Update value and move to most recently used
#             self.dic[key] = value
#             self.leastUse.remove(key)
#             self.leastUse.append(key)
#         else:
#             # Evict least recently used if full
#             if len(self.dic) >= self.cap:
#                 leastUseVal = self.leastUse.pop(0)
#                 del self.dic[leastUseVal]
#             # Insert new key
#             self.dic[key] = value
#             self.leastUse.append(key)

class LRUCache:
  def __init__(self, capacity: int):
    self.cache = OrderedDict()
    self.cap = capacity
  def get(self, key: int) -> int:
    if key in self.cache:
      self.cache.move_to_end(key)
      return self.cache[key]
    return -1
  def put(self, key: int, value: int) -> None:
    if key in self.cache:
      self.cache.move_to_end(key) # Moved the updated key to the head and update it values
      self.cache[key] = value
    else:
      if len(self.cache) < self.cap: # No need to remove
        self.cache[key] = value
      else:
        self.cache.popitem(last=False) # popo the top
        self.cache[key] = value
        
