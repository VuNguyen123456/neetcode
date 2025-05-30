class TimeMap:

  def __init__(self):
    self.timeMap = {} #key , value[val, time]
  # Set the stuff with dictionary with each key assiciate with a list of stuff
  def set(self, key: str, value: str, timestamp: int) -> None:
    if key in self.timeMap:
      self.timeMap[key].append([value, timestamp])
    else:
      self.timeMap[key] = []
      self.timeMap[key].append([value, timestamp])
      
  def get(self, key: str, timestamp: int) -> str:
    if key not in self.timeMap:
      return ""
    l = 0
    r = len(self.timeMap[key]) - 1
    result = ""
    # Basically just goes through the key list with Binary search
    while l <= r:
      m = l + (r-l)//2
      if self.timeMap[key][m][1] == timestamp:
        return self.timeMap[key][m][0]
      if self.timeMap[key][m][1] < timestamp:
        # always move toward right because: if l increase middle move right, if r decrease middle didn't got check in the 1st place so it stay still
        result = self.timeMap[key][m][0]
        l = m+1
      else:
        r = m-1
    return result
