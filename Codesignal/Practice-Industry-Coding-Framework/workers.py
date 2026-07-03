import math
from datetime import datetime, timedelta
import copy

class Workers:
    def __init__(self):
        self.workers = {}

    def ADD_WORKER(self, workerId, position, compensation):
        if workerId in self.workers:
            return "false"
        self.workers[workerId] = {"position": position, "compensation": compensation, "is_in_office": False, "enter_time": [], "leave_time": [], "time_spend_in_office": 0, "sessions": []}
        return "true"
    
    def REGISTER(self, workerId, timestamp):
        if workerId not in self.workers:
            return "invalid_request"
        pending = self.workers[workerId].get("pending_promotion")
        if pending and int(timestamp) >= pending["startTimestamp"]:
            self.workers[workerId]["position"] = pending["position"]
            self.workers[workerId]["compensation"] = pending["compensation"]
            self.workers[workerId]["pending_promotion"] = None
        compen = self.workers[workerId]["compensation"]
        if not self.workers[workerId]["is_in_office"]:
            self.workers[workerId]["enter_time"].append(int(timestamp))
            self.workers[workerId]["is_in_office"] = True
        else:
            self.workers[workerId]["leave_time"].append(int(timestamp))
            self.workers[workerId]["is_in_office"] = False
            self.workers[workerId]["time_spend_in_office"] += self.workers[workerId]["leave_time"][-1] - self.workers[workerId]["enter_time"][-1]
            self.workers[workerId]["sessions"].append((self.workers[workerId]["enter_time"][-1], self.workers[workerId]["leave_time"][-1], compen))

        return "registered"
    
    def GET(self, workerId):
        if workerId not in self.workers:
            return "" 
        return str(self.workers[workerId]["time_spend_in_office"])
        
    def TOP_N_WORKERS(self, n, position):
        matches = [w for w in self.workers if self.workers[w]["position"] == position]
        matches.sort(key=lambda x: (-int(self.GET(x)),x))

        topN = matches[:int(n)]

        res = []
        for w in topN:
            res.append(f"{w}({self.GET(w)})")

        return ", ".join(res)

    def PROMOTE(self, workerId, newPosition, newCompensation, startTimestamp):
        if workerId not in self.workers or self.workers[workerId].get("pending_promotion"):
            return "invalid_request"
        # if currently in office
        if self.workers[workerId]["is_in_office"]:
            self.workers[workerId]["pending_promotion"] = {
                "position": newPosition,
                "compensation": int(newCompensation),
                "startTimestamp": int(startTimestamp)
            }
            self.REGISTER(workerId, startTimestamp)
            self.REGISTER(workerId, startTimestamp)
        else:
            # store pending, apply when worker next enters at/after startTimestamp
            self.workers[workerId]["pending_promotion"] = {
                "position": newPosition,
                "compensation": int(newCompensation),
                "startTimestamp": int(startTimestamp)
            }

        return "success"
    
    def CALC_SALARY(self, workerId, startTimestamp, endTimestamp):
        if workerId not in self.workers:
            return ""
        start, end = int(startTimestamp), int(endTimestamp)
        salary = 0

        for enter, leave, comp in self.workers[workerId]["sessions"]:
            s = max(enter, start)
            e = min(leave, end)
            if e > s:
                salary += (e - s) * comp
        
        return str(salary)

        

        
