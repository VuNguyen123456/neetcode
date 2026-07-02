import math
from datetime import datetime, timedelta
import copy

class InMemoryDatabase:
    def __init__(self):
        self.db = {}
        self.history = {}

    def set(self, key, field, value):
        if key not in self.db:
            self.db[key] = {}
        self.db[key][field] = {"value": value, "ttl": None}
        return ""

    def get(self, key, field):
        if key not in self.db or field not in self.db[key]:
            return ""
        return self.db[key][field]["value"]
    
    def delete(self, key, field):
        if key not in self.db or field not in self.db[key]:
            return "false"
        self.db[key].pop(field)
        return "true"
    
    def scan(self, key):
        return self.scan_by_prefix(key, "")

    def scan_by_prefix(self, key, prefix):
        if key not in self.db:
            return ""
        all_fields_of_key = [field for field in self.db[key] if field.startswith(prefix)]
        all_fields_of_key.sort()
        return ", ".join(f"{field}({self.db[key][field]['value']})" for field in all_fields_of_key)
    
    def set_at(self, key, field, value, timestamp):
        if key not in self.db:
            self.db[key] = {}
        self.db[key][field] = {"value": value, "ttl": None, "created_at": timestamp}
        return ""
    
    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        if key not in self.db:
            self.db[key] = {}
        self.db[key][field] = {"value": value, "ttl": ttl, "created_at": timestamp}
        return ""
    
    def delete_at(self, key, field, timestamp):
        if key not in self.db or field not in self.db[key] or not self.is_alive(key, field, timestamp):
            return "false"
        self.db[key].pop(field)
        return "true"
    
    def is_alive(self, key, field, timestamp):
        if self.db[key][field]["ttl"] is None:
            return True
        return timestamp < self.db[key][field]["created_at"] + self.db[key][field]["ttl"]
    
    def get_at(self, key, field, timestamp):
        if key not in self.db or field not in self.db[key] or not self.is_alive(key, field, timestamp):
            return ""
        return self.db[key][field]["value"]
    
    def scan_by_prefix_at(self, key, prefix, timestamp):
        if key not in self.db:
            return ""
        all_fields_of_key = [field for field in self.db[key] if field.startswith(prefix) and self.is_alive(key, field, timestamp)]
        all_fields_of_key.sort()
        return ", ".join(f"{field}({self.db[key][field]['value']})" for field in all_fields_of_key)
    
    def scan_at(self, key, timestamp):
        return self.scan_by_prefix_at(key, "", timestamp)

    def backup(self, timestamp):
        self.history[timestamp] = copy.deepcopy(self.db)
        # Do they want to recalc ttl or something?
        num = 0
        for key in self.db:
            alive_fields = [f for f in self.db[key] if self.is_alive(key, f, timestamp)]
            if len(alive_fields) > 0:
                num += 1
        return str(num)
    
    def restore(self, timestamp, timestampToRestore):
        possible_time = [ts for ts in self.history if ts < timestampToRestore]
        restored_one = max(possible_time)
        self.db = copy.deepcopy(self.history[restored_one])
        # recal
        for key in self.db:
            for field in self.db[key]:
                # if they don't need recalc
                if self.db[key][field]["ttl"] is not None and self.is_alive(key, field, restored_one):
                    # remaining: need to calculate at the new created at
                    # (old_created_at + old_ttl) - new_created_at
                    remaining = (self.db[key][field]["created_at"] + self.db[key][field]["ttl"]) - restored_one
                    self.db[key][field]["created_at"] = timestamp
                    self.db[key][field]["ttl"] = remaining
        return ""
